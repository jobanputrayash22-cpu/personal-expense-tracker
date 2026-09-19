import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database import get_connection


class ExpenseTrackerUI:

    def __init__(self, root):
        self.root = root

        self.root.title("Personal Expense Tracker")
        self.root.geometry("1100x700")
        self.root.minsize(950, 600)
        self.root.configure(bg="#f5f6fa")

        self.setup_styles()
        self.create_header()
        self.create_summary_cards()
        self.create_action_bar()
        self.create_expense_table()

        self.load_expenses()

    # =========================
    # STYLES
    # =========================

    def setup_styles(self):

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="white",
            foreground="#2f3542",
            rowheight=40,
            fieldbackground="white",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#2f3542",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=10
        )

        style.map(
            "Treeview",
            background=[("selected", "#dfe4ea")],
            foreground=[("selected", "#2f3542")]
        )

    # =========================
    # HEADER
    # =========================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg="#2f3542",
            height=80
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="Personal Expense Tracker",
            font=("Segoe UI", 22, "bold"),
            bg="#2f3542",
            fg="white"
        )

        title.pack(side="left", padx=30)

        subtitle = tk.Label(
            header,
            text="Manage your daily expenses",
            font=("Segoe UI", 10),
            bg="#2f3542",
            fg="#dfe4ea"
        )

        subtitle.pack(side="right", padx=30)

    # =========================
    # SUMMARY CARDS
    # =========================

    def create_summary_cards(self):

        container = tk.Frame(
            self.root,
            bg="#f5f6fa"
        )

        container.pack(
            fill="x",
            padx=30,
            pady=25
        )

        self.total_expenses_label = self.create_card(
            container,
            "Total Expenses",
            "₹ 0.00",
            0
        )

        self.month_expenses_label = self.create_card(
            container,
            "This Month",
            "₹ 0.00",
            1
        )

        self.transaction_label = self.create_card(
            container,
            "Transactions",
            "0",
            2
        )

    def create_card(self, parent, title, value, column):

        card = tk.Frame(
            parent,
            bg="white",
            height=110,
            bd=1,
            relief="solid"
        )

        card.grid(
            row=0,
            column=column,
            padx=8,
            sticky="nsew"
        )

        parent.grid_columnconfigure(
            column,
            weight=1
        )

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 10),
            bg="white",
            fg="#747d8c"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#2f3542"
        )

        value_label.pack(
            anchor="w",
            padx=20
        )

        return value_label

    # =========================
    # ACTION BAR
    # =========================

    def create_action_bar(self):

        action_frame = tk.Frame(
            self.root,
            bg="#f5f6fa"
        )

        action_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        # Add Expense

        add_button = tk.Button(
            action_frame,
            text="+ Add Expense",
            font=("Segoe UI", 10, "bold"),
            bg="#2f3542",
            fg="white",
            activebackground="#57606f",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
            command=self.add_expense_form
        )

        add_button.pack(side="left")

        # Delete Expense

        delete_button = tk.Button(
            action_frame,
            text="Delete Selected",
            font=("Segoe UI", 10, "bold"),
            bg="#d63031",
            fg="white",
            activebackground="#ff7675",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
            command=self.delete_expense
        )

        delete_button.pack(
            side="left",
            padx=(10, 0)
        )

        # Monthly Summary

        summary_button = tk.Button(
            action_frame,
            text="Monthly Summary",
            font=("Segoe UI", 10, "bold"),
            bg="#3742fa",
            fg="white",
            activebackground="#5352ed",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
            command=self.show_monthly_summary
        )

        summary_button.pack(
            side="left",
            padx=(10, 0)
        )

        # Search

        self.search_entry = tk.Entry(
            action_frame,
            font=("Segoe UI", 11),
            width=30,
            relief="solid",
            bd=1
        )

        self.search_entry.pack(
            side="right",
            ipady=7
        )

        self.search_entry.insert(
            0,
            "Search expenses..."
        )

        self.search_entry.bind(
            "<FocusIn>",
            self.clear_search_placeholder
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_expenses
        )

    def clear_search_placeholder(self, event=None):

        if self.search_entry.get() == "Search expenses...":

            self.search_entry.delete(
                0,
                tk.END
            )

    # =========================
    # EXPENSE TABLE
    # =========================

    def create_expense_table(self):

        table_frame = tk.Frame(
            self.root,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 30)
        )

        columns = (
            "id",
            "title",
            "amount",
            "category",
            "date"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.table.heading(
            "id",
            text="ID"
        )

        self.table.heading(
            "title",
            text="Title"
        )

        self.table.heading(
            "amount",
            text="Amount"
        )

        self.table.heading(
            "category",
            text="Category"
        )

        self.table.heading(
            "date",
            text="Date"
        )

        self.table.column(
            "id",
            width=60,
            anchor="center"
        )

        self.table.column(
            "title",
            width=280
        )

        self.table.column(
            "amount",
            width=150
        )

        self.table.column(
            "category",
            width=180
        )

        self.table.column(
            "date",
            width=180
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

    # =========================
    # DELETE EXPENSE
    # =========================

    def delete_expense(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select an expense to delete."
            )

            return

        item = self.table.item(selected[0])

        expense_id = item["values"][0]
        expense_title = item["values"][1]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete\n'{expense_title}'?"
        )

        if not confirm:
            return

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Deleted",
            "Expense deleted successfully."
        )

        self.load_expenses()

    # =========================
    # MONTHLY SUMMARY
    # =========================

    def show_monthly_summary(self):

        window = tk.Toplevel(self.root)

        window.title("Monthly Expense Summary")
        window.geometry("650x500")
        window.resizable(False, False)
        window.configure(bg="#f5f6fa")

        tk.Label(
            window,
            text="Monthly Expense Summary",
            font=("Segoe UI", 20, "bold"),
            bg="#f5f6fa",
            fg="#2f3542"
        ).pack(
            pady=(25, 5)
        )

        tk.Label(
            window,
            text="Expense breakdown by month",
            font=("Segoe UI", 10),
            bg="#f5f6fa",
            fg="#747d8c"
        ).pack(
            pady=(0, 20)
        )

        table_frame = tk.Frame(
            window,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 30)
        )

        columns = (
            "month",
            "total",
            "transactions"
        )

        summary_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        summary_table.heading(
            "month",
            text="Month"
        )

        summary_table.heading(
            "total",
            text="Total Expense"
        )

        summary_table.heading(
            "transactions",
            text="Transactions"
        )

        summary_table.column(
            "month",
            width=200,
            anchor="center"
        )

        summary_table.column(
            "total",
            width=200,
            anchor="center"
        )

        summary_table.column(
            "transactions",
            width=150,
            anchor="center"
        )

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                substr(expense_date, 1, 7) AS month,
                SUM(amount) AS total,
                COUNT(*) AS transactions
            FROM expenses
            GROUP BY substr(expense_date, 1, 7)
            ORDER BY month DESC
            """
        )

        summaries = cursor.fetchall()

        connection.close()

        for summary in summaries:

            summary_table.insert(
                "",
                "end",
                values=(
                    summary["month"],
                    f"₹ {summary['total']:,.2f}",
                    summary["transactions"]
                )
            )

        summary_table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    # =========================
    # ADD EXPENSE FORM
    # =========================

    def add_expense_form(self):

        form = tk.Toplevel(self.root)

        form.title("Add Expense")
        form.geometry("450x500")
        form.resizable(False, False)
        form.configure(bg="#f5f6fa")

        tk.Label(
            form,
            text="Add New Expense",
            font=("Segoe UI", 20, "bold"),
            bg="#f5f6fa",
            fg="#2f3542"
        ).pack(
            pady=(25, 5)
        )

        tk.Label(
            form,
            text="Enter your expense details",
            font=("Segoe UI", 10),
            bg="#f5f6fa",
            fg="#747d8c"
        ).pack(
            pady=(0, 25)
        )

        # Title

        tk.Label(
            form,
            text="Expense Title",
            font=("Segoe UI", 10, "bold"),
            bg="#f5f6fa"
        ).pack(
            anchor="w",
            padx=45
        )

        title_entry = tk.Entry(
            form,
            font=("Segoe UI", 11),
            width=35
        )

        title_entry.pack(
            padx=45,
            pady=(5, 15),
            ipady=7
        )

        # Amount

        tk.Label(
            form,
            text="Amount",
            font=("Segoe UI", 10, "bold"),
            bg="#f5f6fa"
        ).pack(
            anchor="w",
            padx=45
        )

        amount_entry = tk.Entry(
            form,
            font=("Segoe UI", 11),
            width=35
        )

        amount_entry.pack(
            padx=45,
            pady=(5, 15),
            ipady=7
        )

        # Category

        tk.Label(
            form,
            text="Category",
            font=("Segoe UI", 10, "bold"),
            bg="#f5f6fa"
        ).pack(
            anchor="w",
            padx=45
        )

        category_combo = ttk.Combobox(
            form,
            values=[
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Entertainment",
                "Health",
                "Education",
                "Other"
            ],
            state="readonly",
            width=33
        )

        category_combo.pack(
            padx=45,
            pady=(5, 15),
            ipady=5
        )

        category_combo.set("Food")

        # Date

        tk.Label(
            form,
            text="Date",
            font=("Segoe UI", 10, "bold"),
            bg="#f5f6fa"
        ).pack(
            anchor="w",
            padx=45
        )

        date_entry = tk.Entry(
            form,
            font=("Segoe UI", 11),
            width=35
        )

        date_entry.pack(
            padx=45,
            pady=(5, 20),
            ipady=7
        )

        date_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        # =========================
        # SAVE EXPENSE
        # =========================

        def save_expense():

            title = title_entry.get().strip()
            amount = amount_entry.get().strip()
            category = category_combo.get()
            date = date_entry.get().strip()

            # Empty fields

            if not title or not amount or not category or not date:

                messagebox.showwarning(
                    "Missing Information",
                    "Please fill all fields."
                )

                return

            # Title validation

            if len(title) < 2:

                messagebox.showwarning(
                    "Invalid Title",
                    "Expense title must contain at least 2 characters."
                )

                return

            # Amount validation

            try:

                amount = float(amount)

                if amount <= 0:
                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    "Invalid Amount",
                    "Please enter a valid amount greater than 0."
                )

                return

            # Date validation

            try:

                expense_date = datetime.strptime(
                    date,
                    "%Y-%m-%d"
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Date",
                    "Date must be in YYYY-MM-DD format."
                )

                return

            # Future date validation

            if expense_date > datetime.now():

                messagebox.showerror(
                    "Invalid Date",
                    "Expense date cannot be in the future."
                )

                return

            # Save to database

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO expenses
                (title, amount, category, expense_date)
                VALUES (?, ?, ?, ?)
                """,
                (
                    title,
                    amount,
                    category,
                    date
                )
            )

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Expense added successfully!"
            )

            form.destroy()

            self.load_expenses()

        # Add Button

        tk.Button(
            form,
            text="Add Expense",
            font=("Segoe UI", 10, "bold"),
            bg="#2f3542",
            fg="white",
            activebackground="#57606f",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=10,
            command=save_expense
        ).pack()

    # =========================
    # SEARCH
    # =========================

    def search_expenses(self, event=None):

        search_text = self.search_entry.get().strip()

        if search_text == "Search expenses...":
            search_text = ""

        self.load_expenses(search_text)

    # =========================
    # LOAD EXPENSES
    # =========================

    def load_expenses(self, search_text=""):

        connection = get_connection()
        cursor = connection.cursor()

        if search_text:

            cursor.execute(
                """
                SELECT id, title, amount, category, expense_date
                FROM expenses
                WHERE title LIKE ?
                   OR category LIKE ?
                ORDER BY id DESC
                """,
                (
                    f"%{search_text}%",
                    f"%{search_text}%"
                )
            )

        else:

            cursor.execute(
                """
                SELECT id, title, amount, category, expense_date
                FROM expenses
                ORDER BY id DESC
                """
            )

        expenses = cursor.fetchall()

        # Total expenses

        cursor.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses"
        )

        total_expenses = cursor.fetchone()[0]

        # Current month

        current_month = datetime.now().strftime("%Y-%m")

        cursor.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE substr(expense_date, 1, 7) = ?
            """,
            (current_month,)
        )

        month_expenses = cursor.fetchone()[0]

        # Transaction count

        cursor.execute(
            "SELECT COUNT(*) FROM expenses"
        )

        transaction_count = cursor.fetchone()[0]

        connection.close()

        # Update cards

        self.total_expenses_label.config(
            text=f"₹ {total_expenses:,.2f}"
        )

        self.month_expenses_label.config(
            text=f"₹ {month_expenses:,.2f}"
        )

        self.transaction_label.config(
            text=str(transaction_count)
        )

        # Clear table

        for item in self.table.get_children():

            self.table.delete(item)

        # Add records

        for expense in expenses:

            self.table.insert(
                "",
                "end",
                values=(
                    expense["id"],
                    expense["title"],
                    f"₹ {expense['amount']:,.2f}",
                    expense["category"],
                    expense["expense_date"]
                )
            )


# =========================
# START APPLICATION
# =========================

if __name__ == "__main__":

    root = tk.Tk()

    app = ExpenseTrackerUI(root)

    root.mainloop()