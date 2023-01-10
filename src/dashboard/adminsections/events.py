# "IT JUST WORKS, DON'T ASK WHY I DID THAT"

import customtkinter
import csv
import mysql.connector
import openpyxl
import time
import uuid

from tkinter import ttk, messagebox, filedialog
from tkcalendar import Calendar
from datetime import datetime, timedelta
from ...database.db_connect import cursor, cnx

customtkinter.set_appearance_mode("light") 
customtkinter.set_default_color_theme("dark-blue")

class EventSection:
    def __init__(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
   
        new_event_button = customtkinter.CTkButton(
                        frame,
                        text='New Event',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        width=180, 
                        height=65, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command= lambda: NewEvent(frame)
                        )
        new_event_button.grid(row=1, column=1, sticky="n", padx=35, pady=5)
        
        mark_completed_button = customtkinter.CTkButton(
                        frame,
                        text='Mark Completed',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        width=180, 
                        height=65, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command= lambda: MarkCompleted(frame, treeview)
                        )
        mark_completed_button.grid(row=2, column=1, sticky="n", padx=35, pady=5)
        
        update_event_button = customtkinter.CTkButton(
                        frame,
                        text='Update Event',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        width=180, 
                        height=65, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command= lambda: UpdateEvent(frame, treeview)
                        )
        update_event_button.grid(row=3, column=1, sticky="n", padx=35, pady=5)
        
        cancel_event_button = customtkinter.CTkButton(
                        frame,
                        text='Cancel Event',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#FF0000",  
                        width=180, 
                        height=65, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command= lambda: CancelEvent(frame, treeview)
                        )
        cancel_event_button.grid(row=4, column=1, sticky="s", padx=35, pady=5)
        
        event_history_button = customtkinter.CTkButton(
                        frame,
                        text='Event History',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        width=180, 
                        height=65, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command= lambda: EventHistory(frame)
                        )
        event_history_button.grid(row=5, column=1, sticky="s", padx=35, pady=5)
        
        export_data_button = customtkinter.CTkButton(
                        frame,
                        text='Export Data',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        width=180, 
                        height=65, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command= lambda: ExportData(frame)
                        )
        export_data_button.grid(row=6, column=1, sticky="s", padx=35, pady=5)
        
        ##################################### Treeview #####################################
        
        style = ttk.Style()    
        style.theme_use("default")  
        style.configure("Treeview",
                        font=customtkinter.CTkFont(size=15),
                        background="#2A2D2E",
                        foreground="#EDF6FA",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=1)
        style.map('Treeview', background=[('selected', '#22559b')])
    
        style.configure("Treeview.Heading",
                        font=customtkinter.CTkFont(size=18, weight="bold"),
                        background="#3D3D3D",
                        foreground="#EDF6FA",
                        relief="flat")
        style.map("Treeview.Heading", background=[('active', '#0065D9')])
        
        treeview = ttk.Treeview(frame)
        treeview["columns"] = ("sr", "event_name", "event_description", "event_date", "event_time", "event_venue", "event_id",)
        treeview["show"] = "headings"
        
        treeview.column("sr", width=50, anchor="center")
        treeview.column("event_name", width=200, anchor="center")
        treeview.column("event_description", width=300, anchor="center")
        treeview.column("event_date", width=80, anchor="center")
        treeview.column("event_time", width=80, anchor="center")
        treeview.column("event_venue", width=150, anchor="center")
        treeview.column("event_id", width=200, anchor="center")
        
        treeview.heading("sr", text="Sr. No")
        treeview.heading("event_name", text="Title")
        treeview.heading("event_description", text="Description")
        treeview.heading("event_date", text="Date")
        treeview.heading("event_time", text="Time")
        treeview.heading("event_venue", text="Location")
        treeview.heading("event_id", text="Event ID")

        treeview.grid(row=1, column=2, rowspan=6, sticky="nsew", padx=10, pady=10)
        
        query = "SELECT event_name, event_description, event_date, event_time, event_venue, event_id FROM events"
        while True:
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                break
            except mysql.connector.Error as err:
                print(f"[x] Error occured while executing query: {query}\n{err}")
                print("[*] Trying to load the treeview again...\n")
                print("--- While we are at it, check your database connection...\n")
                time.sleep(5)
                continue
            finally:
                for row in treeview.get_children():
                    treeview.delete(row)
                i=0
                for row in results:
                    i=i+1
                    treeview.insert("", "end", text="", values=(i, row[0], row[1], row[2], row[3], row[4], row[5]))

class NewEvent:
    def __init__(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        self.the_frame = frame
        self.new_event(frame)
    
    def new_event(self, frame):
        
        go_back_button = customtkinter.CTkButton(
                        frame,
                        text="Go Back",
                        font=customtkinter.CTkFont(size=16),
                        fg_color="Green",
                        hover_color="#2AAAFA",
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command=lambda: EventSection(frame)
                        )
        go_back_button.place(relx=0.1, rely=0.02, anchor="n")    
        
        new_event_label = customtkinter.CTkLabel(
                        frame,
                        text='Add New Event',
                        font=customtkinter.CTkFont(size=24, weight="bold"),
                        )
        new_event_label.place(relx=0.5, rely=0.02, anchor="n")
        
        event_name_label = customtkinter.CTkLabel(
                        frame,
                        text='Event Name:',
                        font=customtkinter.CTkFont(size=18), 
                        )
        event_name_label.place(x=120, y=80, anchor="center")
        
        self.event_name_entry = customtkinter.CTkEntry(
                        frame,
                        width=400,
                        height=25,
                        font=customtkinter.CTkFont(size=18),
                        border_width=3,
                        border_color=("#1B1B24", "#EDF6FA"),
                        corner_radius=10,
                        )
        self.event_name_entry.place(x=400, y=80, anchor="center")
        
        event_description_label = customtkinter.CTkLabel(
                        frame,
                        text='Description:',
                        font=customtkinter.CTkFont(size=18), 
                        )
        event_description_label.place(x=120, y=120, anchor="center")
            
        self.event_description_entry = customtkinter.CTkTextbox(
                        frame,
                        text_color = ("#1B1B24", "#EDF6FA"),
                        width=400,
                        height=320,
                        font=customtkinter.CTkFont(size=18),
                        border_width=3,
                        border_color=("#1B1B24", "#EDF6FA"),
                        corner_radius=10,
                        )
        self.event_description_entry.place(x=400, y=270, anchor="center")
        
        event_date_label = customtkinter.CTkLabel(
                        frame,
                        text='Event Date:',
                        font=customtkinter.CTkFont(size=18), 
                        )
        event_date_label.place(x=675, y=80, anchor="center")
        
        today = datetime.now() 
        
        self.event_date_calendar = Calendar(
                            frame, 
                            year=today.year, 
                            month=today.month, 
                            day=today.day,
                            date_pattern='dd/mm/yy'
                            )
        self.event_date_calendar.place(x=740, y=190, anchor="center")
        
        # Can only specify the date between today and 30 days from now
        self.event_date_calendar.datemin = datetime.now().date()
        self.event_date_calendar.datemax = datetime.now().date() + timedelta(days=30)
        
        self.selected_date_label = customtkinter.CTkLabel(
                        frame,
                        text="",
                        font=customtkinter.CTkFont(size=18), 
                        )
        self.selected_date_label.place(x=740, y=300, anchor="center")
        
        get_date_button = customtkinter.CTkButton(
                            frame,
                            text="Select Date",
                            font=customtkinter.CTkFont(size=16),
                            fg_color="#0065D9",
                            border_width=2,
                            border_color=("#1B1B24","#EDF6FA"),
                            corner_radius=15,
                            command=self.select_date 
                            )
        get_date_button.place(x=740, y=340, anchor="center")
        
        event_time_label = customtkinter.CTkLabel(
                        frame,
                        text="Event Time:",
                        font=customtkinter.CTkFont(size=18), 
                        )
        event_time_label.place(x=940, y=80, anchor="center")

        self.hour_menu = customtkinter.CTkOptionMenu(
                        frame, 
                        values=['12', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11'],
                        corner_radius=10,
                        width=60
                        )
        self.hour_menu.place(x=1040, y=80, anchor="center")
        
        self.minute_menu = customtkinter.CTkOptionMenu(
                            frame, 
                            values=['00', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55'],
                            corner_radius=10,
                            width=60
                            )
        self.minute_menu.place(x=1110, y=80, anchor="center")
        
        self.ampm_menu = customtkinter.CTkOptionMenu(
                        frame, 
                        values=['AM', 'PM'],
                        corner_radius=10,
                        width=60
                        )
        self.ampm_menu.place(x=1180, y=80, anchor="center")
        
        self.selected_time_label = customtkinter.CTkLabel(
                        frame,
                        text="",
                        font=customtkinter.CTkFont(size=18), 
                        )
        self.selected_time_label.place(x=1110, y=120, anchor="center")
        
        get_time_button = customtkinter.CTkButton(
                            frame,
                            text="Select Time",
                            font=customtkinter.CTkFont(size=16),
                            fg_color="#0065D9",
                            border_width=2,
                            border_color=("#1B1B24","#EDF6FA"),
                            corner_radius=15,
                            command=self.select_time 
                            )
        get_time_button.place(x=1110, y=160, anchor="center")
        
        event_venue_label = customtkinter.CTkLabel(
                        frame,
                        text='Event Venue:',
                        font=customtkinter.CTkFont(size=18), 
                        )
        event_venue_label.place(x=940, y=220, anchor="center")
        
        self.event_venue_entry = customtkinter.CTkTextbox(
                        frame,
                        width=330,
                        height=100,
                        font=customtkinter.CTkFont(size=18),
                        border_width=3,
                        border_color=("#1B1B24", "#EDF6FA"),
                        corner_radius=10,
                        )
        self.event_venue_entry.place(x=1050, y=300, anchor="center")
        
        submit_event_button = customtkinter.CTkButton(
                        frame,
                        text="Submit",
                        font=customtkinter.CTkFont(size=20, weight="bold"),
                        width=140,
                        height=60,
                        fg_color="#0065D9",
                        hover_color="#2AAAFA",
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command=self.check_event_details
                        )
        submit_event_button.place(x=1040, y=400, anchor="center")    
    
    def select_date(self):
        self.selected_date = self.event_date_calendar.get_date()
        self.selected_date_label.configure(text = "Selected Date: " + self.selected_date)
        return self.selected_date
        
    def select_time(self):
        self.selected_time = f"{self.hour_menu.get()}:{self.minute_menu.get()} {self.ampm_menu.get()}" 
        self.selected_time_label.configure(text = "Selected Time: " + self.selected_time)
        return self.selected_time
    
    def check_event_details(self):
        self.event_name = self.event_name_entry.get()
        
        event_description = self.event_description_entry.get("0.0", "end")
        escaped_event_description = mysql.connector.conversion.MySQLConverter().escape(event_description) 
        self.event_description = escaped_event_description
        
        self.event_date = self.select_date()
        self.event_time = self.select_time()
        self.event_venue = self.event_venue_entry.get("0.0", "end")
        
        # This generates unique ID for event 
        self.event_id = uuid.uuid5(uuid.NAMESPACE_OID, f"{self.event_name}{self.event_date}{self.event_time}{self.event_venue}")
        
        error_message = ""
        if not self.event_name:
            error_message += "Please provide event name.\n"
        if len(self.event_description) == 2:
            error_message += "Please provide event description.\n"
        if len(self.event_venue) == 1:
            error_message += "Please provide event venue.\n"
        
        # Check if event date is in the future or today   
        current_date = datetime.now().date()
        day, month, year = self.event_date.split("/")
        event_date = datetime((2000 + int(year)), int(month), int(day)).date()
        if event_date < current_date:
            error_message += "Event date must be in the future.\n"
              
        if error_message:
            messagebox.showerror("Error", error_message)
        else:
            self.dialogue_window = customtkinter.CTkToplevel(fg_color=("#EDF6FA", "#1B1B24"))
            self.dialogue_window.geometry("500x400")
            self.dialogue_window.title("Proceed to add event?")
            self.dialogue_window.resizable(False, False)
            
            question_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Are you sure this information is correct?",
                            font=customtkinter.CTkFont(size=16),
                            )
            question_label.place(x=250, y=20, anchor="center")
            
            event_name_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Name: " + self.event_name,
                            font=customtkinter.CTkFont(size=16),
                            )
            event_name_label.place(x=150, y=60, anchor="nw")
            
            event_description_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Description: " + f"{self.event_description[:15]}...",
                            font=customtkinter.CTkFont(size=16),
                            )
            event_description_label.place(x=150, y=100, anchor="nw")
            
            event_date_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Date: " + self.event_date,
                            font=customtkinter.CTkFont(size=16),
                            )
            event_date_label.place(x=150, y=140, anchor="nw")
            
            event_time_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Time: " + self.event_time,
                            font=customtkinter.CTkFont(size=16),
                            )
            event_time_label.place(x=150, y=180, anchor="nw")
            
            event_venue_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Venue: " + self.event_venue,
                            font=customtkinter.CTkFont(size=16),
                            )
            event_venue_label.place(x=150, y=220, anchor="nw")
            
            yes_button = customtkinter.CTkButton(
                            self.dialogue_window,
                            text="Yes (Add Event)",
                            width=140,
                            height=60,
                            font=customtkinter.CTkFont(size=16),
                            fg_color="#0065D9",
                            border_width=2,
                            border_color=("#1B1B24","#EDF6FA"),
                            corner_radius=15,
                            command=self.add_event_to_database
                            )
            yes_button.place(x=145, y=330, anchor="center")
            
            no_button = customtkinter.CTkButton(
                            self.dialogue_window,
                            text="No (Edit Again)",
                            width=140,
                            height=60,
                            font=customtkinter.CTkFont(size=16),
                            fg_color="#0065D9",
                            border_width=2,
                            border_color=("#1B1B24","#EDF6FA"),
                            corner_radius=15,
                            command=self.dialogue_window.destroy
                            )
            no_button.place(x=370, y=330, anchor="center")
            
    def add_event_to_database(self):
              
        # For future purposes (date and time is being stored as string as of now)
        # # This converts the date from string to datetime object 
        #date_format = "%d/%m/%y"  
        #date = datetime.strptime(self.event_date, date_format)
        
        # # This converts the time from string to datetime object     
        # time_format = "%I:%M %p"
        # time = datetime.strptime(self.event_time, time_format)
        
        try:
            cursor.execute("""INSERT INTO events(event_name, event_description, event_date, event_time, event_venue, event_id) VALUES ("{}", "{}", "{}", "{}", "{}", "{}");""".format(
                            self.event_name, self.event_description, self.event_date, self.event_time,  self.event_venue, self.event_id)
                        )
            cnx.commit()                         
        except Exception as error:
            raise Exception("Error", str(error))  
        else:
            self.dialogue_window.destroy()
            EventSection(self.the_frame)

