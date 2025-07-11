import DBS, UMS, ACS
import pandas as pd
import openpyxl
import tkinter as tk
from tkinter import messagebox, filedialog
import datetime

# Dark mode color palette
DARK_BG        = "#2e2e2e"
PANEL_BG       = "#2e2e2e"
ENTRY_BG       = "#3e3e3e"
BTN_BG         = "#4d4d4d"
BTN_ACTIVE_BG  = "#5e5e5e"
TEXT_FG        = "#FFFFFF"
FRAME_BG = DARK_BG

# Standard fonts
FONT_HEADER = ("Segoe UI", 32, "bold")
FONT_BTN    = ("Segoe UI", 16)
FONT_SUB    = ("Segoe UI", 16, "bold")
FONT_SMALL  = ("Segoe UI", 12)

class F5ICTSBAApp:
    def __init__(self, master):
        self.master = master
        master.title("F5-ICT-SBA")
        master.minsize(800, 600)
        master.configure(bg=DARK_BG)

        # Main frame
        self.frame = tk.Frame(master, bg=FRAME_BG, padx=16, pady=16)
        self.frame.pack(fill="both", expand=True)

        # Header
        tk.Label(
            self.frame,
            text="EMEAS dev-0.0.21",
            font=FONT_HEADER,
            bg=PANEL_BG,
            fg=TEXT_FG
        ).pack(pady=(0, 20))

        # Button grid container
        button_container = tk.Frame(self.frame, bg=PANEL_BG)
        button_container.pack(expand=True, fill="both")

        for i in range(2):
            button_container.grid_rowconfigure(i, weight=1)
            button_container.grid_columnconfigure(i, weight=1)

        # Primary buttons
        def make_btn(text, cmd, row, col):
            return tk.Button(
                button_container,
                text=text,
                font=FONT_BTN,
                bg=BTN_BG,
                fg=TEXT_FG,
                activebackground=BTN_ACTIVE_BG,
                activeforeground=TEXT_FG,
                relief="flat",
                command=cmd
            ).grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        make_btn("Update Database", self.UDBS, 0, 0)
        make_btn("Upload Marksheets", self.UMS, 0, 1)
        make_btn("Start calculations", self.SumAvg, 1, 0)
        make_btn("Button 4", lambda: self.on_click(3), 1, 1)

    def on_click(self, index):
        print(f"Button {index + 1} clicked!")

    def UDBS(self):
        self.frame.destroy()
        UploadExcelPage(self.master)

    def UMS(self):
        self.frame.destroy()
        UMS.MarkSheetImportPage(self.master)

    def SumAvg(self):
        year = datetime.datetime.now().year
        pattern = f"exam_{year}%"
        try:
            rows = DBS.sqlrun(
                "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ?",
                (pattern,)
            )
        except Exception as e:
            messagebox.showerror("Error checking exam tables", str(e))
            return
        if not rows:
            messagebox.showerror(
                "Missing Exam Tables",
                f"No tables found in the year of {year}"
            )
            return
        self.frame.destroy()
        ACS.SumAvg(self.master)

