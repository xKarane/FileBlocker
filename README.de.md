# Datei Blocker

Ein leistungsstarkes Windows-Tool, das das Ausführen von Programmen durch Änderung der Image File Execution Options in der Windows-Registry blockiert oder wieder erlaubt. Dieses Tool bietet eine benutzerfreundliche Oberfläche zur Verwaltung, welche Anwendungen auf Ihrem System ausgeführt werden dürfen.

## Funktionen
- 🛑 Blockieren von ausführbaren Dateien nach Dateiname
- ✅ Aufheben der Blockierung
- 🔍 Überprüfung, ob eine Datei aktuell blockiert ist
- 🎨 Moderne, intuitive Benutzeroberfläche
- ⚡ Schnelle Bedienung mit Tastatur (Enter zum Ausführen)
- 🚀 Keine Installation erforderlich (portable Exe)

## Systemanforderungen
- Windows 7/8/10/11 (64-bit empfohlen)
- Administratorrechte (für Registry-Änderungen erforderlich)

## Funktionsweise
Das Programm erstellt oder ändert Registrierungsschlüssel unter:
```
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\[dateiname.exe]
```
Beim Blockieren wird ein Debugger-Wert gesetzt, der das Ausführen verhindert.

## Verwendung
1. Laden Sie die neueste Version von der [Releases](https://github.com/xKarane/FileBlocker/releases) Seite herunter
2. Rechtsklick auf `FileBlocker.exe` und "Als Administrator ausführen" wählen
3. Geben Sie den Dateinamen ein, den Sie blockieren/freigeben möchten (z. B. `notepad.exe`)
4. Aktion auswählen (Blockieren/Freigeben)
5. Auf "Ausführen" klicken oder Enter drücken
6. Der Status zeigt das Ergebnis an

## Lizenz
Dieses Projekt steht unter der MIT-Lizenz – siehe [LICENSE](LICENSE) für Details.
