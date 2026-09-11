"""
Converte tutti i .txt nella cartella in UTF-8 (senza BOM).
Rileva automaticamente l'encoding sorgente.
"""
from pathlib import Path
from charset_normalizer import from_bytes

CARTELLA = r"C:\Users\owner\Downloads\Gare_Documenti\Azienda Zero\DocumentiDiGara\OK"
DRY_RUN = False   # True = solo report, non modifica nulla

cartella = Path(CARTELLA)
if not cartella.is_dir():
    raise SystemExit(f"Cartella non trovata: {CARTELLA}")

files = sorted(cartella.glob("*.txt"))
print(f"Trovati {len(files)} file .txt\n")

ok_count = 0
falliti = []
gia_utf8 = 0

for f in files:
    try:
        raw = f.read_bytes()
        result = from_bytes(raw).best()
        if result is None:
            raise ValueError("nessun encoding plausibile")

        enc = result.encoding
        testo = str(result)

        if not DRY_RUN:
            f.write_text(testo, encoding='utf-8', newline='')

        if enc in ('utf_8', 'ascii'):
            gia_utf8 += 1
        ok_count += 1
        print(f"OK   [{enc:12s}] {f.name}")

    except Exception as e:
        falliti.append((f.name, str(e)))
        print(f"FAIL              {f.name} -> {e}")

print(f"\n{'='*60}")
print(f"Totale:     {len(files)}")
print(f"OK:         {ok_count}  (di cui già UTF-8/ASCII: {gia_utf8})")
print(f"Falliti:    {len(falliti)}")
print(f"Modalità:   {'DRY-RUN (nessuna modifica)' if DRY_RUN else 'SCRITTURA ATTIVA'}")

if falliti:
    print("\nFile falliti:")
    for nome, err in falliti:
        print(f"  - {nome}: {err}")