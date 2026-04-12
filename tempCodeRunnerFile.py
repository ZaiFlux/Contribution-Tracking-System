import tkinter as tk
from tkinter import ttk, messagebox
import sys

# ===== DATA =====
contributors_data = []
edit_refresh_callback = None

program_name = sys.argv[1] if len(sys.argv) > 1 else "Program Name"

def main_menu():
    print("Main Menu clicked")

def add_contributor():
    open_add_contributor_window()

def generate_receipt():
    print("Generate Receipt clicked")

# ===== REFRESH TABLE =====
def refresh_table():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Create header labels
    headers = ["Contributor", "Current", "Target", "Remaining"]
    for col_idx, header_text in enumerate(headers):
        ttk.Label(
            scrollable_frame,
            text=header_text,
            font=("Arial", 10, "bold"),
            foreground="#555"
        ).grid(row=0, column=col_idx, sticky="w", padx=5, pady=5)

    if not contributors_data:
        ttk.Label(
            scrollable_frame,
            text="No contributors yet. Add one to get started.",
            font=("Arial", 12)
        ).grid(row=1, column=0, columnspan=4, pady=40, sticky="w")
        return

    # Configure columns to have equal width
    for i in range(4):
        scrollable_frame.columnconfigure(i, weight=1, uniform="group1")

    # Add contributor data starting from row 1
    for i, data in enumerate(contributors_data, start=1):
        remaining = data["target"] - data["current"]
        ttk.Label(scrollable_frame, text=data["name"]).grid(row=i, column=0, sticky="w", padx=5)
        ttk.Label(scrollable_frame, text=f"{data['current']:.2f}").grid(row=i, column=1, sticky="w", padx=5)
        ttk.Label(scrollable_frame, text=f"{data['target']:.2f}").grid(row=i, column=2, sticky="w", padx=5)
        ttk.Label(scrollable_frame, text=f"{remaining:.2f}").grid(row=i, column=3, sticky="w", padx=5)

# ===== ADD CONTRIBUTOR WINDOW =====
def open_add_contributor_window():
    win = tk.Toplevel(root)
    win.title("Contributor Form")
    win.geometry("450x550")

    def update_dynamic_field(*args):
        category = category_var.get()
        if category in ["Student", "Teacher"]:
            dynamic_label.config(text="School")
        elif category == "Alumni":
            dynamic_label.config(text="Year Graduated")
        elif category == "Parent Sponsor":
            dynamic_label.config(text="Child Name")
        else:
            dynamic_label.config(text="Additional Info")

    def submit_form():
        name = name_entry.get()
        if not name:
            messagebox.showerror("Error", "Name is required.")
            return

        contributors_data.append({
            "name": name,
            "current": 0.0,
            "target": 0.0
        })

        refresh_table()
        if edit_refresh_callback:
            edit_refresh_callback()
        win.destroy()

    form_frame = tk.Frame(win)
    form_frame.pack(expand=True, pady=10)

    tk.Label(form_frame, text="Category", font=("Arial", 10, "bold")).pack()

    category_var = tk.StringVar()
    category_dropdown = ttk.Combobox(
        form_frame,
        textvariable=category_var,
        state="readonly",
        width=32
    )

    category_dropdown['values'] = (
        "Select Category",
        "Student",
        "Teacher",
        "Alumni",
        "Parent",
        "Sponsor",
        "Others"
    )

    category_dropdown.current(0)
    category_dropdown.pack(pady=5)

    category_var.trace("w", update_dynamic_field)

    tk.Label(form_frame, text="Full Name").pack()
    name_entry = tk.Entry(form_frame, width=35)
    name_entry.pack(pady=5)

    tk.Label(form_frame, text="Phone Number").pack()
    phone_entry = tk.Entry(form_frame, width=35)
    phone_entry.pack(pady=5)

    tk.Label(form_frame, text="Email Address").pack()
    email_entry = tk.Entry(form_frame, width=35)
    email_entry.pack(pady=5)

    dynamic_label = tk.Label(form_frame, text="Additional Info")
    dynamic_label.pack()

    dynamic_entry = tk.Entry(form_frame, width=35)
    dynamic_entry.pack(pady=5)

    tk.Button(win, text="Add Contributor",
              command=submit_form,
              bg="#4CAF50",
              fg="white",
              width=25).pack(pady=20)

