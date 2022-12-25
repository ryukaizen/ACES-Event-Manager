import customtkinter

from tkinter import ttk
from ...database.db_connect import cursor, cnx

customtkinter.set_appearance_mode("light") 
customtkinter.set_default_color_theme("dark-blue")

class EventSection:
    def __init__(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        self.event_frame(frame)
        
    def event_frame(self, frame):  
        
        add_event_button = customtkinter.CTkButton(
                        frame,
                        text='Add Event',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        width=180, 
                        height=70, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        )
        add_event_button.grid(row=1, column=1, sticky="n", padx=35, pady=10)
        
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
        
        test_another_button = customtkinter.CTkButton(
                        frame,
                        text='Test Button',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        width=180, 
                        height=70, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        )
        test_another_button.grid(row=5, column=1, sticky="s", padx=35, pady=10)