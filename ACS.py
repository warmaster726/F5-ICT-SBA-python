import tkinter as tk
from tkinter import messagebox
import DBS
import Main
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
FONT_OPTION = ("Segoe UI", 12)
FONT_TEXT   = ("Segoe UI", 12)

class Student:
    def __init__(self, sid: str):
        self.sid = sid
        self.total = 0

class SumAvg:
    def __init__(self, master):
        self.master = master
        master.title("Sum & Average Calculator")
        master.minsize(600, 500)
        master.configure(bg=DARK_BG)

        self.frame = tk.Frame(master, bg=FRAME_BG, padx=16, pady=16)
        self.frame.pack(fill="both", expand=True)

        # Header
        tk.Label(
            self.frame,
            text="Sum of Marks per Student",
            font=FONT_HEADER,
            bg=FRAME_BG,
            fg=TEXT_FG
        ).grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Year & Term selectors
        self._build_year_term_select()
        # Exam table selector
        self._build_exam_select()
        # Calculate / Return buttons
        self._build_buttons()
        # Results text area
        self._build_output_area()

        # grid weight
        for c in (0,1,2):
            self.frame.grid_columnconfigure(c, weight=1)

    def _build_year_term_select(self):
        curr_year = datetime.now().year
        years = [str(y) for y in range(curr_year, curr_year-5, -1)]
        self.year_var = tk.StringVar(value=years[0])
        self.term_var = tk.StringVar(value="1")

        # Year
        tk.Label(self.frame, text="Year:", font=FONT_LABEL,
                 bg=FRAME_BG, fg=TEXT_FG).grid(row=1, column=0, sticky="e", padx=8, pady=8)
        om_year = tk.OptionMenu(self.frame, self.year_var, *years)
        om_year.configure(font=FONT_OPTION, bg=ENTRY_BG, fg=TEXT_FG,
                          activebackground=BTN_ACTIVE_BG, activeforeground=TEXT_FG,
                          relief="flat")
        om_year.grid(row=1, column=1, sticky="w", padx=8, pady=8)

        # Term
        tk.Label(self.frame, text="Term:", font=FONT_LABEL,
                 bg=FRAME_BG, fg=TEXT_FG).grid(row=2, column=0, sticky="e", padx=8, pady=8)
        om_term = tk.OptionMenu(self.frame, self.term_var, "1", "2")
        om_term.configure(font=FONT_OPTION, bg=ENTRY_BG, fg=TEXT_FG,
                          activebackground=BTN_ACTIVE_BG, activeforeground=TEXT_FG,
                          relief="flat")
        om_term.grid(row=2, column=1, sticky="w", padx=8, pady=8)

    def _build_exam_select(self):
        # list exam tables that match year_term
        self.exam_var = tk.StringVar(value="")
        self._refresh_exam_list()

        tk.Label(self.frame, text="Exam Table:", font=FONT_LABEL,
                 bg=FRAME_BG, fg=TEXT_FG).grid(row=3, column=0, sticky="e", padx=8, pady=8)
        self.om_exam = tk.OptionMenu(self.frame, self.exam_var, *self.exam_tables)
        self.om_exam.configure(font=FONT_OPTION, bg=ENTRY_BG, fg=TEXT_FG,
                               activebackground=BTN_ACTIVE_BG, activeforeground=TEXT_FG,
                               relief="flat")
        self.om_exam.grid(row=3, column=1, columnspan=2, sticky="w", padx=8, pady=8)

    def _refresh_exam_list(self):
        # fetch all tables that start with exam_<year>_<term>
        y, t = self.year_var.get(), self.term_var.get()
        pattern = f"exam_{y}_{t}"
        rows = DBS.sqlrun(
            "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ?;",
            (pattern + "%",)
        )
        self.exam_tables = [r[0] for r in rows]
        if self.exam_tables:
            self.exam_var.set(self.exam_tables[0])
        else:
            self.exam_var.set("")

    def _build_buttons(self):
        btn_calc = tk.Button(
            self.frame,
            text="Calculate",
            font=FONT_BTN,
            bg=BTN_BG,
            fg=TEXT_FG,
            activebackground=BTN_ACTIVE_BG,
            activeforeground=TEXT_FG,
            relief="flat",
            command=self.calculate
        )
        btn_calc.grid(row=4, column=0, columnspan=2, pady=16, sticky="e")

        btn_return = tk.Button(
            self.frame,
            text="Return",
            font=FONT_BTN,
            bg=BTN_BG,
            fg=TEXT_FG,
            activebackground=BTN_ACTIVE_BG,
            activeforeground=TEXT_FG,
            relief="flat",
            command=self.return_to_main
        )
        btn_return.grid(row=4, column=2, pady=16, sticky="w")

    def _build_output_area(self):
        tk.Label(
            self.frame,
            text="SID    Total Marks",
            font=FONT_LABEL,
            bg=FRAME_BG,
            fg=TEXT_FG
        ).grid(row=5, column=0, columnspan=3, sticky="w", padx=8)

        self.output = tk.Text(
            self.frame,
            height=12,
            bg=PANEL_BG,
            fg=TEXT_FG,
            font=FONT_TEXT,
            relief="flat"
        )
        self.output.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=8, pady=(4,0))

    def calculate(self):
        # ensure exam list is up to date
        self._refresh_exam_list()

        tb = self.exam_var.get().strip()
        if not tb:
            messagebox.showerror("Error", "No exam table available for that Year/Term.")
            return

        # 1) fetch all SID
        sid_rows = DBS.sqlrun("SELECT SID FROM Students;", ())
        students = [Student(r[0]) for r in sid_rows]

        # 2) for each student, calculate total marks
        for stu in students:
            row = DBS.sqlrun(
                f"SELECT SUM(Mark) FROM {tb} WHERE SID = ?;",
                (stu.sid,)
            )
            stu.total = row[0][0] or 0

        # 3) display results
        self.output.delete("1.0", tk.END)
        if not students:
            self.output.insert(tk.END, "No students found.\n")
            return

        for stu in students:
            self.output.insert(tk.END, f"{stu.sid}\t{stu.total}\n")

    def return_to_main(self):
        self.frame.destroy()
        Main.F5ICTSBAApp(self.master)


if __name__ == "__main__":
    root = tk.Tk()
    SumAvg(root)
    root.mainloop()