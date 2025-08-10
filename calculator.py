import tkinter as tk

def click(event):
    btn_text = event.widget.cget("text")
    global expression
    if btn_text == "C":
        expression = ""
        entry_var.set(expression)
    elif btn_text == "=":
        try:
            result = str(eval(expression))
            entry_var.set(result)
            add_history(expression, result)
            expression = result
        except:
            entry_var.set("Error")
            add_history(expression, "Error")
            expression = ""
    else:
        expression += btn_text
        entry_var.set(expression)

def add_history(expr, res):
    history_list.append(f"{expr} = {res}")

def show_history():
    hist_win = tk.Toplevel(root)
    hist_win.title("Calculation History")
    hist_win.geometry("300x400")
    hist_win.resizable(False, False)
    hist_win.config(bg="#f4f4f4")
    
    hist_label = tk.Label(hist_win, text="History", font=("Arial", 14), bg="#f4f4f4")
    hist_label.pack(pady=10)
    
    hist_text = tk.Text(hist_win, font=("Arial", 12), bg="#fafafa", fg="#444", state="normal", wrap="word")
    hist_text.pack(expand=True, fill="both", padx=10, pady=5)
    
    hist_text.delete(1.0, tk.END)
    for item in history_list:
        hist_text.insert(tk.END, item + "\n")
    hist_text.configure(state="disabled")
    
    clear_btn = tk.Button(hist_win, text="Clear History", font=("Arial", 12), bg="#ffdad6", fg="#a33",
                          command=lambda: clear_history(hist_text))
    clear_btn.pack(pady=5)

def clear_history(hist_text_widget=None):
    history_list.clear()
    if hist_text_widget:
        hist_text_widget.configure(state="normal")
        hist_text_widget.delete(1.0, tk.END)
        hist_text_widget.configure(state="disabled")

expression = ""
history_list = []

root = tk.Tk()
root.title("Simple Calculator")
root.geometry("320x450")
root.resizable(False, False)
root.config(bg="#f4f4f4")

entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 22), bd=0, relief="ridge",
                 bg="#fafafa", fg="#333", justify="right")
entry.place(x=15, y=20, width=290, height=50)

btn_cfg = {
    "font": ("Arial", 16),
    "bd":0,
    "bg":"#e0e0e0",
    "fg":"#333",
    "activebackground":"#d1d1d1",
    "activeforeground":"#111",
    "width":5,
    "height":2
}

buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', 'C', '+'],
    ['=']
]

y = 85
for row in buttons:
    x = 15
    for btn_text in row:
        btn = tk.Button(root, text=btn_text, **btn_cfg)
        btn.place(x=x, y=y)
        btn.bind("<Button-1>", click)
        x += 70
    y += 60

show_hist_btn = tk.Button(root, text="Show History", font=("Arial", 12), bg="#cce5ff", fg="#004085",
                          command=show_history)
show_hist_btn.place(x=15, y=400, width=290, height=40)

root.mainloop()
