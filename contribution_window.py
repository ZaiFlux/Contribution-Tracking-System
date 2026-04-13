import tkinter as tk
from tkinter import ttk, messagebox
import sys

# ===== DATA =====
contributors_data = []
edit_refresh_callback = None

program_name = sys.argv[1] if len(sys.argv) > 1 else "Program Name"

# ✅ FIX: safe float conversion
program_target = float(sys.argv[2].replace(",", "")) if len(sys.argv) > 2 else 0.0
program_due = sys.argv[3] if len(sys.argv) > 3 else "Due Date"

# ===== FONT CONTROL (UNCHANGED) =====
TABLE_FONT = ("Consolas", 10)
HEADER_FONT = ("Consolas", 10, "bold")

def main_menu():
    print("Main Menu clicked")

def add_contributor():
    open_add_contributor_window()

def generate_receipt():
    print("Generate Receipt clicked")

# ===== REFRESH TABLE =====
def refresh_table():
    for item in contributor_tree.get_children():
        contributor_tree.delete(item)

    if not contributors_data:
        return

    for data in contributors_data:
        remaining = data["target"] - data["current"]
        contributor_tree.insert("", "end", values=(
            data["name"],
            f"{data['current']:.2f}",
            f"{data['target']:.2f}",
            f"{remaining:.2f}"
        ))

# ===== ADD CONTRIBUTOR WINDOW (UNCHANGED UI) =====
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
            "target": program_target  # ✅ FIXED
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

    category_dropdown["values"] = (
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

    category_var.trace_add("write", update_dynamic_field)

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

    tk.Button(
        win,
        text="Add Contributor",
        command=submit_form,
        bg="#4CAF50",
        fg="white",
        width=25
    ).pack(pady=20)

# ===== EDIT WINDOW (ONLY FIX NUMBER INPUT) =====
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

            def open_add_amount(idx=i):
                data = contributors_data[idx]
                win = tk.Toplevel(root)
                win.title("Add Amount")
                win.geometry("300x150")

                tk.Label(win, text=f"Update {data['name']}").pack(pady=10)
                entry = tk.Entry(win)
                entry.pack()

                def update_val():
                    try:
                        contributors_data[idx]["current"] += float(entry.get().replace(",", ""))  # ✅ FIX
                        refresh_table()
                        if edit_refresh_callback:
                            edit_refresh_callback()
                        win.destroy()
                    except:
                        messagebox.showerror("Error", "Invalid input")

                tk.Button(win, text="Update", command=update_val).pack(pady=10)

            ttk.Button(row, text="Add Amount", command=open_add_amount).pack(side="left", padx=5)

            def delete_item(idx=i):
                contributors_data.pop(idx)
                refresh_edit()
                refresh_table()

            ttk.Button(row, text="❌", command=delete_item).pack(side="right")

    edit_refresh_callback = refresh_edit
    refresh_edit()

# ===== MAIN WINDOW (UNCHANGED UI) =====
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

scroll_container = ttk.Frame(root)
scroll_container.pack(fill="both", expand=True, padx=10, pady=5)

columns = ("Contributor", "Current", "Target", "Remaining")

contributor_tree = ttk.Treeview(scroll_container, columns=columns, show="headings")

contributor_tree.heading("Contributor", text="Contributor", anchor="w")
contributor_tree.heading("Current", text="Current", anchor="w")
contributor_tree.heading("Target", text="Target", anchor="w")
contributor_tree.heading("Remaining", text="Remaining", anchor="w")

contributor_tree.column("Contributor", anchor="w", width=220)
contributor_tree.column("Current", anchor="w", width=120)
contributor_tree.column("Target", anchor="w", width=120)
contributor_tree.column("Remaining", anchor="w", width=120)

style = ttk.Style()
style.configure("Treeview.Heading", font=HEADER_FONT)
style.configure("Treeview", font=TABLE_FONT, rowheight=20)

contributor_tree.pack(fill="both", expand=True)

refresh_table()

root.mainloop()