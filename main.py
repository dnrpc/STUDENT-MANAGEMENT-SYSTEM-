import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_FILE = "students.db"


class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1000x650")
        self.root.minsize(820, 540)
        self.selected_student_id = None

        self.setup_style()
        self.create_widgets()
        self.load_students()

    def connect_db(self):
        return sqlite3.connect(DB_FILE)

    def setup_database(self):
        with self.connect_db() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roll_no TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    course TEXT NOT NULL,
                    email TEXT,
                    phone TEXT
                )
            """)

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Section.TLabel", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("TButton", padding=(10, 6))

    def create_widgets(self):
        outer = ttk.Frame(self.root, padding=18)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text="Student Management System",
                  style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            outer,
            text="Add, view, search, update, and delete student records."
        ).pack(anchor="w", pady=(4, 16))

        form = ttk.LabelFrame(outer, text="Student Details", padding=12)
        form.pack(fill="x")

        self.roll_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.course_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.search_var = tk.StringVar()

        fields = [
            ("Roll Number *", self.roll_var),
            ("Full Name *", self.name_var),
            ("Course *", self.course_var),
            ("Email", self.email_var),
            ("Phone", self.phone_var),
        ]

        for index, (label, variable) in enumerate(fields):
            row, col = divmod(index, 3)
            cell = ttk.Frame(form)
            cell.grid(row=row, column=col, sticky="ew", padx=6, pady=6)
            ttk.Label(cell, text=label).pack(anchor="w")
            ttk.Entry(cell, textvariable=variable).pack(fill="x", pady=(3, 0))

        for col in range(3):
            form.columnconfigure(col, weight=1)

        actions = ttk.Frame(outer)
        actions.pack(fill="x", pady=10)
        ttk.Button(actions, text="Add Student",
                   command=self.add_student).pack(side="left", padx=(0, 6))
        ttk.Button(actions, text="Update Selected",
                   command=self.update_student).pack(side="left", padx=6)
        ttk.Button(actions, text="Delete Selected",
                   command=self.delete_student).pack(side="left", padx=6)
        ttk.Button(actions, text="Clear Form",
                   command=self.clear_form).pack(side="left", padx=6)

        search_frame = ttk.Frame(outer)
        search_frame.pack(fill="x", pady=(4, 8))
        ttk.Label(search_frame, text="Search:").pack(side="left", padx=(0, 8))
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True)
        search_entry.bind("<KeyRelease>", lambda _event: self.load_students())
        ttk.Button(search_frame, text="Clear Search",
                   command=self.clear_search).pack(side="left", padx=(8, 0))

        table_frame = ttk.Frame(outer)
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "roll_no", "name", "course", "email", "phone")
        self.table = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )
        headings = {
            "id": "ID", "roll_no": "Roll Number", "name": "Full Name",
            "course": "Course", "email": "Email", "phone": "Phone"
        }
        widths = {
            "id": 55, "roll_no": 115, "name": 190,
            "course": 145, "email": 220, "phone": 125
        }
        for column in columns:
            self.table.heading(column, text=headings[column])
            self.table.column(column, width=widths[column], minwidth=50,
                              anchor="w")
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical",
                                 command=self.table.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal",
                                 command=self.table.xview)
        self.table.configure(yscrollcommand=y_scroll.set,
                             xscrollcommand=x_scroll.set)
        self.table.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        self.table.bind("<<TreeviewSelect>>", self.on_row_select)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(outer, textvariable=self.status_var).pack(anchor="w", pady=(8, 0))
        self.setup_database()

    def validate_form(self):
        roll_no = self.roll_var.get().strip()
        name = self.name_var.get().strip()
        course = self.course_var.get().strip()
        if not roll_no or not name or not course:
            messagebox.showwarning(
                "Missing details",
                "Please fill in Roll Number, Full Name, and Course."
            )
            return None
        return (
            roll_no, name, course,
            self.email_var.get().strip(), self.phone_var.get().strip()
        )

    def add_student(self):
        values = self.validate_form()
        if values is None:
            return
        try:
            with self.connect_db() as conn:
                conn.execute("""
                    INSERT INTO students (roll_no, name, course, email, phone)
                    VALUES (?, ?, ?, ?, ?)
                """, values)
            self.load_students()
            self.clear_form()
            self.status_var.set("Student added successfully.")
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Duplicate roll number",
                "That roll number already exists. Please use a unique one."
            )
        except sqlite3.Error as exc:
            messagebox.showerror("Database error", str(exc))

    def update_student(self):
        if self.selected_student_id is None:
            messagebox.showinfo("Select a student", "Select a row to update.")
            return
        values = self.validate_form()
        if values is None:
            return
        try:
            with self.connect_db() as conn:
                conn.execute("""
                    UPDATE students
                    SET roll_no=?, name=?, course=?, email=?, phone=?
                    WHERE id=?
                """, (*values, self.selected_student_id))
            self.load_students()
            self.clear_form()
            self.status_var.set("Student updated successfully.")
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Duplicate roll number",
                "Another student already uses that roll number."
            )
        except sqlite3.Error as exc:
            messagebox.showerror("Database error", str(exc))

    def delete_student(self):
        if self.selected_student_id is None:
            messagebox.showinfo("Select a student", "Select a row to delete.")
            return
        if not messagebox.askyesno(
            "Confirm deletion", "Delete the selected student record?"
        ):
            return
        try:
            with self.connect_db() as conn:
                conn.execute(
                    "DELETE FROM students WHERE id=?",
                    (self.selected_student_id,)
                )
            self.load_students()
            self.clear_form()
            self.status_var.set("Student deleted successfully.")
        except sqlite3.Error as exc:
            messagebox.showerror("Database error", str(exc))

    def load_students(self):
        for item in self.table.get_children():
            self.table.delete(item)
        query = self.search_var.get().strip()
        try:
            with self.connect_db() as conn:
                if query:
                    pattern = f"%{query}%"
                    rows = conn.execute("""
                        SELECT id, roll_no, name, course, email, phone
                        FROM students
                        WHERE roll_no LIKE ? OR name LIKE ? OR course LIKE ?
                           OR email LIKE ? OR phone LIKE ?
                        ORDER BY name COLLATE NOCASE
                    """, (pattern, pattern, pattern, pattern, pattern)).fetchall()
                else:
                    rows = conn.execute("""
                        SELECT id, roll_no, name, course, email, phone
                        FROM students
                        ORDER BY name COLLATE NOCASE
                    """).fetchall()
            for row in rows:
                self.table.insert("", "end", values=row)
            self.status_var.set(f"{len(rows)} student record(s) shown.")
        except sqlite3.Error as exc:
            messagebox.showerror("Database error", str(exc))

    def on_row_select(self, _event=None):
        selection = self.table.selection()
        if not selection:
            return
        values = self.table.item(selection[0], "values")
        self.selected_student_id = int(values[0])
        self.roll_var.set(values[1])
        self.name_var.set(values[2])
        self.course_var.set(values[3])
        self.email_var.set(values[4])
        self.phone_var.set(values[5])

    def clear_form(self):
        self.selected_student_id = None
        for variable in (
            self.roll_var, self.name_var, self.course_var,
            self.email_var, self.phone_var
        ):
            variable.set("")
        for selected in self.table.selection():
            self.table.selection_remove(selected)

    def clear_search(self):
        self.search_var.set("")
        self.load_students()


def main():
    root = tk.Tk()
    StudentManagementApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
