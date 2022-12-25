import tkinter as tk
import calendar

class Calendar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.calendar = calendar.Calendar()
        self.year = 2021
        self.month = 1
        self.widgets()

    def widgets(self):
        self.header = tk.Label(self, text=calendar.month_name[self.month] + " " + str(self.year), font=("Helvetica", 16))
        self.header.pack(side="top", fill="x", pady=10)

        self.calendar_frame = tk.Frame(self)
        self.calendar_frame.pack(side="top", fill="both", expand=True)

        self.days = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
        for day in self.days:
            label = tk.Label(self.calendar_frame, text=day, font=("Helvetica", 14), width=2)
            label.grid(row=0, column=self.days.index(day))

        self.display_calendar()

    def display_calendar(self):
        for week in self.calendar.monthdatescalendar(self.year, self.month):
            for day in week:
                if day.month == self.month:
                    tk.Label(self.calendar_frame, text=day.day, font=("Helvetica", 14), width=2).grid(row=week.index(day)+1, column=self.days.index(day.strftime("%a")))

root = tk.Tk()
Calendar(root).pack(side="top", fill="both", expand=True)
root.mainloop()
