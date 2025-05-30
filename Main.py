import DBS, UMS
import pandas as pd
import openpyxl
import tkinter as tk
from tkinter import messagebox, filedialog

class F5ICTSBAApp:
    def __init__(self, master):
        self.master = master
        master.title("F5-ICT-SBA")
        master.minsize(800, 600)

        # Main self.frame with padding
        self.frame = tk.Frame(master, padx=16, pady=16)
        self.frame.pack(fill="both", expand=True)

        # Header label
        tk.Label(
            self.frame,
            text="F5 ICT SBA",
            font=("Arial", 32, "bold")
        ).pack(pady=(0, 20))

        # Button grid self.frame
        button_container = tk.Frame(self.frame)
        button_container.pack(expand=True, fill="both")

        # Configure grid layout (2x2)
        for i in range(2):
            button_container.grid_rowconfigure(i, weight=1)
            button_container.grid_columnconfigure(i, weight=1)

        # Create four buttons
        tk.Button(
            button_container,
            text=f"Update Database",
            font=("Arial", 16),
            command=self.UDBS
        ).grid(row=0, column=0, padx=8, pady=8, sticky="nsew")

        tk.Button(
            button_container,
            text=f"Upload Marksheets",
            font=("Arial", 16),
            command=self.UMS
        ).grid(row=0, column=1, padx=8, pady=8, sticky="nsew")

        for i in range(2,4):
            tk.Button(
                button_container,
                text=f"Button {i + 1}",
                font=("Arial", 16),
                command=lambda i=i: self.on_click(i)
            ).grid(row=i // 2, column=i % 2, padx=8, pady=8, sticky="nsew")

    def on_click(self, index):
        print(f"Button {index + 1} clicked!")

    def UDBS(self):
        self.frame.destroy()
        UploadExcelPage(self.master)

    def UMS(self):
        self.frame.destroy()
        UMS.MarkSheetImportPage(self.master)

class UploadExcelPage:
    def __init__(self, master):
        self.master = master
        master.title("Upload Excel Files")
        master.minsize(600, 300)

        # Main self.frame with padding
        self.frame = tk.Frame(master, padx=16, pady=16)
        self.frame.pack(fill="both", expand=True)

        # Configure self.frame for two columns of equal weight
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        # --- Left Column: Students Table ---
        student_frame = tk.Frame(self.frame, relief="groove", borderwidth=2, padx=10, pady=10)
        student_frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

        # Header for the Students panel
        tk.Label(student_frame,
                 text="Students Table (Excel)",
                 font=("Arial", 16, "bold")
                ).pack(pady=(0, 10))

        # Entry field to display the chosen file path
        self.students_file_var = tk.StringVar()
        tk.Entry(student_frame, textvariable=self.students_file_var, width=40).pack(pady=(0, 5))

        # Browse button for Students table file selection
        tk.Button(student_frame,
                  text="Browse",
                  font=("Arial", 12),
                  command=self.browse_students_file
                 ).pack()

        # --- Right Column: Subjects Table ---
        subject_frame = tk.Frame(self.frame, relief="groove", borderwidth=2, padx=10, pady=10)
        subject_frame.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)

        # Header for the Subjects panel
        tk.Label(subject_frame,
                 text="Subjects Table (Excel)",
                 font=("Arial", 16, "bold")
                ).pack(pady=(0, 10))

        # Entry field to display the chosen file path
        self.subjects_file_var = tk.StringVar()
        tk.Entry(subject_frame, textvariable=self.subjects_file_var, width=40).pack(pady=(0, 5))

        # Browse button for Subjects table file selection
        tk.Button(subject_frame,
                  text="Browse",
                  font=("Arial", 12),
                  command=self.browse_subjects_file
                 ).pack()
        
        submit_button = tk.Button(
            self.frame,
            text="Submit",
            font=("Arial", 14),
            command=self.on_submit
        )
        submit_button.grid(row=1, column=0, columnspan=2, pady=20)


    def browse_students_file(self):
        """
        Opens a file dialog to select an Excel file for the Students table.
        The file dialog now accepts .xlsx, .xls, and .xlsm files.
        """
        file_path_students = filedialog.askopenfilename(
            title="Select Students Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls *.xlsm")]
        )
        if file_path_students:
            self.students_file_var.set(file_path_students)
        else:
            messagebox.showinfo("No file selected", "No Students file was selected.")

    def browse_subjects_file(self):
        """
        Opens a file dialog to select an Excel file for the Subjects table.
        The file dialog now accepts .xlsx, .xls, and .xlsm files.
        """
        file_path_subjects = filedialog.askopenfilename(
            title="Select Subjects Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls *.xlsm")]
        )
        if file_path_subjects:
            self.subjects_file_var.set(file_path_subjects)
        else:
            messagebox.showinfo("No file selected", "No Subjects file was selected.")
    
    def on_submit(self):
        if self.students_file_var.get() and self.subjects_file_var.get():
            # Process Students table
            df = pd.read_excel(self.students_file_var.get())
            for index, row in df.iterrows():
                sid = row['SID']
                class_ = row['Class']
                name = row['Name']
                cno = row['CNO']
            try:
                DBS.sqlrun("insert into Students (SID, Class, Name, CNO) values (?, ?, ?, ?)", (sid, class_, name, cno))
                messagebox.showinfo("Success", "Students table successfully updated")
            except Exception as e:
                messagebox.showerror("Error", f"Error updating Students table: {e}")
                return

            # Process Subjects table
            DBS.sqlrun("delete from Subjects")
            df_subjects = pd.read_excel(self.subjects_file_var.get())
            for index, row in df_subjects.iterrows():
                sid = row['SID']
                class_ = row['Class']
                name = row['Name']
                cno = row['CNO']
                try:
                    DBS.sqlrun("insert into Subjects (SID, Class, Name, CNO) values (?, ?, ?, ?)", (sid, class_, name, cno))
                except Exception as e:
                    messagebox.showerror("Error", f"Error updating Subjects table: {e}")
                    return
            messagebox.showinfo("Success", "Subjects table successfully updated")

            # After successful submission, return to the main page:
            self.frame.destroy()
            F5ICTSBAApp(self.master)
        else:
            messagebox.showerror("Error", "Please select both Students and Subjects Excel files")

if __name__ == "__main__":
    root = tk.Tk()
    app = F5ICTSBAApp(root)
    if DBS.checking() == True:
        messagebox.showwarning("Warning", "Database needs to be updated")
        app.frame.destroy()
        app = UploadExcelPage(root)        
    root.mainloop()
