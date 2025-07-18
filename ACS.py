import tkinter as tk
from tkinter import messagebox
import DBS
import Main
from datetime import datetime

DARK_BG        = "#2e2e2e"
FRAME_BG       = DARK_BG
PANEL_BG       = "#3b3b3b"
ENTRY_BG       = "#3e3e3e"
BTN_BG         = "#4d4d4d"
BTN_ACTIVE_BG  = "#5e5e5e"
TEXT_FG        = "#FFFFFF"

FONT_HEADER = ("Segoe UI", 24, "bold")
FONT_LABEL  = ("Segoe UI", 14)
FONT_BTN    = ("Segoe UI", 14)
FONT_OPTION = ("Segoe UI", 12)
FONT_TEXT   = ("Segoe UI", 12)

class Student:
    def __init__(self, sid: str):
        self.sid = sid
        self.total = 0
        self.count = 0
        self.average = 0.0

    def finalize(self):
        if self.count > 0:
            self.average = self.total / self.count
        else:
            self.average = 0


class SumAvg:
    def __init__(self, master):
        self.master = master
        master.title("Calculation Service")
        master.minsize(600, 500)
        master.configure(bg=DARK_BG)

        self.frame = tk.Frame(master, bg=FRAME_BG, padx=16, pady=16)
        self.frame.pack(fill="both", expand=True)

        tk.Label(
            self.frame,
            text="Calculation Details",
            font=FONT_HEADER,
            bg=FRAME_BG,
            fg=TEXT_FG
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        self._build_year_term_select()
        self._build_buttons()
        self._build_output_area()

        for c in (0, 1):
            self.frame.grid_columnconfigure(c, weight=1)

    def _build_year_term_select(self):
        curr_year = datetime.now().year
        years = [str(y) for y in range(curr_year, curr_year - 5, -1)]
        self.year_var = tk.StringVar(value=years[0])
        self.term_var = tk.StringVar(value="1")

        tk.Label(
            self.frame, text="Year:", font=FONT_LABEL,
            bg=FRAME_BG, fg=TEXT_FG
        ).grid(row=1, column=0, sticky="e", padx=8, pady=8)
        om_year = tk.OptionMenu(self.frame, self.year_var, *years)
        om_year.configure(
            font=FONT_OPTION, bg=ENTRY_BG, fg=TEXT_FG,
            activebackground=BTN_ACTIVE_BG, activeforeground=TEXT_FG,
            relief="flat"
        )
        om_year.grid(row=1, column=1, sticky="w", padx=8, pady=8)

        tk.Label(
            self.frame, text="Term:", font=FONT_LABEL,
            bg=FRAME_BG, fg=TEXT_FG
        ).grid(row=2, column=0, sticky="e", padx=8, pady=8)
        om_term = tk.OptionMenu(self.frame, self.term_var, "1", "2")
        om_term.configure(
            font=FONT_OPTION, bg=ENTRY_BG, fg=TEXT_FG,
            activebackground=BTN_ACTIVE_BG, activeforeground=TEXT_FG,
            relief="flat"
        )
        om_term.grid(row=2, column=1, sticky="w", padx=8, pady=8)

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
        btn_calc.grid(row=3, column=0, pady=16, sticky="e", padx=8)

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
        btn_return.grid(row=3, column=1, pady=16, sticky="w", padx=8)

    def _build_output_area(self):
        tk.Label(
            self.frame,
            text="SID    Total Marks    Average",
            font=FONT_LABEL,
            bg=FRAME_BG,
            fg=TEXT_FG
        ).grid(row=4, column=0, columnspan=2, sticky="w", padx=8)
        self.output = tk.Text(
            self.frame,
            height=12,
            bg=PANEL_BG,
            fg=TEXT_FG,
            font=FONT_TEXT,
            relief="flat"
        )
        self.output.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=8, pady=(4, 0))

    def calculate(self):
        y, t = self.year_var.get(), self.term_var.get()
        tb = f"exam_{y}_{t}"
        try:
            exists = DBS.sqlrun(
                "SELECT name FROM sqlite_master WHERE type='table' AND name = ?;",
                (tb,)
            )
        except Exception as e:
            messagebox.showerror("Error checking exam tables", str(e))
            return
        if not exists:
            messagebox.showerror("Error", f"No table named '{tb}' found")
            return

        sid_rows = DBS.sqlrun("SELECT DISTINCT SID FROM Students;", ())
        students = {r[0] : Student(r[0]) for r in sid_rows}

        marks = DBS.sqlrun(f"SELECT SID, Mark FROM {tb};", ())

        for sid, mark in marks:
            student = students.get(sid)
            if not student:
                continue
            student.total += mark
            student.count += 1

        for stu in students.values():
            stu.finalize()

        self.output.delete("1.0", tk.END)
        if not students:
            self.output.insert(tk.END, "No students found.\n")
        else:
            for stu in students.values():
                self.output.insert(tk.END, f"{stu.sid}\t{stu.total}\t{stu.average:.2f}\n")

        messagebox.showinfo("Complete", "All calculations are done.")
        self.return_to_main()

    def return_to_main(self):
        self.frame.destroy()
        Main.F5ICTSBAApp(self.master)

if __name__ == "__main__":
    root = tk.Tk()
    SumAvg(root)
    root.mainloop()