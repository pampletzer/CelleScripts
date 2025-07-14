# 📦 Amazon Ergebnisse zu Text (D01-Extraktor)

Dieses Python-Skript wurde entwickelt, um spezifische "D01"-Referenznummern aus einer Excel-Datei zu extrahieren. Es durchsucht die Spalte 'Body' in der Datei `Exported results.xlsx`, findet alle eindeutigen Muster wie `D01-XXXXXXX-XXXXXXX` (wobei X eine Ziffer ist) und speichert diese in einer neuen Textdatei (`onlyd01.txt`), wobei jede Referenznummer in einer eigenen Zeile steht.

---

## ✨ Funktionen

* **D01-Muster-Extraktion**: Extrahiert spezifische "D01-XXXXXXX-XXXXXXX"-Muster aus Excel-Dateien.
* **Spaltenbasierte Suche**: Verarbeitet die Spalte 'Body' des Excel-Sheets als Datenquelle.
* **Duplikatentfernung**: Entfernt doppelte Einträge, um eine Liste eindeutiger Referenzen zu erstellen.
* **Textdatei-Export**: Speichert die extrahierten Referenzen in einer einfachen `.txt`-Datei, jeweils eine pro Zeile.

---

## ⚙️ Voraussetzungen

Um dieses Skript erfolgreich auszuführen, benötigen Sie:

* **Python**: Eine installierte Python-Version (empfohlen wird Python 3.x).
* **Pandas Bibliothek**: Die `pandas`-Bibliothek muss installiert sein. Sie können sie über die Kommandozeile installieren:
    ```bash
    pip install pandas
    ```
* **Eingabedatei**: Eine Excel-Datei mit dem Namen `Exported results.xlsx` muss im selben Verzeichnis wie das Skript vorhanden sein. Diese Excel-Datei muss eine Spalte mit dem Titel 'Body' enthalten, in der die zu extrahierenden D01-Referenzen vermutet werden.

---

## 🚀 Verwendung

1.  **Skript und Excel-Datei platzieren**:
    * Speichern Sie das Python-Skript `amazon_results_to_txt_D01.py` in einem Ordner Ihrer Wahl (z.B. `C:\Tools\Amazon_Extractor`).
    * Legen Sie Ihre Excel-Datei (`Exported results.xlsx`), die die 'Body'-Spalte mit den D01-Nummern enthält, **im selben Ordner** ab.

2.  **Kommandozeile im Ordner öffnen**:
    * Navigieren Sie im Windows-Explorer zu dem Ordner, in dem Sie die Dateien gespeichert haben.
    * Halten Sie die `Shift`-Taste gedrückt und klicken Sie mit der **rechten Maustaste** auf einen leeren Bereich im Ordner.
    * Wählen Sie im Kontextmenü die Option "PowerShell-Fenster hier öffnen" oder "Terminal hier öffnen" (je nach Windows-Version).

3.  **Skript ausführen**:
    Geben Sie im geöffneten Terminal den folgenden Befehl ein und drücken Sie Enter:
    ```bash
    python amazon_results_to_txt_D01.py
    ```

4.  **Ergebnis**:
    Nach der Ausführung wird eine neue Datei namens `onlyd01.txt` im selben Ordner erstellt. Diese Datei enthält alle gefundenen, eindeutigen "D01"-Referenznummern, jeweils in einer neuen Zeile.

---

## 📄 Beispiel `onlyd01.txt` Inhalt

    D01-1234567-8901234
    D01-9876543-2109876
    D01-1122334-5566778
    ...


---

## 👤 Autor

* Paul Ampletzer - paul.ampletzer@gmail.com

---
