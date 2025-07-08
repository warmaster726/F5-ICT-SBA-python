import DBS, Main
import pandas as pd
import openpyxl
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime

class MarkSheetImportPage:
    def __init__(self, master):
        self.master = master
        master.title("Upload Exam Mark Sheet")
        master.minsize(600, 450)
        self.frame = tk.Frame(master, padx=16, pady=16)
        self.frame.pack(fill="both", expand=True)
        tk.Label(self.frame, text="Upload Exam Mark Sheet", font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=3, pady=(0,20))
        tk.Label(self.frame, text="Year:", font=("Arial", 14)).grid(row=1, column=0, sticky="e", padx=8, pady=8)
        current_year = datetime.now().year
        self.year_options = [str(y) for y in range(current_year, current_year - 5, -1)]
        self.year_var = tk.StringVar()
        self.year_var.set(self.year_options[0])
        tk.OptionMenu(self.frame, self.year_var, *self.year_options).grid(row=1, column=1, sticky="w", padx=8, pady=8)
        tk.Label(self.frame, text="Term:", font=("Arial", 14)).grid(row=2, column=0, sticky="e", padx=8, pady=8)
        self.term_var = tk.StringVar()
        self.term_var.set("1")
        term_options = ["1", "2"]
        tk.OptionMenu(self.frame, self.term_var, *term_options).grid(row=2, column=1, sticky="w", padx=8, pady=8)
        tk.Label(self.frame, text="Exam:", font=("Arial", 14)).grid(row=3, column=0, sticky="e", padx=8, pady=8)
        self.exam_var = tk.StringVar()
        self.exam_var.set("Exam")
        exam_options = ["Exam"]
        tk.OptionMenu(self.frame, self.exam_var, *exam_options).grid(row=3, column=1, sticky="w", padx=8, pady=8)
        tk.Label(self.frame, text="Subject:", font=("Arial", 14)).grid(row=4, column=0, sticky="e", padx=8, pady=8)
        self.subject_var = tk.StringVar()
        exam_options = DBS.sqlrun("Select SubCode from Subjects;")
        exam_options = [row[0] for row in exam_options]
        self.subject_var.set(" --- ")
        tk.OptionMenu(self.frame, self.subject_var, *exam_options).grid(row=4, column=1, sticky="w", padx=8, pady=8)
        tk.Label(self.frame, text="Papers:", font=("Arial", 14)).grid(row=5, column=0, sticky="e", padx=8, pady=8)
        self.papers_var = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.papers_var, font=("Arial", 14)).grid(row=5, column=1, sticky="w", padx=8, pady=8)
        tk.Label(self.frame, text="Marksheet (Excel):", font=("Arial", 14)).grid(row=6, column=0, sticky="e", padx=8, pady=8)
        self.marksheet_file_var = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.marksheet_file_var, font=("Arial", 14), width=40).grid(row=6, column=1, sticky="w", padx=8, pady=8)
        tk.Button(self.frame, text="Browse", font=("Arial", 12), command=self.browse_marksheet_file).grid(row=6, column=2, padx=8, pady=8)
        submit_btn = tk.Button(self.frame, text="Submit", font=("Arial", 14), command=self.on_submit)
        submit_btn.grid(row=7, column=0, columnspan=2, pady=20, sticky="e")
        return_btn = tk.Button(self.frame, text="Return", font=("Arial", 14), command=self.return_to_main)
        return_btn.grid(row=7, column=2, pady=20, sticky="w")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=3)
        self.frame.grid_columnconfigure(2, weight=1)

    def browse_marksheet_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Marksheet Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls *.xlsm")]
        )
        if file_path:
            self.marksheet_file_var.set(file_path)
        else:
            messagebox.showinfo("No file selected", "No marksheet file was selected.")

    def on_submit(self):
        year_str = self.year_var.get().strip()
        term = self.term_var.get().strip()
        exam = self.exam_var.get().strip()
        subject = self.subject_var.get().strip()
        papers = self.papers_var.get().strip()
        marksheet_file = self.marksheet_file_var.get().strip()
        if not (year_str and term and exam and subject and papers and marksheet_file):
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
            f"CREATE TABLE IF NOT EXISTS {tb_name} (Exam varchar(255) NOT NULL, Subject varchar(255) NOT NULL, Papers Integer NOT NULL, SID char(5) NOT NULL, Mark Integer, PRIMARY KEY (Subject, Papers, SID))", ()
        )
        try:
            for index, row in df.iterrows():
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
    Main.F5ICTSBAApp(root)