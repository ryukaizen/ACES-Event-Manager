import customtkinter

from tkinter import ttk

from ...database.db_connect import cursor, cnx

customtkinter.set_appearance_mode("light") 
customtkinter.set_default_color_theme("dark-blue")

class VenueSection:
    def __init__(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        self.venue_frame(frame)

    def venue_frame(self, frame):  
        
        venue_submit_button = customtkinter.CTkButton(
                        frame,
                        text='Add Venue',
                        font=customtkinter.CTkFont(size=18, weight="bold"), 
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        width=180, 
                        height=70, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        )
        venue_submit_button.grid(row=3, column=3, sticky="nsew")