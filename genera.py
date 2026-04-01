import os
import glob
from datetime import datetime

# 1. Scansiona l'ambiente e trova l'ultimo log
files = glob.glob("giorno*.html")
numeri = []
for f in files:
    try:
        numeri.append(int(f.replace("giorno", "").replace(".html", "")))
    except ValueError:
        pass

nuovo_num = max(numeri) + 1 if numeri else 1
nuovo_file = f"giorno{nuovo_num}.html"
data_odierna = datetime.now().strftime("%d/%m/%Y")

# 2. Il Template Strutturale
template = f"""<!DOCTYPE html>
<html>
<head>
    <title>Giorno {nuovo_num} - N3SSUN0PE LAB</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav style="width: 100%; background: var(--card); padding: 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.1); position: sticky; top: 0; z-index: 100; display: flex; justify-content: center; margin-bottom: 2rem;">
        <div style="width: 100%; max-width: 800px; display: flex; justify-content: space-between; padding: 0 1rem;">
            <span style="font-weight: bold; color: var(--accent);">N3SSUN0PE LAB</span>
            <div>
                <a href="index.html" style="margin-left: 1.5rem; font-size: 0.9rem;">Home</a>
                <a href="archivio.html" style="margin-left: 1.5rem; font-size: 0.9rem;">Archivio</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <h1>Appunti del Giorno {nuovo_num}</h1>
        <p style="color: var(--text-dim); text-align: center;">Data: {data_odierna}</p>
        <div class="log-card">
            <h2>Titolo argomento...</h2>
            <p>Sostituisci questo testo con i log di oggi.</p>
        </div>
    </div>
</body>
</html>"""

# Genera fisicamente il file (QUESTO E' IL PEZZO CHE AVEVI PERSO)
with open(nuovo_file, "w", encoding="utf-8") as f:
    f.write(template)

# 3. L'Iniezione nell'Archivio
with open("archivio.html", "r", encoding="utf-8") as f:
    archivio = f.read()

# Creiamo il bersaglio assemblandolo per evitare censure
bersaglio = "<" + "!-- INJECT_HERE --" + ">"

nuovo_link = f'{bersaglio}\n        <li style="margin-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem;">\n            <a href="{nuovo_file}">🔨 Giorno {nuovo_num}: Appunti del {data_odierna}</a>\n        </li>'

if bersaglio in archivio:
    archivio = archivio.replace(bersaglio, nuovo_link)
    with open("archivio.html", "w", encoding="utf-8") as f:
        f.write(archivio)
    print(f"Script completato: {nuovo_file} generato e indicizzato in archivio.")
else:
    print(f"ERRORE: File {nuovo_file} creato, ma il bersaglio non è stato trovato in archivio.html.")

# 4. Aggiornamento della Home (index.html)
with open("index.html", "r", encoding="utf-8") as f:
    home = f.read()

start_tag = "<" + "!-- LATEST_START --" + ">"
end_tag = "<" + "!-- LATEST_END --" + ">"

if start_tag in home and end_tag in home:
    # Tagliamo a fette il file usando i marcatori come lame
    prima_del_blocco = home.split(start_tag)[0]
    dopo_il_blocco = home.split(end_tag)[1]
    
    # Forgiamo il nuovo pezzo
    nuovo_contenuto = f'\n        <p>Giorno {nuovo_num}: Appunti del {data_odierna}</p>\n        <a href="{nuovo_file}" class="btn" style="display: inline-block; background: var(--accent); color: var(--bg); padding: 0.8rem 1.5rem; border-radius: 8px; font-weight: bold; margin-top: 1rem;">Leggi l\'ultimo log</a>\n        '
    
    # Riappiccichiamo i pezzi
    home_aggiornata = prima_del_blocco + start_tag + nuovo_contenuto + end_tag + dopo_il_blocco
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(home_aggiornata)
    print("Home aggiornata con successo.")
else:
    print("ERRORE: Marcatori LATEST_START o LATEST_END non trovati in index.html.")