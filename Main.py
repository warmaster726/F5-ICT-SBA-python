import DBS
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog

class F5ICTSBAApp:
    def __init__(self, master):
        self.master = master
        master.title("F5-ICT-SBA")
        master.minsize(800, 600)

        # Main container with padding
        container = tk.Frame(master, padx=16, pady=16)
        container.pack(fill="both", expand=True)

        # Header label
        tk.Label(
            container,
            text="F5 ICT SBA",
            font=("Arial", 32, "bold")
        ).pack(pady=(0, 20))

        # Button grid container
        button_container = tk.Frame(container)
        button_container.pack(expand=True, fill="both")

        # Configure grid layout (2x2)
        for i in range(2):
            button_container.grid_rowconfigure(i, weight=1)
            button_container.grid_columnconfigure(i, weight=1)

        # Create four buttons
        for i in range(4):
            tk.Button(
                button_container,
                text=f"Button {i + 1}",
                font=("Arial", 16),
                command=lambda i=i: self.on_click(i)
            ).grid(row=i // 2, column=i % 2, padx=8, pady=8, sticky="nsew")

    def on_click(self, index):
        print(f"Button {index + 1} clicked!")

class UploadExcelPage:
    def __init__(self, master):
        self.master = master
        master.title("Upload Excel Files")
        master.minsize(600, 300)

        # Main container with padding
        container = tk.Frame(master, padx=16, pady=16)
        container.pack(fill="both", expand=True)

        # Configure container for two columns of equal weight
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        # --- Left Column: Students Table ---
        student_frame = tk.Frame(container, relief="groove", borderwidth=2, padx=10, pady=10)
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
        subject_frame = tk.Frame(container, relief="groove", borderwidth=2, padx=10, pady=10)
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
            container,
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
        file_path = filedialog.askopenfilename(
            title="Select Students Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls *.xlsm")]
        )
        if file_path:
            self.students_file_var.set(file_path)
        else:
            messagebox.showinfo("No file selected", "No Students file was selected.")

    def browse_subjects_file(self):
        """
        Opens a file dialog to select an Excel file for the Subjects table.
        The file dialog now accepts .xlsx, .xls, and .xlsm files.
        """
        file_path = filedialog.askopenfilename(
            title="Select Subjects Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls *.xlsm")]
        )
        if file_path:
            self.subjects_file_var.set(file_path)
        else:
            messagebox.showinfo("No file selected", "No Subjects file was selected.")
    
    def on_submit(self):
        # DBS.sqlrun("delete from Students")
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = F5ICTSBAApp(root)
    if DBS.checking() == True:
        messagebox.showwarning("Warning", "Database needs to be updated")
        for widget in root.winfo_children():
            widget.destroy()
        app = UploadExcelPage(root)
    root.mainloop()
