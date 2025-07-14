# ✂️ CSC - Chat Schönheits Chirurg

Dieses PowerShell-Skript erstellt eine bereinigte Version eines HTML-Reports, indem es bestimmte Dateisysteminformationen (Stacks) automatisch ausblendet und einen Hinweis auf die gekürzte Version am Ende des Berichts hinzufügt. Es ist besonders nützlich, um Berichte für Präsentationen oder Weitergabe vorzubereiten, bei denen sensible Dateipfade nicht sichtbar sein sollen, während der Originalbericht für die vollständige Dokumentation erhalten bleibt.

---

## ✨ Funktionen

* **Dateisysteminformationen ausblenden**: Versteckt automatisch "Stack"-Informationen im HTML-Report, die oft Dateipfade oder interne Strukturen enthalten.
* **Neue Report-Version**: Erstellt eine separate HTML-Datei (`Print_Report.html`), sodass der Originalbericht (`Report.html`) unverändert bleibt.
* **Automatischer Hinweis**: Fügt am Ende des neuen Berichts einen auffälligen Hinweis ein, dass es sich um eine gekürzte Version handelt.
* **Fortschrittsanzeige**: Zeigt eine Fortschrittsleiste während der Bearbeitung des Reports an.
* **Benutzerinteraktion**: Führt den Benutzer durch den Prozess mit Anweisungen und Wartezeiten.

---

## ⚙️ Voraussetzungen

Um dieses Skript erfolgreich auszuführen, benötigen Sie:

* **Betriebssystem**: Windows.
* **PowerShell**: Version 5.1 oder neuer (Standard auf modernen Windows-Systemen).
* **Originalbericht**: Eine HTML-Datei namens `Report.html` muss sich im selben Verzeichnis wie das Skript befinden.

---

## 🚀 Verwendung

1.  **Skript und Report platzieren**:
    * Speichern Sie das Skript unter dem Namen `CSC.ps1` in dem Ordner, in dem sich Ihr Originalbericht (`Report.html`) befindet.
    * Stellen Sie sicher, dass Ihr Originalbericht ebenfalls `Report.html` heißt und sich im **selben Ordner** wie das Skript befindet.

2.  **PowerShell im Ordner öffnen**:
    * Navigieren Sie im Windows-Explorer zu dem Ordner, in dem Sie `CSC.ps1` und `Report.html` gespeichert haben.
    * Halten Sie die `Shift`-Taste gedrückt und klicken Sie mit der **rechten Maustaste** auf einen leeren Bereich im Ordner.
    * Wählen Sie im Kontextmenü die Option "PowerShell-Fenster hier öffnen" oder "Terminal hier öffnen" (je nach Windows-Version).

3.  **Skript ausführen**:
    Geben Sie im geöffneten PowerShell-Fenster den folgenden Befehl ein und drücken Sie Enter:
    ```powershell
    .\CSC.ps1
    ```

4.  **Anweisungen folgen**:
    * Das Skript zeigt eine Einleitung und fordert Sie auf, eine beliebige Taste zu drücken, um fortzufahren.
    * Es erstellt dann eine neue Datei namens `Print_Report.html` im selben Verzeichnis. Eine Fortschrittsleiste zeigt den Bearbeitungsfortschritt an.
    * Nach Abschluss erhalten Sie eine Bestätigung, dass der Vorgang abgeschlossen ist, und können das Fenster durch Drücken einer beliebigen Taste schließen.

---

## ⚠️ Wichtige Hinweise / Haftungsausschluss

* **Originalbericht aufbewahren**: Das Skript erstellt eine *zweite* Version des Berichts. Der Originalbericht (`Report.html`) sollte immer für die vollständige Dokumentation aufbewahrt werden.
* **Inhaltsintegrität**: Das Skript zielt darauf ab, lediglich Dateisysteminformationen auszublenden. Es ist wichtig, die Integrität der Chat-Inhalte selbst manuell zu überprüfen, da diese unverändert bleiben sollten.
* **Verkauf des Erstgeborenen und Koks**: Der humoristische Hinweis im Skript über den Verkauf von "Erstgeborenem und 10kg Koks" ist natürlich nicht ernst gemeint und dient lediglich der Belustigung des Nutzers.

---

## 👤 Autor

* Paul Ampletzer - paul.ampletzer@gmail.com

---