class MarkCompleted:
    def __init__(self, frame, treeview):
        self.the_frame = frame
        try:
            selected_item = treeview.selection()[0]
            self.event_id = treeview.item(selected_item)['values'][6]
        except IndexError:
            messagebox.showerror("Error", "Please select an event to mark it as completed!")
        else:
            self.mark_completed(frame)
    
    def mark_completed(self, frame):
        try:
            # This inserts the selected event into completed_event tables and deletes it from the events table  
            cursor.execute("""INSERT INTO completed_events (event_name, event_description, event_date, event_time, event_venue, event_id) SELECT event_name, event_description, event_date, event_time, event_venue, event_id FROM events WHERE event_id = "{}";""".format(self.event_id))
            cursor.execute("""DELETE FROM events WHERE event_id = "{}";""".format(self.event_id))
            cnx.commit()
        except Exception as error:
            raise Exception("Error", str(error))
        else:
            messagebox.showinfo("Success", "Event marked as completed!\n\nCheck Event Histroy to list all the completed events!")
            EventSection(self.the_frame)
            
class UpdateEvent:
    def __init__(self, frame, treeview):
        self.the_frame = frame
        try:
            selected_item = treeview.selection()[0]
            self.event_name = treeview.item(selected_item)['values'][1]
            self.event_description = treeview.item(selected_item)['values'][2]
            self.event_date = treeview.item(selected_item)['values'][3]
            self.event_time = treeview.item(selected_item)['values'][4]
            self.event_venue = treeview.item(selected_item)['values'][5]
            self.event_id = treeview.item(selected_item)['values'][6]
        
        except IndexError:
            messagebox.showerror("Error", "Please select an event to update")
        else:
            for widget in frame.winfo_children():
                widget.destroy()
            self.update_event(frame)              
    
    def update_event(self, frame):
        go_back_button = customtkinter.CTkButton(
                        frame,
                        text="Go Back",
                        font=customtkinter.CTkFont(size=16),
                        fg_color="Green",
                        hover_color="#2AAAFA",
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command=lambda: EventSection(frame)
                        )
        go_back_button.place(relx=0.1, rely=0.02, anchor="n")    
        
        new_event_label = customtkinter.CTkLabel(
                        frame,
                        text='Edit Event Details',
                        font=customtkinter.CTkFont(size=26, weight="bold"),
                        )
        new_event_label.place(relx=0.5, rely=0.02, anchor="n")
        
        event_name_label = customtkinter.CTkLabel(
                        frame,
                        text='Event Name:',
                        font=customtkinter.CTkFont(size=18), 
                        )
        event_name_label.place(x=120, y=80, anchor="center")
        
        self.event_name_entry = customtkinter.CTkEntry(
                        frame,
                        width=400,
                        height=25,
                        font=customtkinter.CTkFont(size=18),
                        border_width=3,
                        border_color=("#1B1B24", "#EDF6FA"),
                        corner_radius=10,
                        )
        self.event_name_entry.place(x=400, y=80, anchor="center")
        
        event_description_label = customtkinter.CTkLabel(
                        frame,
                        text='Description:',
                        font=customtkinter.CTkFont(size=18), 
                        )
        event_description_label.place(x=120, y=120, anchor="center")
            
        self.event_description_entry = customtkinter.CTkTextbox(
                        frame,
                        text_color = ("#1B1B24", "#EDF6FA"),
                        width=400,
                        height=320,
                        font=customtkinter.CTkFont(size=18),
                        border_width=3,
                        border_color=("#1B1B24", "#EDF6FA"),
                        corner_radius=10,
                        )
        self.event_description_entry.place(x=400, y=270, anchor="center")
        
        event_date_label = customtkinter.CTkLabel(
                        frame,
                        text='Event Date:',
                        font=customtkinter.CTkFont(size=18), 
                        )
        event_date_label.place(x=675, y=80, anchor="center")
        
        # Add existing date values in calendar
        self.event_date_calendar = Calendar(
                            frame, 
                            year=int(self.event_date[6:]),
                            month=int(self.event_date[3:5]), 
                            day=int(self.event_date[:2]),
                            date_pattern='dd/mm/yy'
                            )
        self.event_date_calendar.place(x=740, y=190, anchor="center")
        
        # Can only specify the date between today and 30 days from now
        self.event_date_calendar.datemin = datetime.now().date()
        self.event_date_calendar.datemax = datetime.now().date() + timedelta(days=30)
        
        self.selected_date_label = customtkinter.CTkLabel(
                        frame,
                        text="",
                        font=customtkinter.CTkFont(size=18), 
                        )
        self.selected_date_label.place(x=740, y=300, anchor="center")
        
        
        get_date_button = customtkinter.CTkButton(
                            frame,
                            text="Select Date",
                            font=customtkinter.CTkFont(size=16),
                            fg_color="#0065D9",
                            border_width=2,
                            border_color=("#1B1B24","#EDF6FA"),
                            corner_radius=15,
                            command=self.select_date
                            )
        get_date_button.place(x=740, y=340, anchor="center")
        
        
        event_time_label = customtkinter.CTkLabel(
                        frame,
                        text="Event Time:",
                        font=customtkinter.CTkFont(size=18), 
                        )
        event_time_label.place(x=940, y=80, anchor="center")

        self.hour_menu = customtkinter.CTkOptionMenu(
                        frame, 
                        values=['12', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11'],
                        corner_radius=10,
                        width=60
                        )
        self.hour_menu.place(x=1040, y=80, anchor="center")
        
        # Add existing time values in hour dropdown menu
        self.hour_menu.set(self.event_time[:2])
        
        self.minute_menu = customtkinter.CTkOptionMenu(
                            frame, 
                            values=['00', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55'],
                            corner_radius=10,
                            width=60
                            )
        self.minute_menu.place(x=1110, y=80, anchor="center")
        
        # Add existing time values in minute dropdown menu
        self.minute_menu.set(self.event_time[3:5])
        
        self.ampm_menu = customtkinter.CTkOptionMenu(
                        frame, 
                        values=['AM', 'PM'],
                        corner_radius=10,
                        width=60
                        )
        self.ampm_menu.place(x=1180, y=80, anchor="center")
        
        # Add existing time values in ampm dropdown menu
        self.ampm_menu.set(self.event_time[6:])
        
        self.selected_time_label = customtkinter.CTkLabel(
                        frame,
                        text="",
                        font=customtkinter.CTkFont(size=18), 
                        )
        self.selected_time_label.place(x=1110, y=120, anchor="center")
        
        get_time_button = customtkinter.CTkButton(
                            frame,
                            text="Select Time",
                            font=customtkinter.CTkFont(size=16),
                            fg_color="#0065D9",
                            border_width=2,
                            border_color=("#1B1B24","#EDF6FA"),
                            corner_radius=15,
                            command=self.select_time 
                            )
        get_time_button.place(x=1110, y=160, anchor="center")
        
        event_venue_label = customtkinter.CTkLabel(
                        frame,
                        text='Event Venue:',
                        font=customtkinter.CTkFont(size=18), 
                        )
        event_venue_label.place(x=940, y=220, anchor="center")
        
        self.event_venue_entry = customtkinter.CTkTextbox(
                        frame,
                        width=330,
                        height=100,
                        font=customtkinter.CTkFont(size=18),
                        border_width=3,
                        border_color=("#1B1B24", "#EDF6FA"),
                        corner_radius=10,
                        )
        self.event_venue_entry.place(x=1050, y=300, anchor="center")
        
        update_event_button = customtkinter.CTkButton(
                        frame,
                        text="Update",
                        font=customtkinter.CTkFont(size=20, weight="bold"),
                        width=140,
                        height=60,
                        fg_color="#0065D9",
                        hover_color="#2AAAFA",
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command=self.check_event_details
                        )
        update_event_button.place(x=1040, y=400, anchor="center")
        
        ############################### Add existing event values to the form ###############################
        
        self.event_name_entry.insert(0, self.event_name)
        self.event_description_entry.insert("0.0", self.event_description)
        self.event_venue_entry.insert("0.0", self.event_venue)
        self.selected_date_label.configure(text=self.event_date)
        self.selected_time_label.configure(text=self.event_time)
        
    def check_event_details(self):
        self.event_name = self.event_name_entry.get()

        event_description = self.event_description_entry.get("0.0", "end")
        escaped_event_description = mysql.connector.conversion.MySQLConverter().escape(event_description) 
        self.event_description = escaped_event_description
        
        self.event_date = self.select_date()
        self.event_time = self.select_time()
        self.event_venue = self.event_venue_entry.get("0.0", "end")
        
        error_message = ""
        if not self.event_name:
            error_message += "Please provide event name.\n"
        if len(self.event_description) == 2:
            error_message += "Please provide event description.\n"
        if len(self.event_venue) == 1:
            error_message += "Please provide event venue.\n"
            
        # Check if event date is in the future or today   
        current_date = datetime.now().date()
        day, month, year = self.event_date.split("/")
        event_date = datetime((2000 + int(year)), int(month), int(day)).date()
        if event_date < current_date:
            error_message += "Event date must be in the future.\n"
              
        if error_message:
            messagebox.showerror("Error", error_message)
        else:
            self.dialogue_window = customtkinter.CTkToplevel(fg_color=("#EDF6FA", "#1B1B24"))
            self.dialogue_window.geometry("500x400")
            self.dialogue_window.title("Proceed to update event?")
            self.dialogue_window.resizable(False, False)
            
            question_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Are you sure this information is correct?",
                            font=customtkinter.CTkFont(size=16),
                            )
            question_label.place(x=250, y=20, anchor="center")
            
            event_name_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Name: " + self.event_name,
                            font=customtkinter.CTkFont(size=16),
                            )
            event_name_label.place(x=150, y=60, anchor="nw")
            
            event_description_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Description: " + f"{self.event_description[:15]}...",
                            font=customtkinter.CTkFont(size=16),
                            )
            event_description_label.place(x=150, y=100, anchor="nw")
            
            event_date_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Date: " + self.event_date,
                            font=customtkinter.CTkFont(size=16),
                            )
            event_date_label.place(x=150, y=140, anchor="nw")
            
            event_time_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Time: " + self.event_time,
                            font=customtkinter.CTkFont(size=16),
                            )
            event_time_label.place(x=150, y=180, anchor="nw")
            
            event_venue_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Venue: " + self.event_venue,
                            font=customtkinter.CTkFont(size=16),
                            )
            event_venue_label.place(x=150, y=220, anchor="nw")
            
            yes_button = customtkinter.CTkButton(
                            self.dialogue_window,
                            text="Yes (Update Event)",
                            width=140,
                            height=60,
                            font=customtkinter.CTkFont(size=16),
                            fg_color="#0065D9",
                            border_width=2,
                            border_color=("#1B1B24","#EDF6FA"),
                            corner_radius=15,
                            command=self.update_event_in_database
                            )
            yes_button.place(x=145, y=330, anchor="center")
            
            no_button = customtkinter.CTkButton(
                            self.dialogue_window,
                            text="No (Edit Again)",
                            width=140,
                            height=60,
                            font=customtkinter.CTkFont(size=16),
                            fg_color="#0065D9",
                            border_width=2,
                            border_color=("#1B1B24","#EDF6FA"),
                            corner_radius=15,
                            command=self.dialogue_window.destroy
                            )
            no_button.place(x=370, y=330, anchor="center") 
         
    def select_date(self):
        self.selected_date = self.event_date_calendar.get_date()
        self.selected_date_label.configure(text = "Selected Date: " + self.selected_date)
        return self.selected_date
        
    def select_time(self):
        self.selected_time = f"{self.hour_menu.get()}:{self.minute_menu.get()} {self.ampm_menu.get()}" 
        self.selected_time_label.configure(text = "Selected Time: " + self.selected_time)
        return self.selected_time
            
    def update_event_in_database(self):     
        try:
            cursor.execute("""UPDATE events SET event_name = "{}", event_description = "{}", event_date = "{}", event_time = "{}", event_venue = "{}" WHERE event_id = "{}";""".format(
                            self.event_name, 
                            self.event_description, 
                            self.event_date, 
                            self.event_time,  
                            self.event_venue, 
                            self.event_id)
                        )
            cnx.commit()                         
        except Exception as error:
            raise Exception("Error", str(error))  
        else:
            self.dialogue_window.destroy()
            EventSection(self.the_frame)

