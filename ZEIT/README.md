# ⏳ Zukunft Erkennen In Timestamps (ZEIT)

Dieses PowerShell-Skript konvertiert Unix- oder Android-Timestamps in ein für Menschen lesbares lokales Datums- und Zeitformat. Es ist ein einfaches Tool, um Zeitstempel schnell zu interpretieren.

---

## ✨ Funktionen

* **Timestamp-Erkennung**: Erkennt automatisch, ob es sich um einen 10-stelligen Unix-Timestamp (Sekunden) oder einen 13-stelligen Android-Timestamp (Millisekunden) handelt.
* **Datums- und Zeitkonvertierung**: Wandelt den eingegebenen Timestamp in das lokale Datums- und Zeitformat um.
* **Benutzerfreundlich**: Einfache Eingabeaufforderung und direkte Ausgabe.
* **Fehlerbehandlung**: Fängt ungültige Eingaben ab.

---

## ⚙️ Voraussetzungen

Um dieses Skript erfolgreich auszuführen, benötigen Sie:

* **Betriebssystem**: Windows (Das Skript verwendet PowerShell).
* **PowerShell**: Version 5.1 oder neuer (Standard auf modernen Windows-Systemen).

---

## 🚀 Verwendung

1.  **Speichern des Skripts**:
    Speichern Sie den bereitgestellten Code als `ZEIT.ps1` an einem Ort Ihrer Wahl (z.B. `C:\Tools`).

2.  **PowerShell öffnen**:
    * Suchen Sie im Startmenü nach "PowerShell".
    * Öffnen Sie die "Windows PowerShell" oder "PowerShell" App (Administratorrechte sind für dieses Skript nicht zwingend erforderlich, schaden aber auch nicht).

3.  **Zum Skriptverzeichnis navigieren**:
    Wechseln Sie im PowerShell-Fenster in das Verzeichnis, in dem Sie das Skript gespeichert haben:
    ```powershell
    cd C:\Tools
    # Ersetzen Sie C:\Tools durch den tatsächlichen Pfad
    ```

4.  **Skript ausführen**:
    Starten Sie das Skript mit folgendem Befehl:
    ```powershell
    .\ZEIT.ps1
    ```

5.  **Zeitstempel eingeben**:
    Das Skript fordert Sie auf, einen Zeitstempel einzugeben:
    ```
    Zeitstempel:
    ```
    Geben Sie hier Ihren 10-stelligen Unix-Timestamp oder 13-stelligen Android-Timestamp ein (z.B. `1678886400` für Unix oder `1678886400000` für Android) und drücken Sie Enter.

6.  **Ergebnis ablesen**:
    Das Skript zeigt das konvertierte Datum und die Uhrzeit an. Anschließend werden Sie aufgefordert, "exit" einzugeben, um das Skript zu beenden.

    **Beispielausgabe für einen Unix-Timestamp (1678886400):**
    ```
    Zeitstempel: 1678886400
    Unix Timestamp
    14.03.2023 09:00:00
    exit:
    ```

    **Beispielausgabe für einen Android-Timestamp (1678886400000):**
    ```
    Zeitstempel: 1678886400000
    Android Timestamp
    14.03.2023 09:00:00
    exit:
    ```

    **Beispielausgabe für eine ungültige Eingabe:**
    ```
    Zeitstempel: abc
    Kein Gülter Timestamp
    Kein gültiger Timestamp
    exit:
    ```

---

## 👤 Autor

* Paul Ampletzer

---
