import customtkinter

customtkinter.set_appearance_mode("light") 
customtkinter.set_default_color_theme("dark-blue")

class GuestDashboard:
    def __init__(self, window):
    # def guest_dashboard(window):
        window.title("Guest View | AEM")
        window.resizable(True, True)
        window.deiconify()
        window.geometry(f"{int(window.winfo_screenwidth())}x{int(window.winfo_screenheight())}")