# 🗑️ Delete Cellebrite Temporary Folders

Dieses PowerShell-Skript automatisiert das Auffinden und Löschen von temporären Ordnern, die den Namen "Cellebrite" enthalten, innerhalb des `AppData\Local\Temp`-Verzeichnisses aller Benutzerprofile auf einem Windows-System. Es wurde entwickelt, um übrig gebliebene Dateien zu bereinigen und Speicherplatz freizugeben.

---

## ✨ Funktionen

* **Automatische Identifizierung**: Findet und löscht automatisch temporäre Ordner, die mit "Cellebrite" in Verbindung stehen.
* **Umfassende Suche**: Durchsucht die temporären Verzeichnisse aller Benutzerprofile auf dem System.
* **Administratorrechte**: Erfordert Administratorberechtigungen für eine vollständige Ausführung.
* **Feedback**: Bietet klares Feedback über gefundene und gelöschte Ordner.

---

## ⚙️ Voraussetzungen

Um dieses Skript erfolgreich auszuführen, benötigen Sie:

* **Betriebssystem**: Windows (Das Skript verwendet PowerShell und Windows-spezifische Pfade).
* **PowerShell**: Version 5.1 oder neuer (Standard auf modernen Windows-Systemen).
* **Administratorrechte**: Das Skript muss mit erhöhten Berechtigungen ausgeführt werden. Wenn es ohne Administratorrechte gestartet wird, versucht es, sich selbst mit diesen Rechten neu zu starten.

---

## 🚀 Verwendung

1.  **Speichern des Skripts**:
    Speichern Sie den bereitgestellten Code als `DeleteTempCellebrite.ps1` an einem Ort Ihrer Wahl (z.B. `C:\Scripts`).

2.  **PowerShell als Administrator öffnen**:
    * Suchen Sie für eine manuelle Ausführung nach "PowerShell" im Startmenü.
    * Rechtsklicken Sie auf "Windows PowerShell" oder "PowerShell" und wählen Sie "Als Administrator ausführen".
    * Alternativ können Sie das Skript auch direkt ausführen; es wird dann versuchen, sich selbst mit Administratorrechten neu zu starten.

3.  **Zum Skriptverzeichnis navigieren (falls manuell geöffnet)**:
    Wechseln Sie im PowerShell-Fenster in das Verzeichnis, in dem Sie das Skript gespeichert haben:
    ```powershell
    cd C:\Scripts
    # Ersetzen Sie C:\Scripts durch den tatsächlichen Pfad.
    ```

4.  **Skript ausführen**:
    Starten Sie das Skript mit folgendem Befehl:
    ```powershell
    .\DeleteTempCellebrite.ps1
    ```
    Das Skript wird die gefundenen Ordner auflisten und deren Löschung bestätigen. Es wird am Ende pausieren, bis Sie eine Taste drücken.

---

## ⚠️ Wichtige Hinweise / Haftungsausschluss

* Dieses Skript führt Dateilöschvorgänge durch. Während es spezifische temporäre Ordner gezielt löscht, **lassen Sie immer Vorsicht walten**, wenn Sie Skripte mit Administratorprivilegien ausführen, insbesondere solche, die Dateien löschen.
* Es wird empfohlen, die Funktionsweise des Skripts zu verstehen, bevor Sie es ausführen.
* Das Skript sucht explizit nach Ordnern, die "Cellebrite" in ihrem Namen enthalten. Stellen Sie sicher, dass dies das beabsichtigte Ziel ist.

---

## 👤 Autor

* Paul Ampletzer - paul.ampletzer@gmail.com

---

