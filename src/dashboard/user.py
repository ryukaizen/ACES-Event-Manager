import customtkinter

customtkinter.set_appearance_mode("light") 
customtkinter.set_default_color_theme("dark-blue")

class UserDashboard:
    def __init__(self, window):
    # def guest_dashboard(window):
        window.title("User Dashboard | AEM")
        window.resizable(True, True)
        window.geometry(f"{int(window.winfo_screenwidth())}x{int(window.winfo_screenheight())}")