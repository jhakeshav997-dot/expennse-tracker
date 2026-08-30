"""
Student Management Software - GUI Version (Tkinter)
"""

import tkinter as tk
from tkinter import ttk, messagebox

# Student data (Roll No -> Name, Marks)
students = {
    1: {"name": "Keshav", "marks": 34},
    2: {"name": "Amit", "marks": 45},
    3: {"name": "Gaurav", "marks": 46},
}


def get_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 75:
        return "A"
    elif marks >= 60:
        return "B"
    elif marks >= 40:
        return "C"
    elif marks >= 33:
        return "D (Pass)"
    else:
        return "F (Fail)"


def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for roll_no, info in students.items():
        grade = get_grade(info["marks"])
        tree.insert("", "end", values=(roll_no, info["name"], info["marks"], grade))


def add_student():
    try:
        roll_no = int(entry_roll.get())
        name = entry_name.get().strip()
        marks = float(entry_marks.get())

        if not name:
            messagebox.showerror("Error", "Naam khali nahi ho sakta!")
            return
        if roll_no in students:
            messagebox.showerror("Error", "Ye Roll No pehle se maujood hai!")
            return

        students[roll_no] = {"name": name, "marks": marks}
        refresh_table()
        clear_fields()
        messagebox.showinfo("Success", f"{name} add ho gaya!")
    except ValueError:
        messagebox.showerror("Error", "Roll No aur Marks numbers mein hone chahiye!")


def delete_student():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Pehle ek student select karo!")
        return
    item = tree.item(selected[0])
    roll_no = int(item["values"][0])
    name = item["values"][1]
    if messagebox.askyesno("Confirm", f"Kya '{name}' ko delete karna hai?"):
        del students[roll_no]
        refresh_table()


def search_student():
    query = entry_search.get().strip()
    if not query:
        refresh_table()
        return
    for row in tree.get_children():
        tree.delete(row)
    for roll_no, info in students.items():
        if query == str(roll_no) or query.lower() in info["name"].lower():
            grade = get_grade(info["marks"])
            tree.insert("", "end", values=(roll_no, info["name"], info["marks"], grade))


def clear_fields():
    entry_roll.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_marks.delete(0, tk.END)


# ---------- Main Window ----------
root = tk.Tk()
root.title("Student Management Software")
root.geometry("650x500")
root.resizable(False, False)

heading = tk.Label(root, text="Student Management System", font=("Arial", 16, "bold"))
heading.pack(pady=10)

# ---------- Input Frame ----------
input_frame = tk.Frame(root)
input_frame.pack(pady=5)

tk.Label(input_frame, text="Roll No:").grid(row=0, column=0, padx=5, pady=5)
entry_roll = tk.Entry(input_frame, width=12)
entry_roll.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Naam:").grid(row=0, column=2, padx=5, pady=5)
entry_name = tk.Entry(input_frame, width=15)
entry_name.grid(row=0, column=3, padx=5)

tk.Label(input_frame, text="Marks:").grid(row=0, column=4, padx=5, pady=5)
entry_marks = tk.Entry(input_frame, width=10)
entry_marks.grid(row=0, column=5, padx=5)

btn_add = tk.Button(input_frame, text="Add Student", bg="#4CAF50", fg="white", command=add_student)
btn_add.grid(row=0, column=6, padx=10)

# ---------- Search + Delete Frame ----------
action_frame = tk.Frame(root)
action_frame.pack(pady=5)

tk.Label(action_frame, text="Search (Roll No / Naam):").grid(row=0, column=0, padx=5)
entry_search = tk.Entry(action_frame, width=20)
entry_search.grid(row=0, column=1, padx=5)

btn_search = tk.Button(action_frame, text="Search", command=search_student)
btn_search.grid(row=0, column=2, padx=5)

btn_reset = tk.Button(action_frame, text="Show All", command=refresh_table)
btn_reset.grid(row=0, column=3, padx=5)

btn_delete = tk.Button(action_frame, text="Delete Selected", bg="#f44336", fg="white", command=delete_student)
btn_delete.grid(row=0, column=4, padx=5)

# ---------- Table (Treeview) ----------
columns = ("Roll No", "Name", "Marks", "Grade")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=140)
tree.pack(pady=15)

refresh_table()

root.mainloop()