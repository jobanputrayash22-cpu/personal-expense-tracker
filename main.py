import tkinter as tk

from database import initialize_database
from ui import ExpenseTrackerUI


def main():
    initialize_database()

    root = tk.Tk()

    ExpenseTrackerUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()