class CancelEvent:
    def __init__(self, frame, treeview):
        self.the_frame = frame
        try:
            selected_item = treeview.selection()[0]
            self.event_name = treeview.item(selected_item)['values'][1]
            self.event_description = treeview.item(selected_item)['values'][2]
            self.event_date = treeview.item(selected_item)['values'][3]
            self.event_time = treeview.item(selected_item)['values'][4]
            self.event_venue = treeview.item(selected_item)['values'][5]
            self.event_id = treeview.item(selected_item)['values'][6]
        
        except IndexError:
            messagebox.showerror("Error", "Please select an event to cancel.")
        else:
            self.dialogue_window = customtkinter.CTkToplevel(fg_color=("#EDF6FA", "#1B1B24"))
            self.dialogue_window.geometry("500x400")
            self.dialogue_window.title("Cancel this event?")
            self.dialogue_window.resizable(False, False)
            
            question_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Are you sure you want to cancel this event?",
                            font=customtkinter.CTkFont(size=16),
                            )
            question_label.place(x=250, y=20, anchor="center")
            
            event_name_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Name: " + self.event_name,
                            font=customtkinter.CTkFont(size=16),
                            )
            event_name_label.place(x=150, y=60, anchor="nw")
            
            event_description_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Description: " + f"{self.event_description[:15]}...",
                            font=customtkinter.CTkFont(size=16),
                            )
            event_description_label.place(x=150, y=100, anchor="nw")
            
            event_date_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Date: " + self.event_date,
                            font=customtkinter.CTkFont(size=16),
                            )
            event_date_label.place(x=150, y=140, anchor="nw")
            
            event_time_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Time: " + self.event_time,
                            font=customtkinter.CTkFont(size=16),
                            )
            event_time_label.place(x=150, y=180, anchor="nw")
            
            event_venue_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Venue: " + self.event_venue,
                            font=customtkinter.CTkFont(size=16),
                            )
            event_venue_label.place(x=150, y=220, anchor="nw")
            
            yes_button = customtkinter.CTkButton(
                            self.dialogue_window,
                            text="Yes (Cancel Event)",
                            width=140,
                            height=60,
                            font=customtkinter.CTkFont(size=16),
                            fg_color="#FF0000",
                            hover_color="#7D0000",
                            border_width=2,
                            border_color=("#1B1B24","#EDF6FA"),
                            corner_radius=15,
                            command=self.delete_event_from_database
                            )
            yes_button.place(x=145, y=330, anchor="center")
            
            no_button = customtkinter.CTkButton(
                            self.dialogue_window,
                            text="No (Go Back)",
                            width=140,
                            height=60,
                            font=customtkinter.CTkFont(size=16),
                            fg_color="#0065D9",
                            border_width=2,
                            border_color=("#1B1B24","#EDF6FA"),
                            corner_radius=15,
                            command=self.dialogue_window.destroy
                            )
            no_button.place(x=370, y=330, anchor="center")
    
    def delete_event_from_database(self):
        try:
            cursor.execute("""DELETE FROM events WHERE event_id = "{}";""".format(self.event_id))
            cnx.commit()                         
        except Exception as error:
            raise Exception("Error", str(error))  
        else:
            self.dialogue_window.destroy()
            EventSection(self.the_frame)

