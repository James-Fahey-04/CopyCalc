import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import pyperclip
import threading
import time

class CopyCalc:
    def __init__(self):
        self.total = 0.0
        self.history = []
        self.active_operator = '+'
        self.last_clipboard = ""

        self.app = tb.Window(themename="flatly")
        self.app.title("CopyCalc")
        self.app.geometry("400x500")
        self.app.resizable(False, False)

        self.total_var = tk.StringVar(value=f"{self.total:.2f}")
        tb.Label(self.app, text="CopyCalc", font=("Segoe UI", 18, "bold"), bootstyle="dark").pack(pady=(15, 5))
        tb.Label(self.app, textvariable=self.total_var, font=("Segoe UI", 28, "bold"), bootstyle="light").pack(pady=(0, 5))

        self.status_var = tk.StringVar(value="Current operator: +")
        tb.Label(self.app, textvariable=self.status_var, font=("Segoe UI", 12), bootstyle="secondary").pack()

        op_frame = tb.Frame(self.app)
        op_frame.pack(pady=10)
        self.make_op_button(op_frame, "+", 0)
        self.make_op_button(op_frame, "-", 1)
        self.make_op_button(op_frame, "*", 2)
        self.make_op_button(op_frame, "/", 3)

        tb.Button(self.app, text="Reset", command=self.reset_total, bootstyle="danger-outline").pack(pady=(0, 10))

        tb.Label(self.app, text="History", font=("Segoe UI", 11, "bold"), bootstyle="dark").pack()
        self.history_box = tk.Listbox(self.app, height=10, font=("Courier New", 10), bg="#f8f9fa", fg="#000000", relief="flat")
        self.history_box.pack(padx=20, pady=(0, 10), fill="both", expand=True)

        threading.Thread(target=self.watch_clipboard, daemon=True).start()
        self.app.mainloop()

    def make_op_button(self, frame, symbol, col):
        tb.Button(
            frame, text=symbol, width=6,
            command=lambda s=symbol: self.set_operator(s),
            bootstyle="primary"
        ).grid(row=0, column=col, padx=5)

    def set_operator(self, op):
        self.active_operator = op
        self.status_var.set(f"Current operator: {op}")

    def watch_clipboard(self):
        while True:
            try:
                current = pyperclip.paste()
                if current != self.last_clipboard:
                    self.last_clipboard = current
                    try:
                        value = float(current)
                        self.apply_operation(value)
                    except ValueError:
                        pass  # Ignore non-numeric
            except Exception as e:
                print("Clipboard error:", e)
            time.sleep(0.4)

    def apply_operation(self, value):
        try:
            if self.active_operator == '+':
                self.total += value
            elif self.active_operator == '-':
                self.total -= value
            elif self.active_operator == '*':
                self.total *= value
            elif self.active_operator == '/':
                if value == 0:
                    messagebox.showerror("Error", "Cannot divide by zero.")
                    return
                self.total /= value

            self.total_var.set(f"{self.total:.2f}")
            self.history.append(f"{self.active_operator} {value}")
            self.update_history()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_history(self):
        self.history_box.delete(0, tk.END)
        for item in self.history:
            self.history_box.insert(tk.END, item)
        self.history_box.yview_moveto(1)

    def reset_total(self):
        self.total = 0.0
        self.history.clear()
        self.total_var.set(f"{self.total:.2f}")
        self.history_box.delete(0, tk.END)

if __name__ == "__main__":
    CopyCalc()



