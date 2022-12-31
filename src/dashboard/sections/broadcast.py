import customtkinter
import tkinter
import mysql.connector
import time

from tkinter import ttk, messagebox, filedialog
from ...database.db_connect import cursor, cnx

customtkinter.set_appearance_mode("light") 
customtkinter.set_default_color_theme("dark-blue")

class BroadcastSection:
    def __init__(self, frame):
        self.the_frame = frame
    
        for widget in frame.winfo_children():
            widget.destroy()
        
        publish_email_button = customtkinter.CTkButton(
                        frame,
                        text='Publish on Email',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#FF002F",
                        hover_color="#7D0017",  
                        width=180, 
                        height=65, 
                        corner_radius=30,
                        command= lambda: PublishEmail(frame, treeview)
                        )
        publish_email_button.place(relx=0.3, rely=0.1, anchor="n")
        
        publish_telegram_button = customtkinter.CTkButton(
                        frame,
                        text='Publish on Telegram',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#229ED9",
                        hover_color="#004E99",  
                        width=180, 
                        height=65, 
                        corner_radius=30,
                        # command= lambda: MarkCompleted(frame, treeview)
                        )
        publish_telegram_button.place(relx=0.5, rely=0.1, anchor="n")
        
        publish_whatsapp_button = customtkinter.CTkButton(
                        frame,
                        text='Publish on WhatsApp',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#25D366",
                        hover_color="#128C7E",  
                        width=180, 
                        height=65, 
                        corner_radius=30,
                        # command= lambda: UpdateEvent(frame, treeview)
                        )
        publish_whatsapp_button.place(relx=0.7, rely=0.1, anchor="n")
    
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
        treeview.column("event_name", width=250, anchor="center")
        treeview.column("event_description", width=350, anchor="center")
        treeview.column("event_date", width=80, anchor="center")
        treeview.column("event_time", width=80, anchor="center")
        treeview.column("event_venue", width=250, anchor="center")
        treeview.column("event_id", width=250, anchor="center")
        
        treeview.heading("sr", text="Sr. No")
        treeview.heading("event_name", text="Title")
        treeview.heading("event_description", text="Description")
        treeview.heading("event_date", text="Date")
        treeview.heading("event_time", text="Time")
        treeview.heading("event_venue", text="Location")
        treeview.heading("event_id", text="Event ID")

        treeview.place(relx=0.5, rely=0.3, anchor="n")
        
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
                    
