import os
import sys
try:
    import docx
except ImportError:
    docx = None
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pyttsx3
import multiprocessing

def read_docx(file_path):
    if not docx:
        messagebox.showerror("Missing Dependency", "python-docx is not installed. Please install it to read .docx files.")
        sys.exit(1)
    doc = docx.Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def get_text_from_file(filepath):
    if not os.path.isfile(filepath):
        messagebox.showerror("File Not Found", f"File '{filepath}' not found.")
        return None
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext == '.txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        elif ext in ['.doc', '.docx']:
            return read_docx(filepath)
        else:
            messagebox.showerror("Unsupported File", "Only .txt, .doc, or .docx files are supported.")
            return None
    except Exception as e:
        messagebox.showerror("Read Error", f"Error reading file: {e}")
        return None

def speak_text(text, rate, voice_id):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    if voice_id:
        engine.setProperty('voice', voice_id)
    engine.say(text)
    engine.runAndWait()

def open_file_dialog(entry):
    filepath = filedialog.askopenfilename(
        title="Select a text or Word file",
        filetypes=[("Text and Word Files", "*.txt *.doc *.docx"), ("All Files", "*.*")]
    )
    if filepath:
        entry.delete(0, tk.END)
        entry.insert(0, filepath)

def start_tts(entry, rate_scale, voice_var, start_btn, stop_btn, tts_proc_holder):
    filepath = entry.get().strip()
    try:
        rate = int(rate_scale.get())
    except Exception:
        rate = 200
    if not filepath:
        messagebox.showwarning("No File", "Please select a file.")
        return
    text = get_text_from_file(filepath)
    if not text:
        return
    voice_id = voice_var.get()
    # If a process is already running, stop it first
    if tts_proc_holder['proc'] is not None and tts_proc_holder['proc'].is_alive():
        tts_proc_holder['proc'].terminate()
        tts_proc_holder['proc'].join()
    proc = multiprocessing.Process(target=speak_text, args=(text, rate, voice_id))
    tts_proc_holder['proc'] = proc
    proc.start()
    start_btn.config(state='disabled')
    stop_btn.config(state='normal')
    def check_proc():
        if proc.is_alive():
            start_btn.after(200, check_proc)
        else:
            start_btn.config(state='normal')
            stop_btn.config(state='disabled')
    start_btn.after(200, check_proc)

def stop_tts(start_btn, stop_btn, tts_proc_holder):
    proc = tts_proc_holder['proc']
    if proc is not None and proc.is_alive():
        proc.terminate()
        proc.join()
    start_btn.config(state='normal')
    stop_btn.config(state='disabled')

def populate_voices(voice_combo, voice_var):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice_names = [f"{v.name} ({v.id})" for v in voices]
    voice_ids = [v.id for v in voices]
    voice_combo['values'] = voice_names
    if voice_names:
        voice_combo.current(0)
        voice_var.set(voice_ids[0])
    def on_select(event):
        idx = voice_combo.current()
        if 0 <= idx < len(voice_ids):
            voice_var.set(voice_ids[idx])
    voice_combo.bind('<<ComboboxSelected>>', on_select)

def main():
    multiprocessing.set_start_method('spawn')
    root = tk.Tk()
    root.title("Safe Text-to-Speech Tool (pyttsx3)")
    root.geometry("500x290")
    root.resizable(False, False)

    # File selection
    tk.Label(root, text="File:").pack(pady=(15, 0))
    file_frame = tk.Frame(root)
    file_frame.pack(pady=2)
    file_entry = tk.Entry(file_frame, width=40)
    file_entry.pack(side=tk.LEFT, padx=(0, 5))
    tk.Button(file_frame, text="Browse...", command=lambda: open_file_dialog(file_entry)).pack(side=tk.LEFT)

    # Speech rate
    tk.Label(root, text="Speech Rate (words per minute):").pack(pady=(15, 0))
    rate_scale = tk.Scale(root, from_=100, to=300, orient=tk.HORIZONTAL)
    rate_scale.set(200)
    rate_scale.pack()

    # Voice selection
    tk.Label(root, text="Voice:").pack(pady=(15, 0))
    voice_var = tk.StringVar()
    voice_combo = ttk.Combobox(root, width=50, state="readonly")
    voice_combo.pack(pady=2)
    populate_voices(voice_combo, voice_var)

    # Start and Stop buttons
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=15)
    tts_proc_holder = {'proc': None}
    start_btn = tk.Button(btn_frame, text="Start TTS", command=lambda: start_tts(file_entry, rate_scale, voice_var, start_btn, stop_btn, tts_proc_holder))
    start_btn.pack(side=tk.RIGHT)
    stop_btn = tk.Button(btn_frame, text="Stop", state='disabled', command=lambda: stop_tts(start_btn, stop_btn, tts_proc_holder))
    stop_btn.pack(side=tk.RIGHT, padx=10)

    root.mainloop()

if __name__ == '__main__':
    main() 