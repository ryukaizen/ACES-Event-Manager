import customtkinter
import re

from tkinter import messagebox 
from PIL import Image
from src.database.db_connect import cursor, cnx
from src.dashboard.admin import AdminDashboard
from src.dashboard.user import UserDashboard
from src.dashboard.guest import GuestDashboard

customtkinter.set_appearance_mode("light") 
customtkinter.set_default_color_theme("dark-blue")

class AEM(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.screen_size = (f"{int(self.screen_width * 0.8)}x{int(self.screen_height * 0.8)}")
        print(f"[*] Screen resolution detected: {self.screen_width}x{self.screen_height}\n--- Current window size: {self.screen_size}")
        self.geometry(self.screen_size)
        self.title("Welcome to AEM - ACES Event Manager")
        self.resizable(False, False)
        
        self.startup_bg = customtkinter.CTkImage(
                            dark_image=Image.open('assets/images/bg.png'), 
                            size=(int(self.screen_width * 0.8), int(self.screen_height * 0.8)))
        self.background_label = customtkinter.CTkLabel(
                                self, 
                                text="", 
                                image=self.startup_bg
                                )
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.left_frame = customtkinter.CTkFrame(
                            self,
                            width=int(self.screen_width * 0.2), 
                            height=int(self.screen_height * 0.8), 
                            corner_radius=0
                            )
        self.left_frame.place(relx=0.25, rely=1, relwidth=0.25, relheight=1, anchor="s")
        
        self.right_frame = customtkinter.CTkFrame(
                            self,
                            fg_color="transparent",
                            width=int(self.screen_width * 0.4), 
                            height=int(self.screen_height * 0.4), 
                            corner_radius=0
                            )
        self.right_frame.place(relx=0.69, rely=0.85, relwidth=0.4, relheight=0.75, anchor="s")
        
        self.logo_label1 = customtkinter.CTkLabel(
                            self.left_frame, 
                            text="A E M", 
                            font=customtkinter.CTkFont(size=30, weight="bold")
                            )
        self.logo_label1.place(relx=0.5, rely=0.1, anchor="n")

        self.logo = customtkinter.CTkImage(
                    dark_image=Image.open("assets/images/logo.png"), 
                    size=(int(self.screen_width / 6), int(self.screen_width / 6))
                    )
        self.logo_frame_label = customtkinter.CTkLabel(
                                self.left_frame, 
                                text="", 
                                image=self.logo
                                )
        self.logo_frame_label.place(relx=0.5, rely=0.55, anchor="s")
        
        self.logo_label2 = customtkinter.CTkLabel(
                            self.left_frame, 
                            text="ACES Event Manager", 
                            font=customtkinter.CTkFont(size=22, weight="bold")
                            )
        self.logo_label2.place(relx=0.5, rely=0.65, anchor="s")
        
        self.switch_var = customtkinter.StringVar(value="light")
        self.theme_switch = customtkinter.CTkSwitch(
                            self.left_frame, 
                            text="Toggle Dark Mode",
                            variable=self.switch_var, 
                            onvalue="dark", 
                            offvalue="light", 
                            command=self.change_appearance_mode
                            )
        self.theme_switch.place(relx=0.5, rely=0.75, anchor="s")
        
        self.tabview = customtkinter.CTkTabview(
                            self.right_frame,
                            bg_color=("gray90", "gray13"), 
                            width=int(self.screen_width * 0.5), 
                            height=int(self.screen_height * 0.6), 
                            corner_radius=15)
        
        self.tabview.pack(side="right")
        self.tabview.add("Sign-in")
        self.tabview.add("Register")
        self.tabview.set("Sign-in")
        
        ########################################### Sign-in Tab ###########################################
        
        self.login_username_label = customtkinter.CTkLabel(self.tabview.tab("Sign-in"),
                        text="Username",
                        font=("Copperplate", 20),
                        width=int(self.screen_width * 0.09),
                        height=int(self.screen_height * 0.03),
                        corner_radius=0
                        )
        self.login_username_label.place(x=40,y=40)

        self.login_username_entry = customtkinter.CTkEntry(self.tabview.tab("Sign-in"),
                        placeholder_text="Enter your PRN",
                        font=("Consolas", 16),
                        width=290,
                        height=40,
                        border_width=2,
                        corner_radius=10
                        )
        self.login_username_entry.place(x=50,y=80)

        self.login_password_label = customtkinter.CTkLabel(self.tabview.tab("Sign-in"),
                        text="Password",
                        font=("Copperplate", 20),
                        width=120,
                        height=25,
                        corner_radius=0
                        )
        self.login_password_label.place(x=40,y=140)
    
        self.login_password_entry = customtkinter.CTkEntry(self.tabview.tab("Sign-in"),
                        placeholder_text="Enter your password",
                        font=("Consolas", 16),
                        show="*",
                        width=290,
                        height=40,
                        border_width=2,
                        corner_radius=10
                        )
        self.login_password_entry.place(x=50,y=180)
        
        self.login_submit_button = customtkinter.CTkButton(self.tabview.tab("Sign-in"), 
                        text='LOGIN',
                        font=customtkinter.CTkFont(size=15, weight="bold"), 
                        fg_color="#0065D9",
                        hover_color="#2AAAFA",  
                        width=120, 
                        height=42, 
                        corner_radius=10, 
                        command=self.submit_login
                        )
        self.login_submit_button.place(x=60, y=260)
        
        self.guest_button = customtkinter.CTkButton(self.tabview.tab("Sign-in"),
                        text='Guest View',
                        font=customtkinter.CTkFont(size=15, weight="bold"), 
                        fg_color="#D96C00",
                        hover_color="#FF8C00",
                        width=120, 
                        height=42, 
                        corner_radius=10, 
                        command=lambda: [widget.destroy() for widget in self.winfo_children()] + [GuestDashboard(self)]
                        )
        self.guest_button.place(x=210, y=260)   
        
        ########################################### Register Tab ###########################################
        
        self.register_username_label = customtkinter.CTkLabel(
                        self.tabview.tab("Register"),
                        text="Username",
                        font=("Copperplate", 16),
                        width=50,
                        height=25,
                        corner_radius=0
                        )
        self.register_username_label.place(x=13,y=20)

        self.register_username_entry = customtkinter.CTkEntry(
                        self.tabview.tab("Register"),
                        placeholder_text="Enter your PRN",
                        width=290,
                        height=35,
                        border_width=2,
                        corner_radius=10
                        )
        self.register_username_entry.place(x=113,y=20)

        self.register_password_label = customtkinter.CTkLabel(
                        self.tabview.tab("Register"),
                        text="Password",
                        font=("Copperplate", 16),
                        width=50,
                        height=25,
                        corner_radius=0
                        )
        self.register_password_label.place(x=13,y=60)
    
        self.register_password_entry = customtkinter.CTkEntry(
                        self.tabview.tab("Register"),
                        placeholder_text="Enter your password",
                        show="*",
                        width=290,
                        height=35,
                        border_width=2,
                        corner_radius=10
                        )
        self.register_password_entry.place(x=113,y=60)
        
        self.full_name_label = customtkinter.CTkLabel(
                        self.tabview.tab("Register"),
                        text="Full Name",
                        font=("Copperplate", 16),
                        width=50,
                        height=25,
                        corner_radius=0
                        )
        self.full_name_label.place(x=13,y=100)

        self.full_name_entry = customtkinter.CTkEntry(
                        self.tabview.tab("Register"),
                        placeholder_text="Enter your full name",
                        width=290,
                        height=35,
                        border_width=2,
                        corner_radius=10
                        )
        self.full_name_entry.place(x=113,y=100)
        
        self.email_label = customtkinter.CTkLabel(
                        self.tabview.tab("Register"),
                        text="Email ID",
                        font=("Copperplate", 16),
                        width=50,
                        height=25,
                        corner_radius=0
                        )
        self.email_label.place(x=13,y=140)

        self.email_entry = customtkinter.CTkEntry(
                        self.tabview.tab("Register"),
                        placeholder_text="Enter your email address",
                        width=290,
                        height=35,
                        border_width=2,
                        corner_radius=10
                        )
        self.email_entry.place(x=113,y=140)
        
        self.mobile_label = customtkinter.CTkLabel(
                        self.tabview.tab("Register"),
                        text="Mobile No.",
                        font=("Copperplate", 16),
                        width=50,
                        height=25,
                        corner_radius=0
                        )
        self.mobile_label.place(x=13,y=180)

        self.mobile_entry = customtkinter.CTkEntry(
                        self.tabview.tab("Register"),
                        placeholder_text="Enter your mobile number",
                        width=290,
                        height=35,
                        border_width=2,
                        corner_radius=10
                        )
        self.mobile_entry.place(x=113,y=180)
        
        self.year_label = customtkinter.CTkLabel(
                        self.tabview.tab("Register"),
                        text="Year",
                        font=("Copperplate", 16),
                        width=50,
                        height=25,
                        corner_radius=0
                        )
        self.year_label.place(x=13,y=220)
        
        self.year_optionmenu = customtkinter.CTkOptionMenu(
                                self.tabview.tab("Register"), 
                                values=["First Year", "Second Year", "Third Year", "Final Year"],
                                corner_radius=10
                                )
        self.year_optionmenu.place(x=113,y=220)   
        
        self.gender_label = customtkinter.CTkLabel(
                        self.tabview.tab("Register"),
                        text="Gender",
                        font=("Copperplate", 16),
                        width=50,
                        height=25,
                        corner_radius=0
                        )
        self.gender_label.place(x=13,y=260)
        
        self.gender_radio_var = customtkinter.StringVar(value="Male")
        
        self.gender_radio_button_1 = customtkinter.CTkRadioButton(
                                self.tabview.tab("Register"), 
                                text="Male", 
                                variable=self.gender_radio_var, 
                                value="Male"
                                )
        self.gender_radio_button_1.place(x=113,y=260)  
        
        self.gender_radio_button_2 = customtkinter.CTkRadioButton(
                                self.tabview.tab("Register"), 
                                text="Female", 
                                variable=self.gender_radio_var, 
                                value="Female"
                                )
        self.gender_radio_button_2.place(x=193,y=260)  
        
        self.role_label = customtkinter.CTkLabel(
                        self.tabview.tab("Register"),
                        text="Role",
                        font=("Copperplate", 16),
                        width=50,
                        height=25,
                        corner_radius=0
                        )
        self.role_label.place(x=13,y=300)
        
        self.role_radio_var = customtkinter.StringVar(value="USER")
        
        self.role_radio_button_1 = customtkinter.CTkRadioButton(
                                self.tabview.tab("Register"), 
                                text="Admin", 
                                variable=self.role_radio_var, 
                                value="ADMIN",
                                state="disabled"
                                )
        self.role_radio_button_1.place(x=113,y=300)  
        
        self.role_radio_button_2 = customtkinter.CTkRadioButton(
                                self.tabview.tab("Register"), 
                                text="User", 
                                variable=self.role_radio_var, 
                                value="USER"
                                )
        self.role_radio_button_2.place(x=193,y=300)  
        
        self.register_submit_button = customtkinter.CTkButton(
                        self.tabview.tab("Register"),
                        text='SUBMIT',
                        font=customtkinter.CTkFont(size=15, weight="bold"), 
                        fg_color="#0065D9",
                        hover_color="#2AAAFA", 
                        width=120, 
                        height=42, 
                        corner_radius=10, 
                        command=self.submit_register
                        )
        self.register_submit_button.place(x=150, y=340)
    
        self.footer_label = customtkinter.CTkLabel(
                               self,
                               text="© Department of Computer Engineering, Dr. Babasaheb Ambedkar Technological University, Lonere.",
                               text_color="white",
                               font=customtkinter.CTkFont(size=15),
                               bg_color="black",
                               width=int(self.screen_width * 0.8),
                               height=35,
                               corner_radius=0
                               )
        self.footer_label.place(x=0, y=1, relx=0, rely=1, relwidth=1.0, anchor="sw")  

    def change_appearance_mode(self):
        customtkinter.set_appearance_mode(self.switch_var.get())
    
    def submit_login(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()
        
        error_message = ""
        if not username:
            error_message += "Please enter a username.\n"
        if not password:
            error_message += "Please enter a password.\n"
        
        if error_message:
            messagebox.showerror("Error", error_message)
        else:
            try:
                query = "SELECT * FROM users WHERE username=%s AND password=%s"
                cursor.execute(query, (username, password))
                result = cursor.fetchone()
            except Exception as e:
                messagebox.showerror("Error", e)
                print("[x] Error: ", e)
            else:
                if result:
                    self.after_login(username)
                elif username == "test" and password == "test":
                    self.test_login()    
                else:
                    messagebox.showerror("Login Failed", "Invalid username or password!")
                    print("[x] Login Failed. Invalid username or password.")
    
    def submit_register(self):
        self.username = self.register_username_entry.get()
        self.password = self.register_password_entry.get()
        self.name = self.full_name_entry.get()
        self.email = self.email_entry.get()
        self.mobile = self.mobile_entry.get()
        self.year = self.year_optionmenu.get()
        self.gender = self.gender_radio_var.get()
        self.role = self.role_radio_var.get()
        
        error_message = ""
        if not self.username:
            error_message += "Please enter a username.\n"
        if not self.password:
            error_message += "Please enter a password.\n"
        if not self.name:
            error_message += "Please enter a name.\n"
        if not self.email:
            error_message += "Please enter an email.\n"
        if not self.mobile:
            error_message += "Please enter a mobile number.\n"
        if not self.year:
            error_message += "Please enter a year.\n"
        if not self.gender:
            error_message += "Please select a gender.\n"
        if not self.role:
            error_message += "Please select a role.\n"
        
        if error_message:
            messagebox.showerror("Error", error_message)
        else:
            if not re.match(r"^\d{13}$", self.username) or "30331245" not in self.username:
                messagebox.showerror("Error", "Please enter a valid username (13-digit PRN of Computer Department)")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
                messagebox.showerror("Error", "Please enter a valid email address")
            elif not re.match(r"^[0-9]{10}$", self.mobile):
                messagebox.showerror("Error", "Please enter a valid mobile number (10 digits)")
            else:
                try:
                    cursor.execute("SELECT * FROM users WHERE username = {};".format(self.username)) 
                    if cursor.fetchone() is not None:
                        messagebox.showerror("Error", "PRN already exists in the database.\nKindly login instead.")
                        return False
                    else:
                        cursor.execute("""INSERT INTO users(username, password, full_name, email, mobile, year, gender, role) VALUES ({}, "{}", "{}", "{}", {}, "{}", "{}", "{}");""".format(
                                self.username, 
                                self.password,
                                self.name, 
                                self.email, 
                                self.mobile, 
                                self.year, 
                                self.gender, 
                                self.role)
                                )
                        cnx.commit()  
                except ValueError as error:
                    raise ValueError("Error", str(error))  
                else:
                    if not False:
                        messagebox.showinfo("Registration Successful", f"Registration Successful!\n\nWelcome,{self.username}.\nKindly login to proceed further.")
                        print("Registration Successful. Username added: " + self.username)
                        
    def after_login(self, username):
        messagebox.showinfo("Login Successful", "Welcome, " + username)
        print("\n[*] Login Successful. Welcome, " + username)
        for widget in self.winfo_children():
            widget.destroy()
            
        cursor.execute("SELECT role FROM users WHERE username = {};".format(username))
        role = cursor.fetchone()[0]
        if role == "ADMIN":
            AdminDashboard(self)
        else:
            UserDashboard(self)
            
    # FUNCTION FOR QUICK LOGIN DURING TESTING, REMOVE LATER
    def test_login(self):
        messagebox.showinfo("Login Successful", "Welcome, TEST")
        print("\n[*] Login Successful. TEST LOGIN.")
        for widget in self.winfo_children():
            widget.destroy()

        AdminDashboard(self)
        # UserDashboard(self)  
        
if __name__ == "__main__":
    aem = AEM()
    aem.mainloop()