import tkinter as tk
from tkinter import filedialog, messagebox
import base64
import os
import shutil
from cryptography.fernet import Fernet

# --- CYBERSECURITY THEME PALETTE ---
CB_BG = "#0A0B10"        # Deep Space Black
CB_CARD = "#161B22"      # GitHub Dark Grey
CB_ACCENT = "#00F2FF"    # Neon Cyan
CB_TEXT = "#E6EDF3"      # Off White
CB_MUTED = "#8B949E"     # Steel Grey
CB_DANGER = "#FF3E3E"    # Alert Red

class CryptoEngine:
    KEY_FILE = "master.key"

    @classmethod
    def get_key(cls):
        if os.path.exists(cls.KEY_FILE):
            with open(cls.KEY_FILE, "rb") as kf: return kf.read()
        key = Fernet.generate_key()
        with open(cls.KEY_FILE, "wb") as kf: kf.write(key)
        return key

    @staticmethod
    def backup_key():
        if not os.path.exists(CryptoEngine.KEY_FILE): return False, "No key found."
        dest = filedialog.asksaveasfilename(defaultextension=".key", title="Export Master Key")
        if dest:
            shutil.copy2(CryptoEngine.KEY_FILE, dest)
            return True, dest
        return False, "Cancelled"

    @staticmethod
    def restore_key():
        src = filedialog.askopenfilename(title="Select Backup Key", filetypes=[("Key files", "*.key *.bak")])
        if src:
            shutil.copy2(src, CryptoEngine.KEY_FILE)
            return True
        return False

class CyberVaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CYBER-VAULT v4.0 // SECURE NODE")
        self.root.geometry("950x650")
        self.root.configure(bg=CB_BG)
        self.mode = "text"

        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        self.root.option_add("*Font", "Consolas 11")

    def build_ui(self):
        # --- LEFT NAVIGATION (SIDEBAR) ---
        self.sidebar = tk.Frame(self.root, bg=CB_CARD, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo/Title
        tk.Label(self.sidebar, text="[◢] VAULT_SYS", fg=CB_ACCENT, bg=CB_CARD, 
                 font=("Consolas", 16, "bold")).pack(pady=40)

        # Nav Buttons
        self.create_nav_btn("▣ TEXT_ENCRYPT", lambda: self.switch_view("text"))
        self.create_nav_btn("📁 FILE_VAULT", lambda: self.switch_view("file"))
        
        # Key Ops Section
        tk.Label(self.sidebar, text="KEY MANAGEMENT", fg=CB_MUTED, bg=CB_CARD, 
                 font=("Consolas", 8, "bold")).pack(pady=(50, 10))
        self.create_nav_btn("💾 EXPORT KEY", self.export_logic)
        self.create_nav_btn("🔄 RESTORE KEY", self.restore_logic)

        # --- MAIN WORKSPACE ---
        self.workspace = tk.Frame(self.root, bg=CB_BG)
        self.workspace.pack(side="right", expand=True, fill="both", padx=40, pady=30)

        # Terminal Header
        self.header_lbl = tk.Label(self.workspace, text="LOG::READY_FOR_INPUT", fg=CB_ACCENT, 
                                  bg=CB_BG, font=("Consolas", 14, "bold"))
        self.header_lbl.pack(anchor="w", pady=(0, 20))

        # Text Input (Cyber Style)
        self.text_frame = tk.Frame(self.workspace, bg=CB_ACCENT, padx=1, pady=1) # Border effect
        self.text_frame.pack(fill="both", expand=True)
        self.input_box = tk.Text(self.text_frame, bg=CB_BG, fg=CB_TEXT, insertbackground=CB_ACCENT,
                                 relief="flat", borderwidth=10, font=("Consolas", 11))
        self.input_box.pack(fill="both", expand=True)

        # File View (Hidden)
        self.file_view = tk.Frame(self.workspace, bg=CB_BG)
        self.file_label = tk.Label(self.file_view, text="NO_FILE_TARGETED", fg=CB_DANGER, 
                                   bg=CB_BG, font=("Consolas", 12))
        self.file_label.pack(pady=20)
        tk.Button(self.file_view, text="SELECT TARGET FILE", command=self.pick_file, 
                  bg=CB_CARD, fg=CB_ACCENT, relief="flat", padx=20, pady=10).pack()

        # Command Controls
        self.ctrl_frame = tk.Frame(self.workspace, bg=CB_BG)
        self.ctrl_frame.pack(fill="x", pady=30)

        self.btn_enc = tk.Button(self.ctrl_frame, text="EXECUTE_ENCRYPT", command=self.run_enc,
                                 bg=CB_ACCENT, fg=CB_BG, font=("Consolas", 10, "bold"), 
                                 relief="flat", padx=25, pady=12)
        self.btn_enc.pack(side="left", padx=(0, 15))

        self.btn_dec = tk.Button(self.ctrl_frame, text="EXECUTE_DECRYPT", command=self.run_dec,
                                 bg=CB_CARD, fg=CB_ACCENT, font=("Consolas", 10, "bold"), 
                                 relief="flat", padx=25, pady=12)
        self.btn_dec.pack(side="left")

        # Bottom Status
        self.status_lbl = tk.Label(self.root, text="SYSTEM::STABLE", bg=CB_CARD, 
                                   fg=CB_MUTED, anchor="w", padx=15, pady=5)
        self.status_lbl.pack(side="bottom", fill="x")

    def create_nav_btn(self, label, cmd):
        btn = tk.Button(self.sidebar, text=label, command=cmd, bg=CB_CARD, fg=CB_TEXT,
                       relief="flat", anchor="w", padx=25, pady=12, font=("Consolas", 10))
        btn.pack(fill="x")
        btn.bind("<Enter>", lambda e: btn.config(bg="#1C2128", fg=CB_ACCENT))
        btn.bind("<Leave>", lambda e: btn.config(bg=CB_CARD, fg=CB_TEXT))

    def switch_view(self, mode):
        self.mode = mode
        if mode == "text":
            self.file_view.pack_forget()
            self.text_frame.pack(fill="both", expand=True)
            self.header_lbl.config(text="LOG::TEXT_STREAM_ACTIVE")
        else:
            self.text_frame.pack_forget()
            self.file_view.pack(fill="both", expand=True)
            self.header_lbl.config(text="LOG::FILE_VAULT_ACTIVE")

    def pick_file(self):
        p = filedialog.askopenfilename()
        if p:
            self.target_path = p
            self.file_label.config(text=f"TARGET: {os.path.basename(p)}", fg=CB_ACCENT)

    def export_logic(self):
        s, m = CryptoEngine.backup_key()
        if s: messagebox.showinfo("VAULT", f"Key Exported: {m}")

    def restore_logic(self):
        if CryptoEngine.restore_key():
            messagebox.showinfo("VAULT", "Master Key Restored. System Reboot Recommended.")
        
    def run_enc(self):
        self.status_lbl.config(text="SYSTEM::ENCRYPTING...", fg=CB_ACCENT)
        self.root.after(600, self._enc_process)

    def _enc_process(self):
        try:
            if self.mode == "text":
                raw = self.input_box.get("1.0", tk.END).strip().encode()
                res = Fernet(CryptoEngine.get_key()).encrypt(raw)
                self.input_box.delete("1.0", tk.END)
                self.input_box.insert("1.0", res.decode())
            else:
                with open(self.target_path, "rb") as f: data = f.read()
                res = Fernet(CryptoEngine.get_key()).encrypt(data)
                with open(self.target_path + ".enc", "wb") as f: f.write(res)
                messagebox.showinfo("SUCCESS", "Encrypted file generated.")
            self.status_lbl.config(text="SYSTEM::TASK_COMPLETE", fg=CB_ACCENT)
        except Exception as e:
            messagebox.showerror("CRITICAL_ERROR", str(e))

    def run_dec(self):
        self.status_lbl.config(text="SYSTEM::DECRYPTING...", fg=CB_ACCENT)
        self.root.after(600, self._dec_process)

    def _dec_process(self):
        try:
            if self.mode == "text":
                raw = self.input_box.get("1.0", tk.END).strip().encode()
                res = Fernet(CryptoEngine.get_key()).decrypt(raw)
                self.input_box.delete("1.0", tk.END)
                self.input_box.insert("1.0", res.decode())
            else:
                with open(self.target_path, "rb") as f: data = f.read()
                res = Fernet(CryptoEngine.get_key()).decrypt(data)
                out = filedialog.asksaveasfilename(title="Save Restored File")
                if out: 
                    with open(out, "wb") as f: f.write(res)
            self.status_lbl.config(text="SYSTEM::TASK_COMPLETE", fg=CB_ACCENT)
        except Exception:
            messagebox.showerror("AUTH_FAILURE", "Invalid Key or Corrupted Data")

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberVaultApp(root)
    root.mainloop()
