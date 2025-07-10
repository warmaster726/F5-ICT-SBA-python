import DBS, Main
import pandas as pd
import openpyxl
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime

# === Dark Mode Palette ===
DARK_BG        = "#2e2e2e"
FRAME_BG       = DARK_BG
PANEL_BG       = "#3b3b3b"
ENTRY_BG       = "#3e3e3e"
BTN_BG         = "#4d4d4d"
BTN_ACTIVE_BG  = "#5e5e5e"
TEXT_FG        = "#FFFFFF"

# === Fonts ===
FONT_HEADER = ("Segoe UI", 24, "bold")
FONT_LABEL  = ("Segoe UI", 14)
FONT_BTN    = ("Segoe UI", 14)
FONT_ENTRY  = ("Segoe UI", 14)
FONT_OPTION = ("Segoe UI", 12)

class MarkSheetImportPage:
    def __init__(self, master):
        self.master = master
        master.title("Upload Exam Mark Sheet")
        master.minsize(600, 450)
        master.configure(bg=DARK_BG)

        self.frame = tk.Frame(master, padx=16, pady=16, bg=FRAME_BG)
        self.frame.pack(fill="both", expand=True)

        # Header
        tk.Label(
            self.frame,
            text="Upload Exam Mark Sheet",
            font=FONT_HEADER,
            bg=FRAME_BG,
            fg=TEXT_FG
        ).grid(row=0, column=0, columnspan=3, pady=(0, 20))

        current_year = datetime.now().year
        self.year_options = [str(y) for y in range(current_year, current_year - 5, -1)]
        self.year_var = tk.StringVar(value=self.year_options[0])
        self.term_var = tk.StringVar(value="1")
        self.exam_var = tk.StringVar(value="Exam")
        self.subject_var = tk.StringVar(value=" --- ")
        self.papers_var = tk.StringVar()
        self.marksheet_file_var = tk.StringVar()

        # Form fields
        self.add_label_option("Year:", self.year_var, self.year_options, 1)
        self.add_label_option("Term:", self.term_var, ["1", "2"], 2)
        self.add_label_option("Exam:", self.exam_var, ["Exam"], 3)

        exam_options = DBS.sqlrun("Select SubCode from Subjects;")
        exam_options = [row[0] for row in exam_options]
        self.add_label_option("Subject:", self.subject_var, exam_options, 4)

        self.add_label_entry("Papers:", self.papers_var, 5)
        self.add_label_file_picker("Marksheet (Excel):", self.marksheet_file_var, 6)

        # Action buttons
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
        ).grid(row=7, column=0, columnspan=2, pady=20, sticky="e")

        tk.Button(
            self.frame,
            text="Return",
            font=FONT_BTN,
            bg=BTN_BG,
            fg=TEXT_FG,
            activebackground=BTN_ACTIVE_BG,
            activeforeground=TEXT_FG,
            relief="flat",
            command=self.return_to_main
        ).grid(row=7, column=2, pady=20, sticky="w")

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=3)
        self.frame.grid_columnconfigure(2, weight=1)

    def add_label_option(self, text, variable, options, row):
        tk.Label(
            self.frame,
            text=text,
            font=FONT_LABEL,
            bg=FRAME_BG,
            fg=TEXT_FG
        ).grid(row=row, column=0, sticky="e", padx=8, pady=8)

        option_menu = tk.OptionMenu(self.frame, variable, *options)
        option_menu.configure(font=FONT_OPTION, bg=ENTRY_BG, fg=TEXT_FG,
                              activebackground=BTN_ACTIVE_BG, activeforeground=TEXT_FG,
                              relief="flat")
        option_menu.grid(row=row, column=1, sticky="w", padx=8, pady=8)

    def add_label_entry(self, text, variable, row):
        tk.Label(
            self.frame,
            text=text,
            font=FONT_LABEL,
            bg=FRAME_BG,
            fg=TEXT_FG
        ).grid(row=row, column=0, sticky="e", padx=8, pady=8)

        tk.Entry(
            self.frame,
            textvariable=variable,
            font=FONT_ENTRY,
            width=30,
            bg=ENTRY_BG,
            fg=TEXT_FG,
            insertbackground=TEXT_FG
        ).grid(row=row, column=1, sticky="w", padx=8, pady=8)

    def add_label_file_picker(self, text, variable, row):
        tk.Label(
            self.frame,
            text=text,
            font=FONT_LABEL,
            bg=FRAME_BG,
            fg=TEXT_FG
        ).grid(row=row, column=0, sticky="e", padx=8, pady=8)

        tk.Entry(
            self.frame,
            textvariable=variable,
            font=FONT_ENTRY,
            width=40,
            bg=ENTRY_BG,
            fg=TEXT_FG,
            insertbackground=TEXT_FG
        ).grid(row=row, column=1, sticky="w", padx=8, pady=8)

        tk.Button(
            self.frame,
            text="Browse",
            font=FONT_OPTION,
            bg=BTN_BG,
            fg=TEXT_FG,
            activebackground=BTN_ACTIVE_BG,
            activeforeground=TEXT_FG,
            relief="flat",
            command=self.browse_marksheet_file
        ).grid(row=row, column=2, padx=8, pady=8)

    def browse_marksheet_file(self):
        path = filedialog.askopenfilename(
            title="Select Marksheet Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls *.xlsm")]
        )
        if path:
            self.marksheet_file_var.set(path)
        else:
            messagebox.showinfo("No file selected", "No marksheet file was selected.")

    def on_submit(self):
        year_str = self.year_var.get().strip()
        term = self.term_var.get().strip()
        exam = self.exam_var.get().strip()
        subject = self.subject_var.get().strip()
        papers = self.papers_var.get().strip()
        marksheet_file = self.marksheet_file_var.get().strip()

        if not all([year_str, term, exam, subject, papers, marksheet_file]):
            messagebox.showerror("Error", "Please fill in all fields and select a marksheet file.")
            return

        try:
            year = int(year_str)
        except ValueError:
            messagebox.showerror("Error", "Year must be a valid integer.")
            return

        try:
            df = pd.read_excel(marksheet_file)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read Excel file: {e}")
            return

        tb_name = f"exam_{year_str}_{term}"
        DBS.sqlrun(
            f"""CREATE TABLE IF NOT EXISTS {tb_name} (
                Exam varchar(255) NOT NULL,
                Subject varchar(255) NOT NULL,
                Papers Integer NOT NULL,
                SID char(5) NOT NULL,
                Mark Integer,
                PRIMARY KEY (Subject, Papers, SID))""",
            ()
        )

        try:
            for _, row in df.iterrows():
                student_id = str(row['StudentID'])
                mark = int(row['Mark'])
                DBS.sqlrun(
                    f"INSERT INTO {tb_name} (Exam, Subject, Papers, SID, Mark) VALUES (?, ?, ?, ?, ?)",
                    (exam, subject, papers, student_id, mark)
                )
        except Exception as e:
            messagebox.showerror("Error", f"Error updating MarkSheet table: {e}")
            return

        messagebox.showinfo("Success", "Marksheet successfully updated.")
        self.return_to_main()

    def return_to_main(self):
        self.frame.destroy()
        Main.F5ICTSBAApp(self.master)

if __name__ == "__main__":
    root = tk.Tk()
    app = MarkSheetImportPage(root)
    root.mainloop()