import customtkinter

from ...database.db_connect import cursor, cnx

customtkinter.set_appearance_mode("light") 
customtkinter.set_default_color_theme("dark-blue")

class UsersSection:
    def __init__(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
   
        register_user_button = customtkinter.CTkButton(
                        frame,
                        text='Register User',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        width=180, 
                        height=65, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        # command= lambda: RegisterUser(frame)
                        )
        register_user_button.grid(row=1, column=1, sticky="n", padx=35, pady=5)