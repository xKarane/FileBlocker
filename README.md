# File Blocker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**File Blocker** is a user-friendly Windows utility that lets you block or unblock executable files by managing the Windows Registry. It features a modern GUI, supports English and German, and includes in-app documentation. Ideal for administrators and power users who want to control which applications can run on their system.

A powerful Windows utility that blocks or unblocks executables from running by modifying the Windows Registry's Image File Execution Options. This tool provides a user-friendly interface to manage which applications can be executed on your system.

## Features
- 🛑 Block executables by filename
- ✅ Unblock previously blocked executables
- 🔍 Check if a file is currently blocked
- 🎨 Modern and intuitive user interface
- ⚡ Quick action with keyboard support (press Enter to execute)
- 🚀 No installation required (portable executable)

## System Requirements
- Windows 7/8/10/11 (64-bit recommended)
- Administrator privileges (required for registry modification)
- .NET Framework 4.5 or later

## How It Works
The application works by creating or modifying registry keys under:
```
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\[filename.exe]
```
When a file is blocked, it sets a debugger value that prevents the application from running.

## Usage
1. Download the latest release from the [Releases](https://github.com/xKarane/FileBlocker/releases) page
2. Right-click on `FileBlocker.exe` and select "Run as Administrator"
3. Enter the filename you want to block/unblock (e.g., `notepad.exe`)
4. Select the desired action (Block/Unblock)
5. Click "Execute" or press Enter
6. The status will update to show the result of the operation

## Command Line Usage
You can also use the application from the command line:
```
FileBlocker.exe [filename] [block|unblock]
```
Example:
```
FileBlocker.exe notepad.exe block
```

## Building from Source
1. Install Python 3.8 or later
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Build the executable:
   ```
   pyinstaller --onefile --windowed --icon=assets/icon.ico file_blocker.py
   ```

## Security Notes
- Always verify the source of any executable before running it
- The application requires Administrator privileges to modify the registry
- Some system-protected files might still be executable due to Windows security features
- The application creates a backup of the registry before making changes

## Troubleshooting
- If you get an "Access Denied" error, make sure to run the application as Administrator
- If a file is still running after blocking, try restarting your computer
- Some antivirus programs might interfere with the blocking mechanism

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
