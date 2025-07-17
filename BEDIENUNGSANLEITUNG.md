# Bedienungsanleitung: Marker Analyse Cockpit

## Empfehlung für Schema-Format
Das Marker-Schema sollte im YAML-Format vorliegen, da YAML eine klare Struktur erlaubt und zusätzlich Kommentare unterstützt. Dadurch lassen sich komplexe Zusammenhänge leicht lesbar abbilden.

## Installation
Führen Sie die Installation der benötigten Pakete mit folgendem Befehl aus:

```bash
pip install streamlit pyyaml openai
```

## Starten der Anwendung
Die Anwendung wird über Streamlit gestartet. Verwenden Sie dazu **nicht** `python app.py`, da dies zu `ScriptRunContext`-Warnungen führt. Stattdessen lautet der korrekte Befehl:

```bash
streamlit run app.py
```

## Schritt-für-Schritt-Anleitung
1. **API-Key**: Geben Sie im Seitenbereich Ihren OpenAI API-Key ein.
2. **Schema-Lader**: Laden Sie optional eine eigene Schema-Datei im YAML-Format hoch. Ohne Upload wird `default_schema.yaml` verwendet.
3. **Marker-Lader**: Wählen Sie einzelne Marker-Dateien aus oder geben Sie alternativ den Namen eines Ordners an, aus dem alle Marker-Dateien geladen werden.
4. **Text für Analyse**: Geben Sie den zu analysierenden Text ein und klicken Sie auf **Analysieren**.

## Interpretation der Ergebnisse
- **Linke Spalte**: Zeigt den Originaltext mit farblich hervorgehobenen Markern und listet erkannte atomare sowie semantische Marker auf.
- **Rechte Spalte**: Enthält die narrative Antwort der GPT-4 API zur semantischen Analyse.
