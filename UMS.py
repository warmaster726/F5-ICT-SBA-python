import DBS
import pandas as pd
import openpyxl
import tkinter as tk
from tkinter import messagebox, filedialog

class MarkSheetImportPage:
    def __init__(self, master):
        self.master = master
        master.title("Upload Exam Mark Sheet")
        master.minsize(600, 400)
        
        # Main frame with padding
        self.frame = tk.Frame(master, padx=16, pady=16)
        self.frame.pack(fill="both", expand=True)

        # Header label
        tk.Label(
            self.frame,
            text="Upload Exam Mark Sheet",
            font=("Arial", 24, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # --- Exam Parameters ---
        # Year
        tk.Label(self.frame, text="Year:", font=("Arial", 14)).grid(row=1, column=0, sticky="e", padx=8, pady=8)
        self.year_var = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.year_var, font=("Arial", 14)).grid(row=1, column=1, sticky="w", padx=8, pady=8)

        # Term
        tk.Label(self.frame, text="Term:", font=("Arial", 14)).grid(row=2, column=0, sticky="e", padx=8, pady=8)
        self.term_var = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.term_var, font=("Arial", 14)).grid(row=2, column=1, sticky="w", padx=8, pady=8)

        # Exam Name
        tk.Label(self.frame, text="Exam Name:", font=("Arial", 14)).grid(row=3, column=0, sticky="e", padx=8, pady=8)
        self.exam_name_var = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.exam_name_var, font=("Arial", 14)).grid(row=3, column=1, sticky="w", padx=8, pady=8)

        # Subject
        tk.Label(self.frame, text="Subject:", font=("Arial", 14)).grid(row=4, column=0, sticky="e", padx=8, pady=8)
        self.subject_var = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.subject_var, font=("Arial", 14)).grid(row=4, column=1, sticky="w", padx=8, pady=8)

        # Papers
        tk.Label(self.frame, text="Papers:", font=("Arial", 14)).grid(row=5, column=0, sticky="e", padx=8, pady=8)
        self.papers_var = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.papers_var, font=("Arial", 14)).grid(row=5, column=1, sticky="w", padx=8, pady=8)

        # --- Marksheet File Selection ---
        tk.Label(self.frame, text="Marksheet (Excel):", font=("Arial", 14)).grid(row=6, column=0, sticky="e", padx=8, pady=8)
        self.marksheet_file_var = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.marksheet_file_var, font=("Arial", 14), width=40)\
            .grid(row=6, column=1, sticky="w", padx=8, pady=8)
        tk.Button(self.frame,
                  text="Browse",
                  font=("Arial", 12),
                  command=self.browse_marksheet_file)\
            .grid(row=6, column=2, padx=8, pady=8)

        # Submit button
        tk.Button(self.frame,
                  text="Submit",
                  font=("Arial", 14),
                  command=self.on_submit)\
            .grid(row=7, column=0, columnspan=3, pady=20)

        # Optional: adjust grid column weights for better spacing
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=3)

    def browse_marksheet_file(self):
        """
        Opens a file dialog to select an Excel file for the mark sheet.
        Accepted extensions are .xlsx, .xls, and .xlsm.
        """
        file_path = filedialog.askopenfilename(
            title="Select Marksheet Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls *.xlsm")]
        )
        if file_path:
            self.marksheet_file_var.set(file_path)
        else:
            messagebox.showinfo("No file selected", "No marksheet file was selected.")

    def on_submit(self):
        # Gather exam parameters and file path
        year = self.year_var.get().strip()
        term = self.term_var.get().strip()
        exam_name = self.exam_name_var.get().strip()
        subject = self.subject_var.get().strip()
        papers = self.papers_var.get().strip()
        marksheet_file = self.marksheet_file_var.get().strip()

        # Check that every field is provided
        if not (year and term and exam_name and subject and papers and marksheet_file):
            messagebox.showerror("Error", "Please fill in all fields and select a marksheet file.")
            return

        # Attempt to load the Excel file
        try:
            df = pd.read_excel(marksheet_file)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read Excel file: {e}")
            return

        # Try inserting each record in the marksheet into the database.
        # Assumption: the Excel file has columns "StudentID" and "Mark"
        try:
            for index, row in df.iterrows():
                student_id = row['StudentID']
                mark = row['Mark']
                DBS.sqlrun(
                    "insert into MarkSheet (Year, Term, ExamName, Subject, Papers, StudentID, Mark) values (?, ?, ?, ?, ?, ?, ?)",
                    (year, term, exam_name, subject, papers, student_id, mark)
                )
        except Exception as e:
            messagebox.showerror("Error", f"Error updating MarkSheet table: {e}")
            return

        messagebox.showinfo("Success", "Marksheet successfully updated.")
        
        # Optionally, clear the form or navigate back to a main page.
        self.frame.destroy()
        # If you have a main or dashboard page, instantiate it here.
        # For example:
        # MainApp(self.master)

if __name__ == "__main__":
    root = tk.Tk()
    app = MarkSheetImportPage(root)
    root.mainloop()