class UploadExcelPage:
    def __init__(self, master):
        self.master = master
        master.title("Upload Excel Files")
        master.minsize(600, 300)
        master.configure(bg=DARK_BG)

        self.frame = tk.Frame(master, bg=FRAME_BG, padx=16, pady=16)
        self.frame.pack(fill="both", expand=True)

        # Two-column layout
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        # Left panel: Students
        student_frame = tk.Frame(self.frame, bg=PANEL_BG, relief="groove", borderwidth=2, padx=10, pady=10)
        student_frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

        tk.Label(
            student_frame,
            text="Students Table (Excel)",
            font=FONT_SUB,
            bg=PANEL_BG,
            fg=TEXT_FG
        ).pack(pady=(0, 10))

        self.students_file_var = tk.StringVar()
        tk.Entry(
            student_frame,
            textvariable=self.students_file_var,
            width=40,
            bg=ENTRY_BG,
            fg=TEXT_FG,
            insertbackground=TEXT_FG
        ).pack(pady=(0, 5))

        tk.Button(
            student_frame,
            text="Browse",
            font=FONT_SMALL,
            bg=BTN_BG,
            fg=TEXT_FG,
            activebackground=BTN_ACTIVE_BG,
            activeforeground=TEXT_FG,
            relief="flat",
            command=self.browse_students_file
        ).pack()

        # Right panel: Subjects
        subject_frame = tk.Frame(self.frame, bg=PANEL_BG, relief="groove", borderwidth=2, padx=10, pady=10)
        subject_frame.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)

        tk.Label(
            subject_frame,
            text="Subjects Table (Excel)",
            font=FONT_SUB,
            bg=PANEL_BG,
            fg=TEXT_FG
        ).pack(pady=(0, 10))

        self.subjects_file_var = tk.StringVar()
        tk.Entry(
            subject_frame,
            textvariable=self.subjects_file_var,
            width=40,
            bg=ENTRY_BG,
            fg=TEXT_FG,
            insertbackground=TEXT_FG
        ).pack(pady=(0, 5))

        tk.Button(
            subject_frame,
            text="Browse",
            font=FONT_SMALL,
            bg=BTN_BG,
            fg=TEXT_FG,
            activebackground=BTN_ACTIVE_BG,
            activeforeground=TEXT_FG,
            relief="flat",
            command=self.browse_subjects_file
        ).pack()

        # Submit & Return buttons
        tk.Button(
            self.frame,
            text="Submit",
            font=FONT_BTN,
            bg=BTN_BG,
            fg=TEXT_FG,
            activebackground=BTN_ACTIVE_BG,
            activeforeground=TEXT_FG,
            relief="flat",
            command=self.on_submit
        ).grid(row=1, column=0, pady=20, sticky="e")

        tk.Button(
            self.frame,
            text="Return",
            font=FONT_BTN,
            bg=BTN_BG,
            fg=TEXT_FG,
            activebackground=BTN_ACTIVE_BG,
            activeforeground=TEXT_FG,
            relief="flat",
            command=self.on_return
        ).grid(row=1, column=1, pady=20, sticky="w")

    def browse_students_file(self):
        path = filedialog.askopenfilename(
            title="Select Students Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls *.xlsm")]
        )
        if path:
            self.students_file_var.set(path)
        else:
            messagebox.showinfo("No file selected", "No Students file was selected.")

    def browse_subjects_file(self):
        path = filedialog.askopenfilename(
            title="Select Subjects Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls *.xlsm")]
        )
        if path:
            self.subjects_file_var.set(path)
        else:
            messagebox.showinfo("No file selected", "No Subjects file was selected.")

    def on_return(self):
        self.frame.destroy()
        F5ICTSBAApp(self.master)

    def on_submit(self):
        if not self.students_file_var.get() or not self.subjects_file_var.get():
            messagebox.showerror("Error", "Please select both Students and Subjects Excel files")
            return

        # Students import
        try:
            df_students = pd.read_excel(self.students_file_var.get())
            for _, row in df_students.iterrows():
                DBS.sqlrun(
                    "insert into Students (SID, Class, Name, CNO) values (?, ?, ?, ?)",
                    (row['SID'], row['Class'], row['Name'], row['CNO'])
                )
            messagebox.showinfo("Success", "Students table successfully updated")
        except Exception as e:
            messagebox.showerror("Error updating Students table", str(e))
            return

        # Subjects import
        try:
            DBS.sqlrun("delete from Subjects")
            df_subjects = pd.read_excel(self.subjects_file_var.get())
            for _, row in df_subjects.iterrows():
                DBS.sqlrun(
                    "insert into Subjects (SID, Class, Name, CNO) values (?, ?, ?, ?)",
                    (row['SID'], row['Class'], row['Name'], row['CNO'])
                )
            messagebox.showinfo("Success", "Subjects table successfully updated")
        except Exception as e:
            messagebox.showerror("Error updating Subjects table", str(e))
            return

        self.on_return()


if __name__ == "__main__":
    root = tk.Tk()
    app = F5ICTSBAApp(root)
    if DBS.checking():
        messagebox.showwarning("Warning", "Database needs to be updated")
        app.frame.destroy()
        app = UploadExcelPage(root)
    root.mainloop()