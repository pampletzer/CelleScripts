# 💬 SfS - Sprachnachrichten für Schreibprogramm

Dieses Tool konvertiert automatisch Audio-Dateien (M4A, MP4, Opus) in das AMR-Format (`.amr`), welches oft für bestimmte Telefonie- oder Diktieranwendungen benötigt wird. Es ist ideal, um Sprachnachrichten für die Nutzung in Schreibprogrammen oder spezifischer Software vorzubereiten. Das Tool ist eine kompilierte Anwendung (EXE), die **FFmpeg** intern verwendet, um die Konvertierungsaufgaben zu bewältigen. Es ist für eine einfache Drag-and-Drop- oder Verzeichnisverarbeitung konzipiert.

---

## ✨ Funktionen

* [cite_start]`🔄` **Automatisierte Konvertierung**: Wandelt `.m4a` [cite: 4][cite_start], `.mp4`  [cite_start]und `.opus`  [cite_start]Dateien in `.amr`  um.
* [cite_start]`📦` **Selbstständig**: Beinhaltet `ffmpeg.exe` direkt in der ausführbaren Datei, sodass keine separate Installation von FFmpeg erforderlich ist.
* [cite_start]`📁` **Verzeichnisbasiert**: Sucht und konvertiert automatisch alle unterstützten Dateien im selben Verzeichnis, in dem die Anwendung gestartet wird.
* [cite_start]`🗜️` **Dateinamensäuberung**: Bereinigt Dateinamen von Sonderzeichen und Emoticons, um Probleme bei der Dateiverarbeitung zu vermeiden.
* [cite_start]`✅` **Fehlermeldungen**: Zeigt bei fehlgeschlagenen Konvertierungen detaillierte Fehlermeldungen an.
* [cite_start]`🚀` **Benachrichtigung**: Gibt eine Bestätigung aus, sobald eine Datei erfolgreich konvertiert wurde, und wenn alle Konvertierungen abgeschlossen sind.

---

## ⚙️ Voraussetzungen

* **Betriebssystem**: Windows.
* [cite_start]**Eingabedateien**: `.m4a`, `.mp4` oder `.opus`-Audiodateien, die konvertiert werden sollen.

---

## 🚀 Verwendung

1.  **Tool platzieren**:
    * Legen Sie die `SfS.exe` (die Ihnen bereitgestellt wurde) in den **gleichen Ordner**, in dem sich auch Ihre zu konvertierenden Audio-Dateien (`.m4a`, `.mp4`, `.opus`) befinden.

2.  **Tool ausführen**:
    * Doppelklicken Sie einfach auf die `SfS.exe`-Datei.

3.  **Konvertierungsprozess**:
    * [cite_start]Das Tool startet und beginnt automatisch, alle unterstützten Audio-Dateien im aktuellen Verzeichnis zu verarbeiten.
    * [cite_start]Während der Konvertierung wird ein kleiner Hinweis (Tooltip) angezeigt, welche Datei gerade verarbeitet wird.
    * [cite_start]Bei erfolgreicher Konvertierung wird eine `[OriginalDateiname].amr`-Datei im selben Ordner erstellt.
    * [cite_start]Sollte eine Konvertierung fehlschlagen, wird eine Fehlermeldung mit Details zum Problem angezeigt.

4.  **Abschluss**:
    * [cite_start]Nachdem alle unterstützten Dateien im Ordner verarbeitet wurden, erscheint eine Meldung `Done converting all audio files.` 
    * Drücken Sie `OK`, um das Tool zu beenden.

---

## ⚠️ Wichtige Hinweise

* [cite_start]**Dateiformat**: Das Tool ist spezifisch für die Konvertierung von `.m4a`, `.mp4` und `.opus` zu `.amr` ausgelegt. Andere Dateitypen werden ignoriert.
* [cite_start]**Ausgabeort**: Die konvertierten `.amr`-Dateien werden im **selben Ordner** wie die Originaldateien und die `SfS.exe` abgelegt.
* [cite_start]**FFmpeg-Extraktion**: Das Tool entpackt eine temporäre `ffmpeg.exe` in das temporäre Verzeichnis Ihres Systems. [cite_start]Diese temporäre Datei wird nach Beendigung des Tools wieder gelöscht.

---

## 👤 Autor

* [cite_start]Paul Ampletzer - paul.ampletzer@gmail.com 

---
