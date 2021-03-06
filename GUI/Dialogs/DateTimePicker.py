from calendar import Calendar
from tkinter import *
from tkcalendar import *
import tkinter as tk
from datetime import datetime
from tkinter import messagebox


class DateTimePicker:
    timestamp = " "

    def __init__(self):
        yy, mm, dd, hh, min, sec = self.get_current_timestamp()
        self.root = Tk()
        self.cal = Calendar(self.root, selectmode="day", font="Arial 10", cursor="hand1", year=int(yy), month=int(mm), day=int(dd))
        self.lbl = Label(self.root, text="Select time [HH:MM:SS]")
        self.select_btn = Button(self.root, text="Select Timestamp", command=self.grab_date)
        self.hourstr = tk.StringVar(self.root, hh)
        self.hour = tk.Spinbox(self.root, from_=0, to=23, wrap=True, textvariable=self.hourstr, width=5)
        self.minstr = tk.StringVar(self.root, min)
        self.min = tk.Spinbox(self.root, from_=0, to=59, wrap=True, textvariable=self.minstr, width=5)
        self.secstr = tk.StringVar(self.root, sec)
        self.sec = tk.Spinbox(self.root, from_=0, to=59, wrap=True, textvariable=self.secstr, width=5)
        self.create_widget()

    def create_widget(self):
        self.root.title('Select Timestamp')
        self.root.geometry("400x400")
        self.select_btn.pack(pady=20, side=BOTTOM)
        self.cal.pack(pady=20, fill="both", expand=True)
        self.lbl.pack(pady=20, side=LEFT)
        self.sec.pack(pady=20, side=RIGHT)
        self.min.pack(pady=20, side=RIGHT)
        self.hour.pack(pady=20, side=RIGHT)
        self.root.mainloop()

    def grab_date(self):
        date = self.cal.get_date()
        date = datetime.strptime(date, '%m/%d/%y')
        date = str(date).split(" ")[0]
        hh = self.hour.get()
        mm = self.min.get()
        ss = self.sec.get()
        t = "{} {}:{}:{}".format(date, hh, mm, ss)
        try:
            t = str(datetime.strptime(t, "%Y-%m-%d %H:%M:%S")).replace(" ", "T")
            self.__set_timestamp(t)
            self.root.destroy()
            return self.timestamp
        except:
            self.alert_user()

    def alert_user(self):
        messagebox.showerror("Error", "Invalid time")

    def __set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_timestamp(self):
        return self.timestamp

    def get_current_timestamp(self):
        dateTimeObj = datetime.now()
        date, time = str(dateTimeObj).split(" ")
        yy, mm, dd = str(date).split("-")
        hh, min, sec = str(time).split(".")[0].split(":")
        return yy, mm, dd, hh, min, sec

if __name__ == '__main__':
    widget = DateTimePicker()
    timestamp = widget.get_timestamp()
    widget.get_current_timestamp()
    print("FORMATTED TIMESTAMP")
    print(timestamp)