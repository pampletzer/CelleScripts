# 🔑 Gray-Extraktor (Passwortlisten-Konverter)

Dieses Python-Skript dient dazu, Passwörter aus einer spezifisch formatierten Textdatei zu extrahieren und in eine neue, bereinigte Passwortliste zu überführen. Es sucht nach einem Muster wie "Item value: [Passwort]", entfernt den Vorspann "Item value:" und speichert jedes Passwort in einer eigenen Zeile in einer neuen Textdatei.

---

## ✨ Funktionen

* `🔍` **Mustererkennung**: Sucht nach Zeilen, die dem Muster `.*Item value:.*` entsprechen, um Passwörter zu identifizieren.
* `🧹` **Textbereinigung**: Entfernt den Vorspann "Item value:" aus den gefundenen Zeilen, um nur das reine Passwort zu extrahieren.
* `📄` **Wildcard-Dateisuche**: Findet die Eingabedatei automatisch anhand des Musters `*_passwords.txt` im selben Verzeichnis.
* `💾` **Standardisierte Ausgabe**: Speichert die extrahierten Passwörter in einer neuen Datei namens `newpasswordlist.txt`, wobei jedes Passwort in einer eigenen Zeile steht.

---

## ⚙️ Voraussetzungen

Um dieses Skript erfolgreich auszuführen, benötigen Sie:

* **Python**: Eine installierte Python-Version (empfohlen wird Python 3.x).
* **Eingabedatei**: Eine Textdatei, die Passwörter im Format `Item value: [Passwort]` enthält und deren Dateiname auf `_passwords.txt` endet (z.B. `export_passwords.txt` oder `mydata_passwords.txt`). Diese Datei muss sich im selben Verzeichnis wie das Skript befinden.

---

## 🚀 Verwendung

1.  **Skript und Passwortdatei platzieren**:
    * Speichern Sie das Python-Skript `gray_to_pa_passwordlist.py` in einem Ordner Ihrer Wahl (z.B. `C:\Tools\PasswordExtractor`).
    * Legen Sie Ihre Passwortdatei (z.B. `mein_export_passwords.txt`), die die zu extrahierenden Passwörter enthält, **im selben Ordner** ab.

2.  **Kommandozeile im Ordner öffnen**:
    * Navigieren Sie im Windows-Explorer zu dem Ordner, in dem Sie die Dateien gespeichert haben.
    * Halten Sie die `Shift`-Taste gedrückt und klicken Sie mit der **rechten Maustaste** auf einen leeren Bereich im Ordner.
    * Wählen Sie im Kontextmenü die Option "PowerShell-Fenster hier öffnen" oder "Terminal hier öffnen" (je nach Windows-Version).

3.  **Skript ausführen**:
    Geben Sie im geöffneten Terminal den folgenden Befehl ein und drücken Sie Enter:
    ```bash
    python gray_to_pa_passwordlist.py
    ```

4.  **Ergebnis**:
    Nach der Ausführung wird eine neue Datei namens `newpasswordlist.txt` im selben Ordner erstellt. Diese Datei enthält alle gefundenen und bereinigten Passwörter, jeweils in einer neuen Zeile. Das Skript gibt außerdem den Namen der gefundenen Eingabedatei sowie die extrahierten Passwörter in der Konsole aus.

---

## 📄 Beispiel `newpasswordlist.txt` Inhalt

    Passwort123
    MeinGeheimesPW!
    EasyPeasy
    ...


---

## 👤 Autor

* Paul Ampletzer - paul.ampletzer@gmail.com

---
