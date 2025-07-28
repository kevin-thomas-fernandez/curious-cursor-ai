import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# Create the directory
tool_dir = 'csv_to_xlsx_tool'
os.makedirs(tool_dir, exist_ok=True)

def convert_csv_to_xlsx():
    # Open file dialog
    file_paths = filedialog.askopenfilenames(
        title="Select CSV file(s) to convert",
        filetypes=[("CSV Files", "*.csv")]
    )

    if not file_paths:
        return

    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path)
            new_file = file_path.rsplit(".", 1)[0] + ".xlsx"
            df.to_excel(new_file, index=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert {file_path}:\n{e}")
            continue

    messagebox.showinfo("Success", "Conversion complete!")



def compare_csv_and_xlsx():
    csv_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
    if not csv_path:
        return

    xlsx_path = filedialog.askopenfilename(title="Select XLSX File", filetypes=[("Excel Files", "*.xlsx")])
    if not xlsx_path:
        return

    try:
        df_csv = pd.read_csv(csv_path)
        df_xlsx = pd.read_excel(xlsx_path)

        # Standardize column order and sort if needed
        df_csv = df_csv[df_xlsx.columns] if list(df_csv.columns) == list(df_xlsx.columns) else df_csv
        df_csv = df_csv.reset_index(drop=True)
        df_xlsx = df_xlsx.reset_index(drop=True)

        if df_csv.equals(df_xlsx):
            messagebox.showinfo("Match", "CSV and XLSX files match exactly.")
        else:
            # Compare row by row
            mismatch_rows = []
            min_len = min(len(df_csv), len(df_xlsx))
            for i in range(min_len):
                if not df_csv.iloc[i].equals(df_xlsx.iloc[i]):
                    mismatch_rows.append(i + 1)  # 1-based indexing

            # If lengths differ, add the extra rows
            if len(df_csv) != len(df_xlsx):
                mismatch_rows.extend(range(min_len + 1, max(len(df_csv), len(df_xlsx)) + 1))

            mismatch_message = "Files do not match.\nMismatched row(s):\n" + ', '.join(map(str, mismatch_rows))
            messagebox.showwarning("Mismatch", mismatch_message)

    except Exception as e:
        messagebox.showerror("Error", f"Comparison failed:\n{e}")

# GUI setup
root = tk.Tk()
root.title("CSV to XLSX Tool")
root.geometry("350x200")

label = tk.Label(root, text="Choose an action below", pady=15)
label.pack()

convert_button = tk.Button(root, text="Convert CSV to XLSX", command=convert_csv_to_xlsx)
convert_button.pack(pady=5)

compare_button = tk.Button(root, text="Compare CSV and XLSX", command=compare_csv_and_xlsx)
compare_button.pack(pady=5)

root.mainloop()