# ===== EDIT WINDOW =====
def edit_contributor():
    global edit_refresh_callback

    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Records")
    edit_window.geometry("500x350")

    frame = ttk.Frame(edit_window)
    frame.pack(fill="both", expand=True)

    canvas_edit = tk.Canvas(frame)
    scrollbar_edit = ttk.Scrollbar(frame, orient="vertical", command=canvas_edit.yview)
    list_frame = ttk.Frame(canvas_edit)

    list_frame.bind("<Configure>", lambda e: canvas_edit.configure(scrollregion=canvas_edit.bbox("all")))
    canvas_edit.create_window((0, 0), window=list_frame, anchor="nw")
    canvas_edit.configure(yscrollcommand=scrollbar_edit.set)

    canvas_edit.pack(side="left", fill="both", expand=True)
    scrollbar_edit.pack(side="right", fill="y")

    def refresh_edit():
        for w in list_frame.winfo_children():
            w.destroy()

        for i, d in enumerate(contributors_data):
            row = ttk.Frame(list_frame)
            row.pack(fill="x", pady=5)

            ttk.Label(row, text=d["name"]).pack(side="left")

            ttk.Button(
                row,
                text="Add Amount",
                command=lambda idx=i: open_add_amount(idx)
            ).pack(side="left", padx=5)

            def delete_item(idx=i):
                contributors_data.pop(idx)
                refresh_edit()
                refresh_table()

            ttk.Button(row, text="❌", command=delete_item).pack(side="right")

    edit_refresh_callback = refresh_edit
    refresh_edit()

def open_add_amount(index):
    data = contributors_data[index]

    win = tk.Toplevel(root)
    win.title("Add Amount")
    win.geometry("300x150")

    tk.Label(win, text=f"Update {data['name']}").pack(pady=10)

    entry = tk.Entry(win)
    entry.pack()

    def update_val():
        try:
            data["current"] += float(entry.get())
            refresh_table()
            if edit_refresh_callback:
                edit_refresh_callback()
            win.destroy()
        except:
            messagebox.showerror("Error", "Invalid input")

    tk.Button(win, text="Update", command=update_val).pack(pady=10)

# ===== MAIN WINDOW =====
root = tk.Tk()
root.title("Contribution Program")
root.geometry("900x500")

top_frame = ttk.Frame(root, padding=5, relief="solid", borderwidth=1)
top_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(top_frame, text=program_name, font=("Arial", 12)).grid(row=0, column=0, sticky="w")
ttk.Label(top_frame, text="Due Date", font=("Arial", 10)).grid(row=0, column=1)

dots_button = ttk.Button(top_frame, text="⋯", width=3)
dots_button.grid(row=0, column=2, sticky="e")

top_frame.columnconfigure(1, weight=1)

menu = tk.Menu(root, tearoff=0)
menu.add_command(label="Main Menu", command=main_menu)
menu.add_command(label="Add Contributor", command=add_contributor)
menu.add_command(label="Edit Records", command=edit_contributor)
menu.add_separator()
menu.add_command(label="Generate Receipt", command=generate_receipt)

dots_button.bind("<Button-1>", lambda e: menu.post(e.x_root, e.y_root))

# ===== HEADER =====
header = ttk.Frame(root)
header.pack(fill="x", padx=10)

cols = ["Contributor", "Current", "Target", "Remaining"]
for i, c in enumerate(cols):
    header.columnconfigure(i, weight=1, uniform="group1")
    ttk.Label(
        header,
        text=c.upper(),
        font=("Arial", 10, "bold"),
        foreground="#555"
    ).grid(row=0, column=i, sticky="w")

# ===== TABLE =====
scroll_container = ttk.Frame(root)
scroll_container.pack(fill="both", expand=True, padx=10, pady=5)

canvas = tk.Canvas(scroll_container, highlightthickness=0)
scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def sync_width(event):
    canvas.itemconfig(canvas_window, width=event.width)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.bind("<Configure>", sync_width)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

refresh_table()
root.mainloop()