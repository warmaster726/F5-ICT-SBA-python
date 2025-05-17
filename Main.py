import DBS
import tkinter as tk
from tkinter import messagebox

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

if __name__ == "__main__":
    root = tk.Tk()
    app = F5ICTSBAApp(root)
    if DBS.checking() == True:
        messagebox.showwarning("Warning", "Database needs to be updated")
    root.mainloop()