class EventHistory:
    def __init__(self, frame):
        self.the_frame = frame
        for widget in frame.winfo_children():
            widget.destroy()
        self.event_history(frame)
    
    def event_history(self, frame):
        
        go_back_button = customtkinter.CTkButton(
                        frame,
                        text="Go Back",
                        font=customtkinter.CTkFont(size=16),
                        fg_color="Green",
                        hover_color="#2AAAFA",
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command=lambda: EventSection(frame)
                        )
        go_back_button.grid(row=1, column=1, sticky="n", padx=35, pady=15)
        
        event_history_label = customtkinter.CTkLabel(
                        frame,
                        text='Completed Events',
                        font=customtkinter.CTkFont(size=24, weight="bold"),
                        )
        event_history_label.grid(row=1, column=2, columnspan=2, sticky="n", padx=35, pady=15)
 
        unmark_complete_button = customtkinter.CTkButton(
                        frame,
                        text='Unmark Complete',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        width=180, 
                        height=80, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command= self.unmark_complete
                        )
        unmark_complete_button.grid(row=2, column=1, sticky="n", padx=35, pady=5)
        
        export_data_button = customtkinter.CTkButton(
                        frame,
                        text='Export Data',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        width=180, 
                        height=80, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command=self.export_data
                        )
        export_data_button.grid(row=3, column=1, sticky="n", padx=35, pady=5)
        
        ##################################### Treeview #####################################
        
        style = ttk.Style()    
        style.theme_use("default")  
        style.configure("Treeview",
                        font=customtkinter.CTkFont(size=15),
                        background="#2A2D2E",
                        foreground="#EDF6FA",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=1)
        style.map('Treeview', background=[('selected', '#22559b')])
    
        style.configure("Treeview.Heading",
                        font=customtkinter.CTkFont(size=18, weight="bold"),
                        background="#3D3D3D",
                        foreground="#EDF6FA",
                        relief="flat")
        style.map("Treeview.Heading", background=[('active', '#0065D9')])
        
        self.treeview = ttk.Treeview(frame)
        self.treeview["columns"] = ("sr", "event_name", "event_description", "event_date", "event_time", "event_venue", "event_id",)
        self.treeview["show"] = "headings"
        
        self.treeview.column("sr", width=50, anchor="center")
        self.treeview.column("event_name", width=200, anchor="center")
        self.treeview.column("event_description", width=300, anchor="center")
        self.treeview.column("event_date", width=80, anchor="center")
        self.treeview.column("event_time", width=80, anchor="center")
        self.treeview.column("event_venue", width=150, anchor="center")
        self.treeview.column("event_id", width=200, anchor="center")
        
        self.treeview.heading("sr", text="Sr. No")
        self.treeview.heading("event_name", text="Title")
        self.treeview.heading("event_description", text="Description")
        self.treeview.heading("event_date", text="Date")
        self.treeview.heading("event_time", text="Time")
        self.treeview.heading("event_venue", text="Location")
        self.treeview.heading("event_id", text="Event ID")

        self.treeview.grid(row=2, column=2, rowspan=7, sticky="nsew", padx=10, pady=10)
        
        query = "SELECT event_name, event_description, event_date, event_time, event_venue, event_id FROM completed_events"
        while True:
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                break
            except mysql.connector.Error as err:
                print(f"[x] Error occured while executing query: {query}\n{err}")
                print("[*] Trying to load the treeview again...\n")
                print("--- While we are at it, check your database connection...\n")
                time.sleep(5)
                continue
            finally:
                for row in self.treeview.get_children():
                    self.treeview.delete(row)
                i=0
                for row in results:
                    i=i+1
                    self.treeview.insert("", "end", text="", values=(i, row[0], row[1], row[2], row[3], row[4], row[5]))
 
    def unmark_complete(self):
        try:
            selected_item = self.treeview.selection()[0]
            event_id = self.treeview.item(selected_item, "values")[6]
        except IndexError:
            messagebox.showerror("Error", "Please select an event to unmark it as complete.")
            return
        else:
            try:
                cursor.execute(f"""INSERT INTO events (event_name, event_description, event_date, event_time, event_venue, event_id) SELECT event_name, event_description, event_date, event_time, event_venue, event_id FROM completed_events WHERE event_id = "{event_id}";""")
                cursor.execute(f"DELETE FROM completed_events WHERE event_id = '{event_id}'")
                cnx.commit()  
            except Exception as err:
                raise Exception("Error", str(err))
            else:
                messagebox.showinfo("Success", "Event unmarked as complete.")
                EventHistory(self.the_frame)
    
    def export_data(self):
        self.dialogue_window = customtkinter.CTkToplevel(fg_color=("#EDF6FA", "#1B1B24"))
        self.dialogue_window.geometry("500x400")
        self.dialogue_window.title("Export Data")
        self.dialogue_window.resizable(False, False)
        
        question_label = customtkinter.CTkLabel(
                        self.dialogue_window,
                        text="Select the format in which you want to export the data.",
                        font=customtkinter.CTkFont(size=16),
                        )
        question_label.place(x=250, y=80, anchor="center")
        
        csv_button = customtkinter.CTkButton(
                        self.dialogue_window,
                        text=".CSV (Comma Separated Values)",
                        width=200,
                        height=60,
                        font=customtkinter.CTkFont(size=16),
                        fg_color="#0065D9",
                        hover_color="#19941B", 
                        border_width=2,
                        border_color=("#1B1B24","#EDF6FA"),
                        corner_radius=15,
                        command=self.export_data_csv
                        )
        csv_button.place(x=250, y=160, anchor="center")
        
        xlsx_button = customtkinter.CTkButton(
                        self.dialogue_window,
                        text=".XLSX (Excel Spreadsheet)",
                        width=200,
                        height=60,
                        font=customtkinter.CTkFont(size=16),
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        border_width=2,
                        border_color=("#1B1B24","#EDF6FA"),
                        corner_radius=15,
                        command=self.export_data_xlsx
                        )
        xlsx_button.place(x=250, y=240, anchor="center")   
    
    def export_data_csv(self):
        self.dialogue_window.destroy()
        filepath = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv'), ('All files', '*')]) 
        try:   
            cursor.execute("""SELECT event_name, event_description, event_date, event_time, event_venue FROM completed_events;""")
            data = cursor.fetchall()
        except Exception as error:
            raise Exception("Error", error)  
        else:
            if filepath:
                with open(filepath, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Sr. No.", "Event Name", "Event Description", "Event Date", "Event Time", "Event Venue"])
                    i = 0
                    for row in data:
                        i = i + 1
                        data = [i, row[0], row[1], row[2], row[3], row[4]]
                        writer.writerow(data)      
        finally:        
            EventHistory(self.the_frame)  
            
    def export_data_xlsx(self):
        self.dialogue_window.destroy()
        filepath = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[('Excel files', '*.xlsx'), ('All files', '*')])
        try:
            cursor.execute("""SELECT event_name, event_description, event_date, event_time, event_venue FROM completed_events;""")
            data = cursor.fetchall()
        except Exception as error:
            raise Exception("Error", error)
        else:
            if filepath:
                workbook = openpyxl.Workbook()
                sheet = workbook.active
                sheet.append(["Sr. No.", "Event Name", "Event Description", "Event Date", "Event Time", "Event Venue"])
                i = 0
                for row in data:
                    i= i + 1
                    newrow = [i, row[0], row[1], row[2], row[3], row[4]]
                    sheet.append(newrow)
                workbook.save(filepath)
        finally:        
            EventHistory(self.the_frame)

