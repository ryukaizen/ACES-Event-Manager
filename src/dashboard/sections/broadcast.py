import customtkinter
import mysql.connector
import os
import time
import smtplib

from tkinter import ttk, messagebox, filedialog
from ...database.db_connect import cursor, cnx
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

load_dotenv()
msg = MIMEMultipart()

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_EMAIL_PASS = os.getenv('ADMIN_EMAIL_PASS')
EMAIL_SERVER_HOST = os.getenv('EMAIL_SERVER_HOST')
EMAIL_SERVER_PORT = os.getenv('EMAIL_SERVER_PORT') 

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
        
        self.selected_attachment_label = customtkinter.CTkLabel(
                        frame,
                        text="Selected Attachment: None",
                        font=customtkinter.CTkFont(size=16), 
                        )
        self.selected_attachment_label.place(relx=0.88, rely=0.2, anchor="center")
        
        # Set to None as attachment is not set initially
        self.attachment_filepath = None
        
        add_attachment_button = customtkinter.CTkButton(
                        frame,
                        text="Attach Flyer",
                        font=customtkinter.CTkFont(size=16),
                        fg_color="#0065D9",
                        border_width=2,
                        border_color=("#1B1B24","#EDF6FA"),
                        corner_radius=15,
                        command=self.get_attachment_filepath
                        )
        add_attachment_button.place(relx=0.88, rely=0.3, anchor="n") 
        
        self.socialmedia_checkbox = customtkinter.CTkCheckBox(
                        frame, 
                        text="Include Social Media Links",
                        font=customtkinter.CTkFont(size=16), 
                        onvalue="on", 
                        offvalue="off")
        self.socialmedia_checkbox.place(relx=0.88, rely=0.45, anchor="n") 
        
        test_publish_button = customtkinter.CTkButton(
                            frame,
                            text="Test Publish",
                            font=customtkinter.CTkFont(size=18), 
                            fg_color="#0065D9",
                            hover_color="#19941B",  
                            width=180, 
                            height=65, 
                            border_width=3,
                            border_color=("#EDF6FA", "#1B1B24"),
                            corner_radius=15,
                            command=self.prompt_test_publish
                            )
        test_publish_button.place(relx=0.88, rely=0.6, anchor="n") 
        
        publish_button = customtkinter.CTkButton(
                            frame,
                            text="Publish",
                            font=customtkinter.CTkFont(size=20, weight="bold"), 
                            fg_color="#D96C00",
                            hover_color="#FF8C00",  
                            width=180, 
                            height=65, 
                            border_width=3,
                            border_color=("#EDF6FA", "#1B1B24"),
                            corner_radius=15,
                            # command=self.prompt_publish
                            )
        publish_button.place(relx=0.88, rely=0.75, anchor="n") 
        
        ################################ Insert existing values ################################
        
        self.event_name_entry.insert(0, self.event_name)
        self.event_description_entry.insert("0.0", self.event_description.strip())
        self.event_date_entry.insert(0, self.event_date)
        self.event_time_entry.insert(0, self.event_time)
        self.event_venue_entry.insert(0, self.event_venue.strip())
        
        # Make checkbox by default checked (Enabled including social media links)
        self.socialmedia_checkbox.select()
        
        # This inserts already generated content in the textbox, if any exists
        try:
            query = """SELECT content FROM broadcast WHERE event_id = "{}";""".format(self.event_id)
            cursor.execute(query)
            content = cursor.fetchone()[0]
        except Exception:
            messagebox.showinfo("Configure Email Content", "Found no saved content for event_id: {}\n\nKindly generate content first, edit it by your own according and then save it for later use.".format(self.event_id))
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
        if len(final_content) == 0:
            messagebox.showerror("Error", "Content is empty!")
            return 
        
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
    
    def get_attachment_filepath(self):
        self.attachment_filepath = filedialog.askopenfilename(multiple=True)
        
        # THIS IS JUST TO DISPLAY THE USER THAT HE HAS SELECTED THE RIGHT FILE/s
        # Get the filename/s from the filepath/s
        file_names = [os.path.basename(file_path) for file_path in self.attachment_filepath]
        
        # Join the filenames with a comma and update the label
        self.selected_attachment_label.configure(text=("Selected Attachment: \n" + ",".join(file_names)))
            
    def prompt_test_publish(self):
        self.body = self.generated_content.get("0.0", "end-1c")
        if len(self.body) == 0:
            messagebox.showerror("Error", "Please generate content first!")
        else:
            self.dialogue_window = customtkinter.CTkToplevel(fg_color=("#EDF6FA", "#1B1B24"))
            self.dialogue_window.geometry("600x400")
            self.dialogue_window.title("Test Publish Email")
            self.dialogue_window.resizable(False, False)
            
            question_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="This will send a trial email to yourself, \naccording to the configuration you've done.",
                            font=customtkinter.CTkFont(size=20, weight="bold", slant="roman")
                            )
            question_label.place(relx=0.5, rely=0.1, anchor="n")
        
            subject_label = customtkinter.CTkLabel(
                            self.dialogue_window,
                            text="Subject:",
                            font=customtkinter.CTkFont(size=20, slant="roman")
                            )
            subject_label.place(relx=0.2, rely=0.3, anchor="n")
        
            self.subject_entry = customtkinter.CTkEntry(
                            self.dialogue_window,                    
                            width=420,
                            height=30,
                            font=customtkinter.CTkFont(size=20),
                            border_width=3,
                            border_color=("#1B1B24", "#EDF6FA"),
                            corner_radius=10,
                            )
            self.subject_entry.place(relx=0.5, rely=0.38, anchor="n")
        
            xtest_publish_button = customtkinter.CTkButton(
                            self.dialogue_window,
                            text="Publish",
                            font=customtkinter.CTkFont(size=20, weight="bold"), 
                            fg_color="#D96C00",
                            hover_color="#FF8C00", 
                            width=180, 
                            height=65, 
                            border_width=3,
                            border_color=("#EDF6FA", "#1B1B24"),
                            corner_radius=15,
                            command=self.test_publish
                            )
            xtest_publish_button.place(relx=0.3, rely=0.55, anchor="n")
        
            cancel_button = customtkinter.CTkButton(
                            self.dialogue_window,
                            text="Cancel",
                            font=customtkinter.CTkFont(size=20, weight="bold"), 
                            fg_color="#0065D9",
                            hover_color="#FF0000",  
                            width=180, 
                            height=65, 
                            border_width=3,
                            border_color=("#EDF6FA", "#1B1B24"),
                            corner_radius=15,
                            command=lambda: self.dialogue_window.destroy()
                            )
            cancel_button.place(relx=0.7, rely=0.55, anchor="n") 
        
    def test_publish(self):
        subject = self.subject_entry.get()
        if len(subject) == 0:
            messagebox.showerror("Error", "Subject is empty!")
            return
        
        # Fetch logged in user's username from session file
        f = open('src/dashboard/sections/session.txt', 'r')
        username = f.read()
        f.close()
        
        # Using previously fetched username, fetch their email from database
        try:
            cursor.execute("""SELECT email FROM users WHERE username = "{}";""".format(username))
            email = cursor.fetchall()[0][0]
        except Exception as error:
            raise Exception("Error", str(error))
        else:
            msg['Subject'] = subject
            msg['From'] = ADMIN_EMAIL
            msg['To'] = email
        
            msg.attach(MIMEText(self.body, 'plain'))
            
            if self.attachment_filepath != None:
                # Attach each file to the email
                for file_path in self.attachment_filepath:
                    with open(file_path, "rb") as f:
                        attachment = MIMEApplication(f.read(), _subtype="octet-stream")
                        attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(file_path))
                        msg.attach(attachment)
            
            try:
                server = smtplib.SMTP(EMAIL_SERVER_HOST, EMAIL_SERVER_PORT)
                server.starttls()
                server.login(ADMIN_EMAIL, ADMIN_EMAIL_PASS)
                server.send_message(msg)
                server.quit()
                del msg['From']
                del msg['Subject']
                del msg['To']
                self.body = ""
            
            except Exception as error:
                raise Exception("Error:", str(error))
            else:
                self.dialogue_window.destroy()
                messagebox.showinfo("Success", "Email sent successfully!")
                # self.publish_email(self.the_frame)
        
