import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import sqlite3

def save_program(name, purpose, target, due):
    conn = sqlite3.connect("contribution.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO programs (name, purpose, target, due)
        VALUES (?, ?, ?, ?)
    """, (name, purpose, float(target), due))
    conn.commit()
    conn.close()

def load_programs():
    conn = sqlite3.connect("contribution.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, purpose, target, due FROM programs")
    for r in cursor.fetchall():
        add_program_to_list(r[0], r[1], str(r[2]), r[3])
    conn.close()

def open_contribution_window():
    contrib_window = tk.Toplevel(root)
    contrib_window.title("Create Contribution Program")
    contrib_window.geometry("400x300")

    tk.Label(contrib_window, text="Program Name:").pack(anchor="w", padx=10, pady=5)
    entry_name = tk.Entry(contrib_window, width=40)
    entry_name.pack(padx=10)

    tk.Label(contrib_window, text="Purpose:").pack(anchor="w", padx=10, pady=5)
    entry_purpose = tk.Entry(contrib_window, width=40)
    entry_purpose.pack(padx=10)

    tk.Label(contrib_window, text="Target Amount:").pack(anchor="w", padx=10, pady=5)
    entry_target = tk.Entry(contrib_window, width=40)
    entry_target.pack(padx=10)

    tk.Label(contrib_window, text="Due Date:").pack(anchor="w", padx=10, pady=5)
    entry_due = tk.Entry(contrib_window, width=40)
    entry_due.pack(padx=10)

    def submit_info():
        name = entry_name.get().strip()
        purpose = entry_purpose.get().strip()
        target = entry_target.get().strip().replace(",", "")
        due = entry_due.get().strip()

        if not name:
            messagebox.showwarning("Input Error", "Program Name cannot be empty!")
            return

        try:
            float(target)
        except:
            messagebox.showerror("Error", "Target must be a number")
            return

        save_program(name, purpose, target, due)
        add_program_to_list(name, purpose, target, due)
        contrib_window.destroy()

    tk.Button(contrib_window, text="Add", command=submit_info).pack(pady=15)

def open_program_window(program_name, target, due, purpose):
    subprocess.Popen([
        sys.executable,
        "contribution_window.py",
        program_name,
        target.replace(",", ""),
        due,
        purpose
    ])

def add_program_to_list(program_name, purpose, target, due):

    def delete_program():
        lbl_frame.destroy()

    def on_click(event, name=program_name, t=target, d=due, p=purpose):
        open_program_window(name, t, d, p)

    lbl_frame = tk.Frame(scrollable_frame)
    lbl_frame.pack(fill="x", padx=5, pady=2)

    row_text = f"{program_name:<20}{purpose:<20}{target:<15}{due:<15}"

    lbl = tk.Label(lbl_frame, text=row_text,
                   font=("Courier New", 11), anchor="w", cursor="hand2")
    lbl.pack(side="left", fill="x", expand=True)
    lbl.bind("<Button-1>", on_click)

    dots_btn = tk.Button(lbl_frame, text="⋮")
    dots_btn.pack(side="right")

    menu = tk.Menu(lbl_frame, tearoff=0)
    menu.add_command(label="Delete", command=delete_program)

    dots_btn.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))

root = tk.Tk()
root.title("Main Page")
root.geometry("700x500")

tk.Button(root, text="Create Contribution Program",
          command=open_contribution_window, width=30, height=2).pack(pady=10)

ttk.Separator(root, orient='horizontal').pack(fill='x', padx=10, pady=5)

header_text = f"{'Program Name':<20}{'Purpose':<20}{'Target':<15}{'Due Date':<15}"

tk.Label(root, text=header_text,
         font=("Courier New", 11, "bold"), anchor="w").pack(fill="x", padx=10)

scroll_frame = tk.Frame(root)
scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

canvas = tk.Canvas(scroll_frame)
scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind("<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

load_programs()
root.mainloop()