class ExportData:
    def __init__(self, frame):
        self.the_frame = frame
        self.dialogue_window = customtkinter.CTkToplevel(fg_color=("#EDF6FA", "#1B1B24"))
        self.dialogue_window.geometry("500x400")
        self.dialogue_window.title("Export Data")
        self.dialogue_window.resizable(False, False)
        
        question_label = customtkinter.CTkLabel(
                        self.dialogue_window,
                        text="Select the format in which you want to export the data.",
                        font=customtkinter.CTkFont(size=16),
                        )
        question_label.place(x=250, y=80, anchor="center")
        
        csv_button = customtkinter.CTkButton(
                        self.dialogue_window,
                        text=".CSV (Comma Separated Values)",
                        width=200,
                        height=60,
                        font=customtkinter.CTkFont(size=16),
                        fg_color="#0065D9",
                        hover_color="#19941B", 
                        border_width=2,
                        border_color=("#1B1B24","#EDF6FA"),
                        corner_radius=15,
                        command=self.export_data_csv
                        )
        csv_button.place(x=250, y=160, anchor="center")
        
        xlsx_button = customtkinter.CTkButton(
                        self.dialogue_window,
                        text=".XLSX (Excel Spreadsheet)",
                        width=200,
                        height=60,
                        font=customtkinter.CTkFont(size=16),
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        border_width=2,
                        border_color=("#1B1B24","#EDF6FA"),
                        corner_radius=15,
                        command=self.export_data_xlsx
                        )
        xlsx_button.place(x=250, y=240, anchor="center")   
    
    def export_data_csv(self):
        self.dialogue_window.destroy()
        filepath = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv'), ('All files', '*')]) 
        try:   
            cursor.execute("""SELECT event_name, event_description, event_date, event_time, event_venue FROM events;""")
            data = cursor.fetchall()
        except Exception as error:
            raise Exception("Error", error)  
        else:
            if filepath:
                with open(filepath, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Sr. No.", "Event Name", "Event Description", "Event Date", "Event Time", "Event Venue"])
                    i = 0
                    for row in data:
                        i = i + 1
                        data = [i, row[0], row[1], row[2], row[3], row[4]]
                        writer.writerow(data)      
        finally:        
            EventSection(self.the_frame)  
            
    def export_data_xlsx(self):
        self.dialogue_window.destroy()
        filepath = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[('Excel files', '*.xlsx'), ('All files', '*')])
        try:
            cursor.execute("""SELECT event_name, event_description, event_date, event_time, event_venue FROM events;""")
            data = cursor.fetchall()
        except Exception as error:
            raise Exception("Error", error)
        else:
            if filepath:
                workbook = openpyxl.Workbook()
                sheet = workbook.active
                sheet.append(["Sr. No.", "Event Name", "Event Description", "Event Date", "Event Time", "Event Venue"])
                i = 0
                for row in data:
                    i= i + 1
                    newrow = [i, row[0], row[1], row[2], row[3], row[4]]
                    sheet.append(newrow)
                workbook.save(filepath)
        finally:        
            EventSection(self.the_frame)