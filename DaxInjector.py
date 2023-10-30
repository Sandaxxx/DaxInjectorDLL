import os
import ctypes
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import customtkinter as ctk
import requests

files = {
    "C:\\DaxInjector\\bg1.png": 'https://github.com/Sandaxxx/DaxInjectorDLL/blob/main/bg1.png',
    "C:\\DaxInjector\\icon.ico": 'https://github.com/Sandaxxx/DaxInjectorDLL/blob/main/icon.ico'
}

for path, url in files.items():
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(requests.get(url).content)
            
class DLLInjectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DaxInjector")
        self.root.geometry("200x250")
        self.set_background()
        self.initUI()

    def set_background(self):
        image_path = "C:\\DaxInjector\\bg1.png"
        self.bg_image = ImageTk.PhotoImage(Image.open(image_path))
        bg_label = ctk.CTkLabel(self.root, text=" ", image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def initUI(self):
        self.label_red = ctk.CTkLabel(self.root, text="PID :")
        self.label_red.place(x=90, y=75)
        
        self.process_entry = ctk.CTkEntry(self.root, placeholder_text="   Enter Processus ID", fg_color="#000000", placeholder_text_color="#565B5E")
        self.process_entry.place(x=30, y=100)
        
        self.choose_dll_button = ctk.CTkButton(self.root, text="Select DLL", command=self.choose_dll, fg_color="#000000", border_color="#565B5E", border_width=2, text_color="#ffffff")
        self.choose_dll_button.place(x=30, y=150)

        self.inject_button = ctk.CTkButton(self.root, text="Inject DLL", command=self.inject_dll, fg_color="#39B404")
        self.inject_button.place(x=30, y=200)

    def choose_dll(self):
        file_name = filedialog.askopenfilename(filetypes=[("DLL Files", "*.dll"), ("All Files", "*.*")])
        if file_name:
            self.selected_dll = file_name





    def inject_dll(self):
        pid = int(self.process_entry.get())

        if hasattr(self, 'selected_dll') and self.selected_dll:
            result = self.inject_dll_code(self.selected_dll, pid)
            if result is True:
                messagebox.showinfo("Injection Status", f"Injected '{self.selected_dll}' into PID '{pid}' successfully.")
            else:
                messagebox.showerror("Injection Status", f"Failed to inject | PID '{pid}' |  Error: {result}")
        else:
            messagebox.showwarning("Injection Status", "Please choose a DLL file and a target PID.")





    def inject_dll_code(self, dll_path, pid):
        process_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, pid)
        if process_handle:
            dll_path = os.path.abspath(dll_path)
            kernel32 = ctypes.windll.kernel32
            kernel32.LoadLibraryW.restype = ctypes.c_void_p
            remote_dll = kernel32.LoadLibraryW(ctypes.c_wchar_p(dll_path))

            if remote_dll:
                ctypes.windll.kernel32.CloseHandle(process_handle)
                return True

        return False

def main():
    root = ctk.CTk()
    icon_path = "C:\\DaxInjector\\icon.ico"
    root.iconbitmap(icon_path)
    root.resizable(False, False)
    app = DLLInjectorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
