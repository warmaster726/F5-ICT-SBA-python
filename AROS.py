import tkinter as tk
from tkinter import filedialog
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

class ReportGenerator:
	def __init__(self, master):
		self.master = master
		master.title("Report Generation Service")
		master.minsize(600, 500)
		master.configure(bg=DARK_BG)

		self.frame = tk.Frame(master, bg=FRAME_BG, padx=16, pady=16)
		self.frame.pack(fill="both", expand=True)

		tk.Label(
			self.frame,
			text="Batch Report Generator",
			font=FONT_HEADER,
			bg=FRAME_BG,
			fg=TEXT_FG
		).grid(row=0, column=0, columnspan=3, pady=(0, 20))

		# Year and term selection
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
		om_year.grid(row=1, column=1, columnspan=2, sticky="w", padx=8, pady=8)

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
		om_term.grid(row=2, column=1, columnspan=2, sticky="w", padx=8, pady=8)

		# Template selector
		tk.Label(
			self.frame, text="Template (.dotx):", font=FONT_LABEL,
			bg=FRAME_BG, fg=TEXT_FG
		).grid(row=3, column=0, sticky="e", padx=8, pady=8)

		tk.Label(
			self.frame, text="RCTemplate.dotx", font=FONT_TEXT,
			bg=FRAME_BG, fg=TEXT_FG
		).grid(row=3, column=1, columnspan=2, sticky="w", padx=8, pady=8)

		# Action buttons
		btn_gen = tk.Button(
			self.frame, text="Generate Reports",
			font=FONT_BTN, bg=BTN_BG, fg=TEXT_FG,
			activebackground=BTN_ACTIVE_BG, activeforeground=TEXT_FG,
			relief="flat", command=self._generate_reports
		)
		btn_gen.grid(row=4, column=1, sticky="e", padx=8, pady=16)

		btn_ret = tk.Button(
			self.frame, text="Return",
			font=FONT_BTN, bg=BTN_BG, fg=TEXT_FG,
			activebackground=BTN_ACTIVE_BG, activeforeground=TEXT_FG,
			relief="flat", command=self._return_to_main
		)
		btn_ret.grid(row=4, column=2, sticky="w", padx=8, pady=16)

		# Output area
		tk.Label(
			self.frame, text="Log / Preview",
			font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_FG
		).grid(row=5, column=0, columnspan=3, sticky="w", padx=8)
		self.output = tk.Text(
			self.frame, height=12,
			bg=PANEL_BG, fg=TEXT_FG, font=FONT_TEXT,
			relief="flat"
		)
		self.output.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=8, pady=(4, 0))

		for c in range(3):
			self.frame.grid_columnconfigure(c, weight=1)

	def _generate_reports(self):
		self.output.delete("1.0", tk.END)
		self.output.insert(tk.END, "Report generation logic is not yet implemented.\n")

	def _return_to_main(self):
		self.frame.destroy()
		import Main
		Main.F5ICTSBAApp(self.master)

if __name__ == "__main__":
	root = tk.Tk()
	ReportGenerator(root)
	root.mainloop()
	