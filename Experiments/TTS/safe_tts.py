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
import tempfile
try:
    from pydub import AudioSegment  # type: ignore  # May not be installed
except ImportError:
    AudioSegment = None

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

def speak_text(text, rate, voice_id, save_path=None):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    if voice_id:
        engine.setProperty('voice', voice_id)
    if save_path:
        # Save to temporary WAV, then convert to MP3
        if not AudioSegment:
            messagebox.showerror("Missing Dependency", "pydub is not installed. Please install it to save as MP3.")
            return
        try:
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_wav:
                tmp_wav_path = tmp_wav.name
            engine.save_to_file(text, tmp_wav_path)
            engine.runAndWait()
            # Convert to MP3
            audio = AudioSegment.from_wav(tmp_wav_path)
            audio.export(save_path, format="mp3")
            os.remove(tmp_wav_path)
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving MP3: {e}")
    else:
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

def start_tts(entry, rate_scale, voice_var, start_btn, stop_btn, tts_proc_holder, save_var, save_path_holder):
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
    save_path = None
    if save_var.get():
        save_path = save_path_holder['path']
        if not save_path:
            messagebox.showwarning("No Save Path", "Please select a location to save the MP3 file.")
            return
    # If a process is already running, stop it first
    if tts_proc_holder['proc'] is not None and tts_proc_holder['proc'].is_alive():
        tts_proc_holder['proc'].terminate()
        tts_proc_holder['proc'].join()
    proc = multiprocessing.Process(target=speak_text, args=(text, rate, voice_id, save_path))
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
    root.geometry("500x340")
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

    # Save to MP3 option
    save_var = tk.BooleanVar()
    save_path_holder = {'path': ''}  # Use empty string to avoid linter error
    def choose_save_path():
        path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if path:
            save_path_holder['path'] = path
    save_frame = tk.Frame(root)
    save_frame.pack(pady=(10, 0))
    save_check = tk.Checkbutton(save_frame, text="Save speech to MP3", variable=save_var)
    save_check.pack(side=tk.LEFT)
    save_btn = tk.Button(save_frame, text="Choose location...", command=choose_save_path)
    save_btn.pack(side=tk.LEFT, padx=5)

    # Start and Stop buttons
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=15)
    tts_proc_holder = {'proc': None}
    start_btn = tk.Button(btn_frame, text="Start TTS", command=lambda: start_tts(file_entry, rate_scale, voice_var, start_btn, stop_btn, tts_proc_holder, save_var, save_path_holder))
    start_btn.pack(side=tk.RIGHT)
    stop_btn = tk.Button(btn_frame, text="Stop", state='disabled', command=lambda: stop_tts(start_btn, stop_btn, tts_proc_holder))
    stop_btn.pack(side=tk.RIGHT, padx=10)

    root.mainloop()

if __name__ == '__main__':
    main() 