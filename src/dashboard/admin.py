import customtkinter
import subprocess

from tkinter import messagebox
from PIL import Image
from ..database.db_connect import cursor
from .sections.events import EventSection
from .sections.broadcast import BroadcastSection
from .sections.users import UsersSection

customtkinter.set_appearance_mode("light") 
customtkinter.set_default_color_theme("dark-blue")

class AdminDashboard:
    def __init__(self, window):
        window.title("Admin Dashboard | AEM")
        window.resizable(True, True)
        window.geometry(f"{int(window.winfo_screenwidth())}x{int(window.winfo_screenheight())}")
    
        title_frame = customtkinter.CTkFrame(
                        window, 
                        fg_color=("#EDF6FA", "#1B1B24"), 
                        width=int(window.winfo_screenwidth()), 
                        height=100, 
                        corner_radius=0
                        )
        title_frame.pack(fill="x", side="top")
        
        dashboard_label1 = customtkinter.CTkLabel(
                            title_frame, 
                            text="A E M", 
                            font=customtkinter.CTkFont(size=30, weight="bold")
                            )
        dashboard_label1.place(relx=0.5, rely=0.1, anchor="n")
        
                
        welcome_name_label = customtkinter.CTkLabel(
                            title_frame, 
                            text=f"Welcome", 
                            font=customtkinter.CTkFont(size=16)
                            )
        f = open('src/dashboard/sections/session.txt', 'r')
        username = f.read()
        f.close()
        try:
            cursor.execute("""SELECT full_name FROM users WHERE username = "{}";""".format(username))
            full_name = cursor.fetchone()[0]
        except Exception as e:
            print(e)
        else:
            welcome_name_label.configure(text=f"Welcome, {full_name}")
        finally:
            welcome_name_label.place(relx=0.71, rely=0.13, anchor="n")
            
        logout_button = customtkinter.CTkButton(
                        title_frame,
                        text="LOGOUT",
                        width=60,
                        height=40,
                        font=customtkinter.CTkFont(size=16),
                        fg_color="Green",
                        hover_color="#2AAAFA",
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command=lambda: self.logout(window)
                        )
        logout_button.place(relx=0.71, rely=0.5, anchor="n")

        aces_logo = customtkinter.CTkImage(
                    dark_image=Image.open("assets/images/logo.png"), 
                    size=(int(window.winfo_screenwidth() / 14), int(window.winfo_screenwidth() / 14))
                    )
        aces_logo_frame_label = customtkinter.CTkLabel(
                                title_frame, 
                                text="", 
                                image=aces_logo
                                )
        aces_logo_frame_label.place(relx=0.053, rely=0.03, anchor="nw")

        dbatu_logo = customtkinter.CTkImage(
                    dark_image=Image.open("assets/images/BATU_logo.png"), 
                    size=(int(window.winfo_screenwidth() / 14), int(window.winfo_screenwidth() / 14))
                    )
        dbatu_logo_frame_label = customtkinter.CTkLabel(
                                title_frame, 
                                text="", 
                                image=dbatu_logo
                                )
        dbatu_logo_frame_label.place(relx=0.93, rely=0.025, anchor="ne")
        
        
        
        dashboard_label1 = customtkinter.CTkLabel(
                            title_frame, 
                            text="ACES Event Manager", 
                            font=customtkinter.CTkFont(size=22, weight="bold")
                            )
        dashboard_label1.place(relx=0.5, rely=0.85, anchor="s")
        
        self.section_segment_button = customtkinter.CTkSegmentedButton(
                                window,
                                font=customtkinter.CTkFont(size=20, weight="bold"),
                                border_width=5,
                                height=55,
                                selected_color="#0065D9", 
                                selected_hover_color="#2AAAFA",
                                unselected_color="#D96C00",
                                unselected_hover_color="#FF8C00",
                                fg_color=("#EDF6FA", "#1B1B24"),
                                bg_color=("#EDF6FA", "#1B1B24"),
                                values=["Events", "Broadcast", "Committee", "Users", "Options"],
                                command=self.section_choice,
                                corner_radius=15,
                                )
        self.section_segment_button.pack(fill="x", side="top", pady=2)
        
        self.section_segment_button.set("Events")
        
        self.body_frame = customtkinter.CTkFrame(
                        window,
                        border_width=2,
                        border_color=("#1B1B24", "#EDF6FA"), 
                        fg_color=("#EDF6FA", "#1B1B24"), 
                        height=55, 
                        corner_radius=0
                        )
        self.body_frame.pack(expand=True, fill="both", side="bottom")
        
        self.footer_label = customtkinter.CTkLabel(
                               window,
                               text="© Department of Computer Engineering, Dr. Babasaheb Ambedkar Technological University, Lonere.",
                               text_color="white",
                               font=customtkinter.CTkFont(size=15),
                               bg_color="black",
                               height=35,
                               corner_radius=0
                               )
        self.footer_label.place(x=0, y=1, relx=0, rely=1, relwidth=1.0, anchor="sw") 
        
        EventSection(self.body_frame)
        
    def section_choice(self, value):
    
        if value == "Events":
            EventSection(self.body_frame)
        elif value == "Broadcast":
            BroadcastSection(self.body_frame)
        # elif value == "Committee":
        #     self.committee_section()
        elif value == "Users":
            UsersSection(self.body_frame)
        # elif value == "Options":
        #     self.options_section()

    def logout(self, window):
        try:
            f = open('src/dashboard/sections/session.txt', 'w')
            f.write("")
            f.close()
            messagebox.showinfo("Logout", "You have been logged out successfully.")
            window.destroy()
        except Exception:
            pass
        finally:
            subprocess.run(["python", "app.py"])