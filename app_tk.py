import tkinter as tk
from tkinter import ttk, messagebox
import threading

from tutor import ask_ai
from tts import speak

def run_in_thread(fn):
    def wrapper(*args, **kwargs):
        t = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
        t.start()
    return wrapper

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Language Tutor")
        self.geometry("720x520")
        self.minsize(680, 480)


        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Target language:").pack(side="left")
        self.lang_var = tk.StringVar(value="English")
        ttk.Entry(top, textvariable=self.lang_var, width=15).pack(side="left", padx=(6, 16))

        ttk.Label(top, text="Role:").pack(side="left")
        self.role_var = tk.StringVar(value="Tutor")
        ttk.Combobox(top, textvariable=self.role_var, values=["Tutor", "Pirate"], width=10, state="readonly").pack(side="left", padx=(6, 16))

        ttk.Label(top, text="TTS code:").pack(side="left")
        self.tts_lang_var = tk.StringVar(value="en")
        ttk.Entry(top, textvariable=self.tts_lang_var, width=6).pack(side="left", padx=(6, 16))

        self.tts_on = tk.BooleanVar(value=True)
        ttk.Checkbutton(top, text="Speak (TTS)", variable=self.tts_on).pack(side="left")

        mid = ttk.Frame(self, padding=(10, 0, 10, 10))
        mid.pack(fill="both", expand=False)

        ttk.Label(mid, text="Write a sentence:").pack(anchor="w", pady=(10, 4))
        self.input_text = tk.Text(mid, height=5, wrap="word")
        self.input_text.pack(fill="x")

        btns = ttk.Frame(mid)
        btns.pack(fill="x", pady=(8, 0))

        self.send_btn = ttk.Button(btns, text="Send", command=self.on_send)
        self.send_btn.pack(side="left")

        self.clear_btn = ttk.Button(btns, text="Clear", command=self.on_clear)
        self.clear_btn.pack(side="left", padx=8)

        out = ttk.Frame(self, padding=(10, 0, 10, 10))
        out.pack(fill="both", expand=True)

        ttk.Label(out, text="AI Feedback:").pack(anchor="w", pady=(10, 4))
        self.output_text = tk.Text(out, wrap="word")
        self.output_text.pack(fill="both", expand=True)

        self.status = tk.StringVar(value="Ready.")
        ttk.Label(self, textvariable=self.status, padding=10).pack(anchor="w")

    def on_clear(self):
        self.input_text.delete("1.0", "end")

    def on_send(self):
        user = self.input_text.get("1.0", "end").strip()
        if not user:
            messagebox.showinfo("Info", "Please write a sentence first.")
            return

        self.send_btn.config(state="disabled")
        self.status.set("Thinking...")

        try:
            role = self.role_var.get()
            lang = self.lang_var.get().strip() or "English"
            answer = ask_ai(user_text=user, role=role, lang_name=lang)

            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", answer)

            self.status.set("Done.")

            if self.tts_on.get():
                try:
                    speak(answer[:500], lang=self.tts_lang_var.get().strip() or "en")
                except Exception as e:
        
                    self.status.set(f"Done (TTS failed: {e})")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.set("Error.")
        finally:
            self.send_btn.config(state="normal")

if __name__ == "__main__":
    App().mainloop()
