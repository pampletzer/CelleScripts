Convert-to-MP3 Tool
====================

Usage:
1. Place your .m4a and/or .opus .mp4 audio files in the same folder as convert.exe
2. Run convert.exe
3. It will automatically convert all audio files to .amr using embedded ffmpeg.

Notes:
- This tool includes ffmpeg.exe as an embedded resource.
- No installation required.
- Output files will appear in the same directory.
- ffmpeg is extracted to %TEMP% and used from there.

Created using AutoHotkey.

keine Sonderzeichen im Ordner

https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-2025-06-08-git-5fea5e3e11-essentials_build.7z <-FFMPEG
in bin folder the ffmpeg.exe for compiling with autohotkey

AMR Quality is bad but hey - problem for another day

Snippet from the FAQ Page
====================

Folgende Audio-Formate können importiert werden:

Adaptive Multirate Codec(Dateiendung: .amr)
Advanced Audio Coding (Dateiendungen: .aac, .3gp,.mp4, .m4a)

Die Diktate können durch Drag & Drop oder über den Befehl Importieren in der Menüleiste (Datei-> "Importieren") importiert werden. Dabei werden die Dateien in WAV-Dateien gewandelt und in "Eigene Diktate" abgelegt.

Hinweis:

Zum Importieren von Dateien, die mit dem Advanced Audio Coding (AAC) Codec erstellt wurden, muss ein entsprechender Decoder auf Ihrem System vorhanden sein. Solch einen Codec erhalten Sie bspw. bei Nero (http://www.nero.com/eng/downloads-nerodigital-nero-aac-codec.php) unter Zustimmung der Lizenzvereinbarung. Dieser Codec muss vor der erstmaligen Verwendung einmalig installiert werden.

Gehen Sie dazu wie folgt vor:

1.    AAC Codec
downloaden.

2.    Dateien auf dem
Desktop entpacken.

3.    Den AAC-Decoder
in das Verzeichnis C:\Dokumente und Einstellungen\Anwendungsdate\Grundig
Business Systems\ kopieren.

(Wenn sie den AAC Decoder von Nero verwenden, ist befindet sich die Decoder
Datei (neroAacDec.exe) im Verzeichnis Win 32.)
