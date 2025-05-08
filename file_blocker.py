import tkinter as tk
from tkinter import ttk, messagebox
import winreg
import os
import sys
import ctypes
import webbrowser
import locale
from pathlib import Path

class FileBlockerApp:
    def __init__(self, root):
        self.root = root
        
        # Initialize translations
        self.translations = {
            'en': {
                'title': 'File Blocker',
                'file_label': 'Executable filename:',
                'registry_path': 'Registry path:',
                'status_enter': 'Status: Enter a filename',
                'status_blocked': 'Status: This file is currently BLOCKED',
                'status_not_blocked': 'Status: This file is currently NOT blocked',
                'status_check_error': 'Status: Could not check status',
                'block_btn': 'Block File',
                'unblock_btn': 'Unblock File',
                'check_status': 'Check Status',
                'block_unblock': 'File to Block/Unblock',
                'readme': 'Readme',
                'language': 'Language',
                'error_file': 'Please enter a filename',
                'success_block': 'Successfully blocked: {}',
                'success_unblock': 'Successfully unblocked: {}',
                'error_occurred': 'An error occurred',
                'readme_not_found': 'Readme file not found'
            },
            'de': {
                'title': 'Datei Blocker',
                'file_label': 'Ausführbare Datei:',
                'registry_path': 'Registrierungspfad:',
                'status_enter': 'Status: Dateinamen eingeben',
                'status_blocked': 'Status: Diese Datei ist aktuell GEBLOCKT',
                'status_not_blocked': 'Status: Diese Datei ist aktuell NICHT geblockt',
                'status_check_error': 'Status: Status konnte nicht überprüft werden',
                'block_btn': 'Datei blockieren',
                'unblock_btn': 'Blockierung aufheben',
                'check_status': 'Status prüfen',
                'block_unblock': 'Datei blockieren/freigeben',
                'readme': 'Anleitung',
                'language': 'Sprache',
                'error_file': 'Bitte geben Sie einen Dateinamen ein',
                'success_block': 'Erfolgreich geblockt: {}',
                'success_unblock': 'Blockierung aufgehoben: {}',
                'error_occurred': 'Ein Fehler ist aufgetreten',
                'readme_not_found': 'Anleitung nicht gefunden'
            }
        }
        
        # Set language based on system default
        self.current_lang = 'de' if locale.getdefaultlocale()[0].startswith('de') else 'en'
        
        self.root.title(self.translations[self.current_lang]['title'])
        
        # Set fixed window size and prevent resizing
        self.root.geometry("400x300")  # Compact window size
        self.root.minsize(400, 300)  # Minimum size to ensure everything fits
        self.root.resizable(False, False)  # Disable resizing in both directions
        
        # Create main frame with less padding
        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create top frame for buttons
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Add language button
        # Add language button
        lang_btn = ttk.Menubutton(top_frame, text=self.translations[self.current_lang]['language'])
        lang_menu = tk.Menu(lang_btn, tearoff=0)
        lang_menu.add_command(label='English', command=lambda: self.change_language('en'))
        lang_menu.add_command(label='Deutsch', command=lambda: self.change_language('de'))
        lang_btn['menu'] = lang_menu
        lang_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Add Readme button
        readme_btn = ttk.Button(top_frame, 
                              text=self.translations[self.current_lang]['readme'],
                              command=self.open_readme)
        readme_btn.pack(side=tk.LEFT)
        
        # File selection
        input_frame = ttk.LabelFrame(main_frame, text=f" {self.translations[self.current_lang]['block_unblock']} ")
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Filename input
        self.file_label = ttk.Label(input_frame, text=self.translations[self.current_lang]['file_label'])
        self.file_label.pack(anchor='w', pady=(0, 5))
        
        entry_frame = ttk.Frame(input_frame)
        entry_frame.pack(fill=tk.X, pady=5)
        
        self.file_path = tk.StringVar()
        self.file_path.trace('w', self.update_registry_info)  # Add trace on variable change
        file_entry = ttk.Entry(entry_frame, textvariable=self.file_path, font=('Segoe UI', 10))
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Registry path display with better wrapping
        self.registry_path = ttk.Label(
            input_frame,
            text=f"{self.translations[self.current_lang]['registry_path']} ",
            foreground='#666666',
            font=('Consolas', 7),  # Smaller font
            anchor='w',
            wraplength=350  # Adjusted for narrower window
        )
        self.registry_path.pack(fill=tk.X, pady=(3, 1), padx=2)  # Tighter spacing
        
        # File status display
        self.file_status = ttk.Label(
            input_frame,
            text=self.translations[self.current_lang]['status_enter'],
            font=('Segoe UI', 9, 'italic'),
            anchor='w'
        )
        self.file_status.pack(fill=tk.X, pady=(0, 5))
        
        # Action button (dynamically changes based on current state)
        self.action_btn = ttk.Button(
            main_frame, 
            text=self.translations[self.current_lang]['check_status'], 
            command=self.execute_action,
            style='Accent.TButton',
            padding=3
        )
        self.action_btn.pack(fill=tk.X, pady=5)
        
        # Bind Enter key to execute action
        file_entry.bind('<Return>', lambda e: self.execute_action())
        
        # Set focus to entry field
        file_entry.focus()
        
        # Status label with smaller font and minimal padding
        self.status_label = ttk.Label(main_frame, text="", wraplength=380, font=('Segoe UI', 8))
        self.status_label.pack(fill=tk.X, pady=(3, 0))
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        
        # Make the entry widget expand with window
        main_frame.rowconfigure(5, weight=1)
    
    def update_registry_info(self, *args):
        """Update the registry path and status when filename changes"""
        filename = self.file_path.get().strip()
        if not filename:
            self.registry_path.config(text=f"{self.translations[self.current_lang]['registry_path']} ")
            self.file_status.config(text=self.translations[self.current_lang]['status_enter'])
            self.action_btn.config(text=self.translations[self.current_lang]['check_status'], state='disabled')
            return
            
        # Update registry path
        reg_path = f"HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\{filename}"
        self.registry_path.config(text=f"{self.translations[self.current_lang]['registry_path']} {reg_path}")
        
        # Update status and action button
        try:
            if self.is_file_blocked(filename):
                self.file_status.config(
                    text=self.translations[self.current_lang]['status_blocked'], 
                    foreground='#e74c3c'
                )
                self.action_btn.config(
                    text=self.translations[self.current_lang]['unblock_btn'], 
                    state='normal'
                )
            else:
                self.file_status.config(
                    text=self.translations[self.current_lang]['status_not_blocked'], 
                    foreground='#2ecc71'
                )
                self.action_btn.config(
                    text=self.translations[self.current_lang]['block_btn'], 
                    state='normal'
                )
        except Exception:
            self.file_status.config(
                text=self.translations[self.current_lang]['status_check_error'], 
                foreground='#f39c3c'
            )
            self.action_btn.config(
                text=self.translations[self.current_lang]['check_status'], 
                state='disabled'
            )

    def change_language(self, lang):
        """Change the application language and update all UI text instantly (no layout change)"""
        if lang in self.translations and lang != self.current_lang:
            self.current_lang = lang
            tr = self.translations[self.current_lang]
            self.root.title(tr['title'])
            self.file_label.config(text=tr['file_label'])
            # Update input frame label (LabelFrame)
            input_frame = self.file_label.master.master
            input_frame.config(text=f" {tr['block_unblock']} ")
            self.registry_path.config(text=f"{tr['registry_path']} ")
            # Find and update language button and readme button if present
            for child in self.file_label.master.master.master.winfo_children():
                if isinstance(child, type(self.file_label.master.master.master.children['!frame'])):
                    for btn in child.winfo_children():
                        if hasattr(btn, 'config') and btn.cget('text') in [self.translations['en']['language'], self.translations['de']['language']]:
                            btn.config(text=tr['language'])
                        if hasattr(btn, 'config') and btn.cget('text') in [self.translations['en']['readme'], self.translations['de']['readme']]:
                            btn.config(text=tr['readme'])
            # Update action button and status
            filename = self.file_path.get().strip()
            if not filename:
                self.file_status.config(text=tr['status_enter'])
                self.action_btn.config(text=tr['check_status'], state='disabled')
            else:
                self.update_registry_info()  # This will update the UI with new translations
            
    def open_readme(self):
        """Open the README file in a new Tkinter window (supports German/English, script and bundled exe)"""
        import sys
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        # Choose README file based on language
        if self.current_lang == 'de':
            readme_filename = 'README.de.md'
        else:
            readme_filename = 'README.md'
        readme_path = os.path.join(base_path, readme_filename)
        if not os.path.exists(readme_path):
            messagebox.showerror(
                "Error",
                self.translations[self.current_lang]['readme_not_found']
            )
            return
        try:
            with open(readme_path, encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open README: {str(e)}")
            return
        # Create a new window
        readme_win = tk.Toplevel(self.root)
        readme_win.title(self.translations[self.current_lang]['readme'])
        readme_win.geometry('600x500')
        readme_win.minsize(400, 300)
        # Add a scrollable Text widget
        text = tk.Text(readme_win, wrap='word', font=('Consolas', 10), state='normal')
        text.insert('1.0', content)
        text.config(state='disabled')
        text.pack(fill='both', expand=True, padx=10, pady=10)
        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(readme_win, command=text.yview)
        text['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side='right', fill='y')
        # Focus the window
        readme_win.focus_set()
    
    def show_success(self, message):
        """Show a success message"""
        self.status_label.config(text=message, foreground='#2ecc71')
        
    def show_error(self, message):
        """Show an error message"""
        self.status_label.config(text=message, foreground='#e74c3c')
        
    def show_info(self, message):
        """Show an info message"""
        self.status_label.config(text=message, foreground='#3498db')

    def execute_action(self, event=None):
        file_path = self.file_path.get().strip()
        
        if not file_path:
            self.show_error(self.translations[self.current_lang]['error_file'])
            return
        
        # Disable button during operation
        self.action_btn.config(state='disabled')
        self.root.update()
        
        try:
            if self.is_file_blocked(file_path):
                self.unblock_file(file_path)
                self.show_success(self.translations[self.current_lang]['success_unblock'].format(os.path.basename(file_path)))
            else:
                self.block_file(file_path)
                self.show_success(self.translations[self.current_lang]['success_block'].format(os.path.basename(file_path)))
            
            # Update status after action
            self.update_registry_info()
            
        except Exception as e:
            self.show_error(f"{self.translations[self.current_lang]['error_occurred']}: {str(e)}")
            self.update_registry_info()  # Reset UI state on error
    
    def block_file(self, file_path):
        try:
            # Get just the filename without path
            filename_only = Path(file_path).name
            
            # Create the Image File Execution Options key for this executable
            key_path = fr"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\{filename_only}"
            
            # Open or create the registry key
            key = winreg.CreateKeyEx(
                winreg.HKEY_LOCAL_MACHINE,
                key_path,
                0,
                winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY
            )
            
            try:
                # Set the debugger to a non-existent program
                winreg.SetValueEx(
                    key,
                    "Debugger",
                    0,
                    winreg.REG_SZ,
                    "ntsd -d"  # This will prevent the program from running
                )
            finally:
                winreg.CloseKey(key)
                
        except Exception as e:
            raise Exception(f"Failed to block file: {str(e)}")
    
    def is_file_blocked(self, file_path):
        """Check if a file is currently blocked"""
        try:
            filename_only = Path(file_path).name
            key_path = fr"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\{filename_only}"
            
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    key_path,
                    0,
                    winreg.KEY_READ | winreg.KEY_WOW64_64KEY
                )
                
                try:
                    # Check if the Debugger value exists
                    winreg.QueryValueEx(key, "Debugger")
                    return True
                except WindowsError:
                    return False
                finally:
                    winreg.CloseKey(key)
                    
            except WindowsError as e:
                if e.winerror == 2:  # Key not found
                    return False
                raise
                
        except Exception as e:
            raise Exception(f"Failed to check if file is blocked: {str(e)}")
    
    def unblock_file(self, file_path):
        try:
            filename_only = Path(file_path).name
            key_path = fr"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\{filename_only}"
            
            # First check if the key exists
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    key_path,
                    0,
                    winreg.KEY_READ | winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY
                )
                winreg.CloseKey(key)
                
                # If we got here, the key exists, so delete it
                winreg.DeleteKeyEx(
                    winreg.HKEY_LOCAL_MACHINE,
                    key_path,
                    winreg.KEY_WOW64_64KEY,
                    0
                )
                
            except WindowsError as e:
                if e.winerror == 2:  # Key not found
                    return  # Nothing to unblock
                raise
                
        except Exception as e:
            raise Exception(f"Failed to unblock file: {str(e)}")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    # Try to set DPI awareness for better display on high-DPI screens
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    root = tk.Tk()
    
    # Set window icon if available
    try:
        root.iconbitmap(default='icon.ico')
    except:
        pass
    
    app = FileBlockerApp(root)
    
    # Center the window
    window_width = 500
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    # Run with elevated privileges if not already
    if not is_admin():
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " \"" + sys.argv[0] + "\"", None, 1)
        sys.exit(0)
    
    try:
        main()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}\n\nPlease make sure to run this program as Administrator.")
        sys.exit(1)
