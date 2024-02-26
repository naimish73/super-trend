from tkinter import Tk, Label, Frame, StringVar
from functions import *

status_label = ""
symbol_list = {
    "Tata Consutancy Services": "TCS.NS",
}
prize_range_touch = []

def onCountdownFunctionCall():
    global status_label, prize_range_touch, symbol_list

    for name, sbl in symbol_list.items():
        data = fetch_realtime_data(sbl)
        super_trend = calculate_supertrend(data)
        check_range = check_supertrend_range(data, super_trend)

        if check_range:
            prize_range_touch.append(name)

    for widget in stock_frame.winfo_children():
        widget.destroy()

    for name in prize_range_touch:
        label = Label(stock_frame, text=name, font=("Helvetica", 16), fg="black", bg="#bfbfbf")
        label.pack(pady=5)

def countdown():
    global timer, status_label
    if timer > 0:
        mins, secs = divmod(timer, 60)
        time_str.set(f"{mins:02d}:{secs:02d}")
        timer -= 1
        root.after(1000, countdown)
    else:
        status_label.config(text="Listing the stocks which touch the 1% range of supertrend...")
        print("Countdown finished, calling function.")
        timer = 60
        countdown()

def start_countdown():
    global timer, status_label
    status_label.config(text="Countdown started...")
    timer = 60
    onCountdownFunctionCall()
    countdown()

root = Tk()
root.title("Super-trend calculator for stocks")

width = int(root.winfo_screenwidth() * 0.75)
height = int(root.winfo_screenheight() * 0.7)
root.geometry(f"{width}x{height}")

time_str = StringVar()
frame = Frame(root, bg="#333333")
frame.pack(fill="both", expand=True)

countdown_label = Label(frame, textvariable=time_str, font=("Helvetica", 48), fg="white", bg="#333333")
countdown_label.pack(pady=50)

status_label = 'fetching data...'
status_label = Label(frame, text=f"status: {status_label}", font=("Helvetica", 16), fg="white", bg="#333333")
status_label.pack(pady=0)


stock_frame = Frame(root, bg="#bfbfbf", width=900, height=400)
stock_frame.place(relx=0.5, rely=0.6, anchor="center")

root.after(100, start_countdown)
root.mainloop()
