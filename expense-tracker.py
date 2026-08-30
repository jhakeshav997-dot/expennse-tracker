import sqlite3
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date

# tkcalendar aur matplotlib install karne ke liye terminal me chalao:
# pip install tkcalendar matplotlib
from tkcalendar import DateEntry
import matplotlib.pyplot as plt


# ---------------------------------------------------
# DATABASE SETUP
# ---------------------------------------------------
def setup_expense_database():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Date TEXT NOT NULL,
            Category TEXT NOT NULL,
            Amount REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_connection():
    return sqlite3.connect("expenses.db")


# ---------------------------------------------------
# DATABASE ACTIONS
# ---------------------------------------------------
def add_expense(exp_date, category, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (Date, Category, Amount) VALUES (?, ?, ?)",
        (exp_date, category, amount)
    )
    conn.commit()
    conn.close()


def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE ID = ?", (expense_id,))
    conn.commit()
    conn.close()


def fetch_all_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID, Date, Category, Amount FROM expenses ORDER BY Date DESC, ID DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_total():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(Amount) FROM expenses")
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0.0


def get_category_totals_for_month(year, month):
    """Diye gaye mahine (year, month) ke liye category-wise total nikalta hai."""
    conn = get_connection()
    cursor = conn.cursor()
    month_str = f"{year:04d}-{month:02d}"
    cursor.execute(
        "SELECT Category, SUM(Amount) FROM expenses WHERE Date LIKE ? GROUP BY Category",
        (f"{month_str}%",)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


# ---------------------------------------------------
# GUI (Tkinter Window)
# ---------------------------------------------------
CATEGORY_OPTIONS = [
    "Food", "Travel", "Gym", "Bills", "Rent", "Groceries",
    "Shopping", "Health", "Entertainment", "Other"
]


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker - खर्च ट्रैकर")
        self.root.geometry("650x560")
        self.root.resizable(False, False)

        # ---------- Input Frame ----------
        input_frame = tk.LabelFrame(root, text="Naya Expense Jodein", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=10)

        # Date picker (calendar wala)
        tk.Label(input_frame, text="Date:").grid(row=0, column=0, sticky="w", pady=5)
        self.date_entry = DateEntry(
            input_frame, width=18, date_pattern="yyyy-mm-dd",
            background="darkblue", foreground="white", borderwidth=2
        )
        self.date_entry.grid(row=0, column=1, pady=5, padx=5, sticky="w")

        # Category dropdown
        tk.Label(input_frame, text="Category:").grid(row=1, column=0, sticky="w", pady=5)
        self.category_combo = ttk.Combobox(
            input_frame, values=CATEGORY_OPTIONS, width=17, state="normal"
        )
        self.category_combo.grid(row=1, column=1, pady=5, padx=5, sticky="w")

        tk.Label(input_frame, text="Amount (₹):").grid(row=2, column=0, sticky="w", pady=5)
        self.amount_entry = tk.Entry(input_frame, width=20)
        self.amount_entry.grid(row=2, column=1, pady=5, padx=5, sticky="w")

        add_btn = tk.Button(input_frame, text="Add Expense", bg="#4CAF50", fg="white",
                             command=self.handle_add)
        add_btn.grid(row=0, column=2, rowspan=3, padx=15, ipadx=10, ipady=10)

        # ---------- Table Frame ----------
        table_frame = tk.Frame(root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("ID", "Date", "Category", "Amount")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.column("ID", width=50)
        self.tree.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # ---------- Action Buttons Frame ----------
        actions_frame = tk.Frame(root)
        actions_frame.pack(fill="x", padx=10, pady=5)

        delete_btn = tk.Button(actions_frame, text="Delete Selected", bg="#f44336", fg="white",
                                command=self.handle_delete)
        delete_btn.pack(side="left", padx=(0, 5))

        chart_btn = tk.Button(actions_frame, text="Monthly Chart", bg="#2196F3", fg="white",
                               command=self.handle_show_chart)
        chart_btn.pack(side="left", padx=5)

        export_btn = tk.Button(actions_frame, text="Export to CSV", bg="#FF9800", fg="white",
                                command=self.handle_export_csv)
        export_btn.pack(side="left", padx=5)

        # ---------- Bottom Frame ----------
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(fill="x", padx=10, pady=10)

        self.total_label = tk.Label(bottom_frame, text="Total: ₹0.00", font=("Arial", 12, "bold"))
        self.total_label.pack(side="right")

        self.refresh_table()

    # -----------------------------------------------
    def handle_add(self):
        exp_date = self.date_entry.get().strip()
        category = self.category_combo.get().strip()
        amount_text = self.amount_entry.get().strip()

        if not exp_date or not category or not amount_text:
            messagebox.showwarning("Missing Info", "Kripya sabhi fields bharein.")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror("Galat Amount", "Amount sirf number me dalein (jaise 250 ya 99.50).")
            return

        add_expense(exp_date, category, amount)
        self.category_combo.set("")
        self.amount_entry.delete(0, tk.END)
        self.refresh_table()

    def handle_delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Kuch Select Nahi", "Delete karne ke liye pehle ek row select karein.")
            return

        item = self.tree.item(selected[0])
        expense_id = item["values"][0]

        confirm = messagebox.askyesno("Confirm Delete", f"ID {expense_id} wala expense delete karein?")
        if confirm:
            delete_expense(expense_id)
            self.refresh_table()

    def handle_show_chart(self):
        today = date.today()
        data = get_category_totals_for_month(today.year, today.month)

        if not data:
            messagebox.showinfo("Data Nahi Mila", "Is mahine ka koi expense record nahi mila.")
            return

        labels = [row[0] for row in data]
        values = [row[1] for row in data]

        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        plt.title(f"Category-wise Kharch - {today.strftime('%B %Y')}")
        plt.axis("equal")
        plt.show()

    def handle_export_csv(self):
        rows = fetch_all_expenses()
        if not rows:
            messagebox.showinfo("Data Nahi Mila", "Export karne ke liye koi expense nahi hai.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="expenses_export.csv"
        )
        if not file_path:
            return

        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Date", "Category", "Amount"])
            writer.writerows(rows)

        messagebox.showinfo("Export Ho Gaya", f"Data safaltapoorvak export ho gaya:\n{file_path}")

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for expense in fetch_all_expenses():
            self.tree.insert("", tk.END, values=expense)

        total = get_total()
        self.total_label.config(text=f"Total: ₹{total:,.2f}")


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------
if __name__ == "__main__":
    setup_expense_database()
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
