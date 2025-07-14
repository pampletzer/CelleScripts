# 🔑 Hash-Extraktor (hash_conv_Analyzer_to_PA)

Dieses PowerShell-Skript dient dazu, MD5- und SHA-Hashes aus einer spezifisch formatierten, tabulatorgetrennten Textdatei (z.B. einem Hash-Report oder einer Datenbank) zu extrahieren. Es bietet eine benutzerfreundliche grafische Oberfläche zur Dateiauswahl und speichert die extrahierten Hashes in separaten `.txt`-Dateien (MD5 in `md5.txt` und SHA in `sha.txt`) im selben Verzeichnis wie die Quelldatei.

---

## ✨ Funktionen

* `🖱️` **Grafische Dateiauswahl (GUI)**: Ermöglicht die einfache Auswahl der Quelldatei über ein Windows Forms Dialogfenster.
* `🔍` **Gezielte Hash-Extraktion**: Extrahiert den MD5-Hash aus der 5. Spalte und den SHA-Hash aus der 9. Spalte der tabulatorgetrennten Eingabedatei.
* `📊` **Fortschrittsanzeige**: Zeigt den Verarbeitungsfortschritt während der Dateianalyse in der Konsole an.
* `💾` **Separate Hash-Listen**: Erstellt zwei separate Textdateien (`md5.txt` und `sha.txt`) mit den jeweiligen extrahierten Hashes.
* `📁` **Ausgabe im Quellverzeichnis**: Die generierten Ausgabedateien werden automatisch im selben Ordner wie die ausgewählte Quelldatei gespeichert.

---

## ⚙️ Voraussetzungen

Um dieses Skript erfolgreich auszuführen, benötigen Sie:

* **Betriebssystem**: Windows.
* **PowerShell**: Version 5.1 oder neuer (Standard auf modernen Windows-Systemen).
* **Eingabedatei**: Eine tabulatorgetrennte Textdatei (z.B. `test.txt` oder `TBK_LKA_NI_HASHDB_*.txt`). Diese Datei muss:
    * MD5-Hashes in der **5. Spalte** (Index 4 bei 0-basierter Zählung) enthalten.
    * SHA-Hashes in der **9. Spalte** (Index 8 bei 0-basierter Zählung) enthalten.
    * **Achtung**: Andere Dateiformate oder Spaltenanordnungen werden nicht korrekt verarbeitet.

---

## 🚀 Verwendung

1.  **Skript platzieren**: Speichern Sie das Skript `hash_conv_Analyzer_to_PA.ps1` in einem Ordner Ihrer Wahl (z.B. `C:\Tools\HashExtractor`).
2.  **PowerShell im Ordner öffnen**:
    * Navigieren Sie im Windows-Explorer zu dem Ordner, in dem Sie `hash_conv_Analyzer_to_PA.ps1` gespeichert haben.
    * Halten Sie die `Shift`-Taste gedrückt und klicken Sie mit der **rechten Maustaste** auf einen leeren Bereich im Ordner.
    * Wählen Sie im Kontextmenü die Option "PowerShell-Fenster hier öffnen" oder "Terminal hier öffnen" (je nach Windows-Version).
3.  **Skript ausführen**: Geben Sie im geöffneten PowerShell-Fenster den folgenden Befehl ein und drücken Sie Enter:
    ```powershell
    .\hash_conv_Analyzer_to_PA.ps1
    ```
4.  **Datei auswählen**: Es öffnet sich ein "Bitte wählen Sie die Quelldatei 'test.txt'"-Dialogfenster. Navigieren Sie zu Ihrer tabulatorgetrennten Quelldatei und klicken Sie auf "Öffnen".
5.  **Verarbeitung und Ergebnis**: Das Skript verarbeitet die ausgewählte Datei und zeigt dabei eine Fortschrittsanzeige in der Konsole an. Nach Abschluss des Vorgangs werden zwei neue Dateien, `md5.txt` und `sha.txt`, im **selben Verzeichnis wie Ihre Quelldatei** erstellt. Diese enthalten die extrahierten MD5- bzw. SHA-Hashes, jeweils einen pro Zeile.
6.  **Skript beenden**: Das Skript zeigt eine Abschlussmeldung an und wartet auf einen Tastendruck, um das Fenster zu schließen.

---

## 👤 Autor

* Paul Ampletzer - paul.ampletzer@gmail.com

---