class PublishEmail:
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
            messagebox.showerror("Error", "Please select an event to publish using email.")
        else:
            for widget in frame.winfo_children():
                widget.destroy()
            self.publish_email(frame) 
    
    def publish_email(self, frame): 
            
        go_back_button = customtkinter.CTkButton(
                        frame,
                        text="Go Back",
                        font=customtkinter.CTkFont(size=16),
                        fg_color="Green",
                        hover_color="#2AAAFA",
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command=lambda: BroadcastSection(frame)
                        )
        go_back_button.place(relx=0.08, rely=0.02, anchor="n") 
        
        configure_content_label = customtkinter.CTkLabel(
                        frame,
                        text='Configure the Email Content',
                        font=customtkinter.CTkFont(size=26, weight="bold"),
                        )
        configure_content_label.place(relx=0.5, rely=0.02, anchor="n")
        
        event_name_label = customtkinter.CTkLabel(
                        frame,
                        text='Name:',
                        font=customtkinter.CTkFont(size=18), 
                        )
        event_name_label.place(x=80, y=80, anchor="center")
        
        self.event_name_entry = customtkinter.CTkEntry(
                        frame,
                        width=330,
                        height=25,
                        font=customtkinter.CTkFont(size=18),
                        border_width=3,
                        border_color=("#1B1B24", "#EDF6FA"),
                        corner_radius=10,
                        )
        self.event_name_entry.place(x=280, y=80, anchor="center")
        
        event_description_label = customtkinter.CTkLabel(
                        frame,
                        text='Description:',
                        font=customtkinter.CTkFont(size=18), 
                        )
        event_description_label.place(x=100, y=120, anchor="center")
            
        self.event_description_entry = customtkinter.CTkTextbox(
                        frame,
                        text_color=("#1B1B24", "#EDF6FA"),
                        width=400,
                        height=200,
                        font=customtkinter.CTkFont(size=18),
                        border_width=3,
                        border_color=("#1B1B24", "#EDF6FA"),
                        corner_radius=10,
                        )
        self.event_description_entry.place(x=250, y=240, anchor="center")
        
        event_date_label = customtkinter.CTkLabel(
                        frame,
                        text='Date:',
                        font=customtkinter.CTkFont(size=18), 
                        )
        event_date_label.place(x=80, y=380, anchor="center")
        
        self.event_date_entry = customtkinter.CTkEntry(
                        frame,
                        width=100,
                        height=25,
                        font=customtkinter.CTkFont(size=18),
                        border_width=3,
                        border_color=("#1B1B24", "#EDF6FA"),
                        corner_radius=10,
                        )
        self.event_date_entry.place(x=100, y=420, anchor="center")
        
        event_time_label = customtkinter.CTkLabel(
                        frame,
                        text="Time:",
                        font=customtkinter.CTkFont(size=18), 
                        )
        event_time_label.place(x=200, y=380, anchor="center")
        
        self.event_time_entry = customtkinter.CTkEntry(
                        frame,
                        width=100,
                        height=25,
                        font=customtkinter.CTkFont(size=18),
                        border_width=3,
                        border_color=("#1B1B24", "#EDF6FA"),
                        corner_radius=10,
                        )
        self.event_time_entry.place(x=220, y=420, anchor="center")
        
        event_venue_label = customtkinter.CTkLabel(
                        frame,
                        text="Venue:",
                        font=customtkinter.CTkFont(size=18), 
                        )
        event_venue_label.place(x=320, y=380, anchor="center")
        
        self.event_venue_entry = customtkinter.CTkEntry(
                        frame,
                        width=160,
                        height=25,
                        font=customtkinter.CTkFont(size=18),
                        border_width=3,
                        border_color=("#1B1B24", "#EDF6FA"),
                        corner_radius=10,
                        )
        self.event_venue_entry.place(x=370, y=420, anchor="center")
        
        generate_content_button = customtkinter.CTkButton(
                            frame,
                            text="Generate Content",
                            font=customtkinter.CTkFont(size=18), 
                            fg_color="#0065D9",
                            hover_color="#19941B",  
                            width=180, 
                            height=65, 
                            border_width=3,
                            border_color=("#EDF6FA", "#1B1B24"),
                            corner_radius=15,
                            command=self.generate_email_text 
                            )
        generate_content_button.place(x=660, y=410, anchor="center")
        
        save_content_button = customtkinter.CTkButton(
                            frame,
                            text="Save Content",
                            font=customtkinter.CTkFont(size=18), 
                            fg_color="#0065D9",
                            hover_color="#19941B",  
                            width=180, 
                            height=65, 
                            border_width=3,
                            border_color=("#EDF6FA", "#1B1B24"),
                            corner_radius=15,
                            command=self.save_generated_content
                            )
        save_content_button.place(x=900, y=410, anchor="center")
        
        self.generated_content = customtkinter.CTkTextbox(
                        frame,
                        text_color=("#1B1B24", "#EDF6FA"),
                        width=550,
                        height=290,
                        font=customtkinter.CTkFont(size=18),
                        border_width=3,
                        border_color=("#1B1B24", "#EDF6FA"),
                        corner_radius=10,
                        )
        self.generated_content.place(x=780, y=220, anchor="center")
        
        add_attachment_button = customtkinter.CTkButton(
                        frame,
                        text="Attach Flyer",
                        font=customtkinter.CTkFont(size=16),
                        fg_color="#0065D9",
                        border_width=2,
                        border_color=("#1B1B24","#EDF6FA"),
                        corner_radius=15,
                        # command=lambda: BroadcastSection(frame)
                        )
        add_attachment_button.place(relx=0.8, rely=0.02, anchor="n") 
        
        ################################ Insert existing values ################################
        
        self.event_name_entry.insert(0, self.event_name)
        self.event_description_entry.insert("0.0", self.event_description)
        self.event_date_entry.insert(0, self.event_date)
        self.event_time_entry.insert(0, self.event_time)
        self.event_venue_entry.insert(0, self.event_venue)
        
        # This inserts already generated content in the textbox, if any exists
        try:
            query = """SELECT content FROM broadcast WHERE event_id = "{}";""".format(self.event_id)
            cursor.execute(query)
            content = cursor.fetchone()[0]
        except Exception:
            print("\nFound no saved content for event_id:", self.event_id)
        else:
            if content:
                self.generated_content.insert("0.0", content)

    def generate_email_text(self):
        event_name = self.event_name_entry.get()
        event_description = self.event_description_entry.get("0.0", "end-1c")
        event_date = self.event_date_entry.get()
        event_time = self.event_time_entry.get()
        event_venue = self.event_venue_entry.get()
        
        # Remove extra empty lines from the end
        event_name = event_name.strip()
        event_description = event_description.strip()
        event_venue = event_venue.strip()
        
        email_text = f"""Hello,\n\n{event_name} is coming up soon!\n\n{event_description}\n\nDate: {event_date}\nTime: {event_time}\nVenue: {event_venue}\n\nPS: Participate in large numbers!\n\nRegards,\nTeam ACES"""
        
        self.generated_content.delete("0.0", "end")
        self.generated_content.insert("0.0", email_text)
    
    def save_generated_content(self):
        final_content = self.generated_content.get("0.0", "end-1c")
        
        # Remove extra empty lines from the end
        final_final_content = final_content.strip()
        
        # Format it as per MySQL entry
        escaped_final_content = mysql.connector.conversion.MySQLConverter().escape(final_final_content) 
        self.final_final_final_content = escaped_final_content
               
        try:
            query = """INSERT INTO broadcast (event_id, content) VALUES ("{}", "{}") ON DUPLICATE KEY UPDATE content = "{}";""".format(self.event_id,  self.final_final_final_content,  self.final_final_final_content)
            cursor.execute(query)
            cnx.commit() 
        except Exception as error:
            raise Exception("Error", str(error))  
        else:
            messagebox.showinfo("Success", "Content saved successfully!")
            
