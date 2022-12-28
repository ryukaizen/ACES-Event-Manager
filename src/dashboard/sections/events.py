import customtkinter
import mysql.connector
import time
import uuid

from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
from ...database.db_connect import cursor, cnx

customtkinter.set_appearance_mode("light") 
customtkinter.set_default_color_theme("dark-blue")

class EventSection:
    def __init__(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        self.event_frame(frame)
        self.event_treeview(frame)
        
    def event_frame(self, frame):  
        
        new_event_button = customtkinter.CTkButton(
                        frame,
                        text='New Event',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        width=180, 
                        height=70, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command= lambda: NewEvent(frame)
                        )
        new_event_button.grid(row=1, column=1, sticky="n", padx=35, pady=10)
        
        update_event_button = customtkinter.CTkButton(
                        frame,
                        text='Update Event',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        width=180, 
                        height=70, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        )
        update_event_button.grid(row=2, column=1, sticky="n", padx=35, pady=10)
        
        remove_event_button = customtkinter.CTkButton(
                        frame,
                        text='Remove Event',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#FF0000",  
                        width=180, 
                        height=70, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        )
        remove_event_button.grid(row=3, column=1, sticky="s", padx=35, pady=10)
        
        event_history_button = customtkinter.CTkButton(
                        frame,
                        text='Event History',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        width=180, 
                        height=70, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        )
        event_history_button.grid(row=4, column=1, sticky="s", padx=35, pady=10)
        
        export_data_button = customtkinter.CTkButton(
                        frame,
                        text='Export Data',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        width=180, 
                        height=70, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        )
        export_data_button.grid(row=5, column=1, sticky="s", padx=35, pady=10)
        
    def event_treeview(self, frame):
        
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
        treeview.column("event_venue", width=100, anchor="center")
        treeview.column("event_id", width=250, anchor="center")
        
        treeview.heading("sr", text="Sr. No")
        treeview.heading("event_name", text="Title")
        treeview.heading("event_description", text="Description")
        treeview.heading("event_date", text="Date")
        treeview.heading("event_time", text="Time")
        treeview.heading("event_venue", text="Location")
        treeview.heading("event_id", text="Event ID")

        treeview.grid(row=1, column=2, rowspan=5, sticky="nsew", padx=10, pady=10)
        
        query = "SELECT event_name, event_description, event_date, event_time, event_venue, event_id FROM events"
        while True:
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                print(results)
                break
            except mysql.connector.Error as err:
                print(f"[x] Error occured while executing query: {query}\n{err}")
                print("[*] Trying to load the treeview again...\n")
                print("--- While we are at it, check your database connection...\n")
                time.sleep(5)
                continue
            finally:
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
                            day=today.day
                            )
        self.event_date_calendar.place(x=740, y=190, anchor="center")
        
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

        self.hour_menu = customtkinter.CTkOptionMenu(frame, 
                                                 values=['12', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11'],
                                                 corner_radius=10,
                                                 width=60
                                                )
        self.hour_menu.place(x=1040, y=80, anchor="center")
        
        self.minute_menu = customtkinter.CTkOptionMenu(frame, 
                                                    values=['00', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55'],
                                                    corner_radius=10,
                                                    width=60
                                                    )
        self.minute_menu.place(x=1110, y=80, anchor="center")
        
        self.ampm_menu = customtkinter.CTkOptionMenu(frame, 
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
        self.event_description = self.event_description_entry.get("0.0", "end")
        self.event_date = self.select_date()
        self.event_time = self.select_time()
        self.event_venue = self.event_venue_entry.get("0.0", "end")
        
        error_message = ""
        if not self.event_name:
            error_message += "Please provide event name.\n"
        if len(self.event_description) == 1:
            error_message += "Please provide event description.\n"
        if len(self.event_venue) == 1:
            error_message += "Please provide event venue.\n"
              
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
            event_name_label.place(x=250, y=60, anchor="center")
            
            event_description_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Description: " + f"{self.event_description[:15]}...",
                            font=customtkinter.CTkFont(size=16),
                            )
            event_description_label.place(x=250, y=100, anchor="center")
            
            event_date_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Date: " + self.event_date,
                            font=customtkinter.CTkFont(size=16),
                            )
            event_date_label.place(x=250, y=140, anchor="center")
            
            event_time_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Time: " + self.event_time,
                            font=customtkinter.CTkFont(size=16),
                            )
            event_time_label.place(x=250, y=180, anchor="center")
            
            event_venue_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Event Venue: " + self.event_venue,
                            font=customtkinter.CTkFont(size=16),
                            )
            event_venue_label.place(x=250, y=220, anchor="center")
            
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
        
        # This generates unique ID for event 
        self.event_id = uuid.uuid5(uuid.NAMESPACE_OID, f"{self.event_name}{self.event_date}{self.event_time}{self.event_venue}")
        
        # Escape special characters in event description
        eventdesc = mysql.connector.conversion.MySQLConverter().escape(self.event_description)
        
        # For future purposes (date and time is being stored as string as of now)
        # # This converts the date from string to datetime object 
        # date_format = "%d/%m/%y"  
        # date = datetime.strptime(self.event_date, date_format)
        
        # # This converts the time from string to datetime object     
        # time_format = "%I:%M %p"
        # time = datetime.strptime(self.event_time, time_format)
        
        try:
            cursor.execute("""INSERT INTO events(event_name, event_description, event_date, event_time, event_venue, event_id) VALUES ("{}", "{}", "{}", "{}", "{}", "{}");""".format(
                                self.event_name, eventdesc, self.event_date, self.event_time,  self.event_venue, self.event_id)
                        )
            cnx.commit()                         
        except Exception as error:
            raise Exception("Error", str(error))  
        else:
            self.dialogue_window.destroy()
            EventSection(self.the_frame)
            