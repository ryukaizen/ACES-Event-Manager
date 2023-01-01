import customtkinter
import mysql.connector
import re
import time

from tkinter import ttk, messagebox
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
                        height=80, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command= lambda: RegisterUser(frame)
                        )
        register_user_button.grid(row=1, column=1, sticky="n", padx=35, pady=5)
        
        update_details_button = customtkinter.CTkButton(
                        frame,
                        text='Update Details',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        width=180, 
                        height=80, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        # command= lambda: MarkCompleted(frame, treeview)
                        )
        update_details_button.grid(row=2, column=1, sticky="n", padx=35, pady=5)
        
        remove_user_button = customtkinter.CTkButton(
                        frame,
                        text='Remove User',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#FF0000", 
                        width=180, 
                        height=80, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        # command= lambda: UpdateEvent(frame, treeview)
                        )
        remove_user_button.grid(row=3, column=1, sticky="n", padx=35, pady=5)
        
        export_data_button = customtkinter.CTkButton(
                        frame,
                        text='Export Data',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        width=180, 
                        height=80, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        # command= lambda: ExportData(frame)
                        )
        export_data_button.grid(row=4, column=1, sticky="s", padx=35, pady=5)
        
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
        treeview["columns"] = ("sr", "username", "full_name", "email", "mobile", "year", "gender", "role")
        treeview["show"] = "headings"
        
        treeview.column("sr", width=50, anchor="center")
        treeview.column("username", width=150, anchor="center")
        treeview.column("full_name", width=200, anchor="center")
        treeview.column("email", width=250, anchor="center")
        treeview.column("mobile", width=150, anchor="center")
        treeview.column("year", width=100, anchor="center")
        treeview.column("gender", width=100, anchor="center")
        treeview.column("role", width=80, anchor="center")
        
        treeview.heading("sr", text="Sr. No")
        treeview.heading("username", text="PRN")
        treeview.heading("full_name", text="Name")
        treeview.heading("email", text="Email")
        treeview.heading("mobile", text="Mobile")
        treeview.heading("year", text="Year")
        treeview.heading("gender", text="Gender")
        treeview.heading("role", text="Role")
        
        treeview.grid(row=1, column=2, rowspan=6, sticky="nsew", padx=10, pady=10)
        
        query = "SELECT username, full_name, email, mobile, year, gender, role FROM users"
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
                    treeview.insert("", "end", text="", values=(i, row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

class RegisterUser:
    def __init__(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        self.the_frame = frame
        self.new_user(frame)
    
    def new_user(self, frame):
        
        go_back_button = customtkinter.CTkButton(
                        frame,
                        text="Go Back",
                        font=customtkinter.CTkFont(size=16),
                        fg_color="Green",
                        hover_color="#2AAAFA",
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command=lambda: UsersSection(frame)
                        )
        go_back_button.place(relx=0.1, rely=0.02, anchor="n") 
        
        new_user_label = customtkinter.CTkLabel(
                        frame,
                        text='Register New User',
                        font=customtkinter.CTkFont(size=26, weight="bold"),
                        )
        new_user_label.place(relx=0.5, rely=0.02, anchor="n")  
        
        register_username_label = customtkinter.CTkLabel(
                        frame,
                        text="Username",
                        font=customtkinter.CTkFont(size=20),
                        width=50,
                        height=25,
                        corner_radius=0
                        )
        register_username_label.place(relx=0.1, rely=0.15, anchor="n")

        self.register_username_entry = customtkinter.CTkEntry(
                        frame,
                        placeholder_text="PRN (13 digits)",
                        width=290,
                        height=35,
                        font=customtkinter.CTkFont(size=18),
                        border_width=3,
                        border_color=("#1B1B24", "#EDF6FA"),
                        corner_radius=10
                        )
        self.register_username_entry.place(relx=0.17, rely=0.21, anchor="n")

        register_password_label = customtkinter.CTkLabel(
                        frame,
                        text="Password",
                        font=customtkinter.CTkFont(size=20),
                        width=50,
                        height=25,
                        corner_radius=0
                        )
        register_password_label.place(relx=0.1, rely=0.35, anchor="n")
    
        self.register_password_entry = customtkinter.CTkEntry(
                        frame,
                        placeholder_text="Password",
                        show="*",
                        width=290,
                        height=35,
                        font=customtkinter.CTkFont(size=18),
                        border_width=3,
                        border_color=("#1B1B24", "#EDF6FA"),
                        corner_radius=10
                        )
        self.register_password_entry.place(relx=0.17, rely=0.41, anchor="n")
        
        full_name_label = customtkinter.CTkLabel(
                        frame,
                        text="Full Name",
                        font=customtkinter.CTkFont(size=20),
                        width=50,
                        height=25,
                        corner_radius=0
                        )
        full_name_label.place(relx=0.1, rely=0.55, anchor="n")

        self.full_name_entry = customtkinter.CTkEntry(
                        frame,
                        placeholder_text="Full name",
                        width=290,
                        height=35,
                        font=customtkinter.CTkFont(size=18),
                        border_width=3,
                        border_color=("#1B1B24", "#EDF6FA"),
                        corner_radius=10
                        )
        self.full_name_entry.place(relx=0.17, rely=0.61, anchor="n")
        
        email_label = customtkinter.CTkLabel(
                        frame,
                        text="Email ID",
                        font=customtkinter.CTkFont(size=20),
                        width=50,
                        height=25,
                        corner_radius=0
                        )
        email_label.place(relx=0.4, rely=0.15, anchor="n")

        self.email_entry = customtkinter.CTkEntry(
                        frame,
                        placeholder_text="Email ID",
                        width=290,
                        height=35,
                        font=customtkinter.CTkFont(size=18),
                        border_width=3,
                        border_color=("#1B1B24", "#EDF6FA"),
                        corner_radius=10
                        )
        self.email_entry.place(relx=0.48, rely=0.21, anchor="n")
        
        mobile_label = customtkinter.CTkLabel(
                        frame,
                        text="Mobile No.",
                        font=customtkinter.CTkFont(size=20),
                        width=50,
                        height=25,
                        corner_radius=0
                        )
        mobile_label.place(relx=0.41, rely=0.35, anchor="n")

        self.mobile_entry = customtkinter.CTkEntry(
                        frame,
                        placeholder_text="Mobile No.",
                        width=290,
                        height=35,
                        font=customtkinter.CTkFont(size=18),
                        border_width=3,
                        border_color=("#1B1B24", "#EDF6FA"),
                        corner_radius=10
                        )
        self.mobile_entry.place(relx=0.48, rely=0.41, anchor="n")
        
        year_label = customtkinter.CTkLabel(
                        frame,
                        text="Year",
                        font=customtkinter.CTkFont(size=20),
                        width=50,
                        height=25,
                        corner_radius=0
                        )
        year_label.place(relx=0.39, rely=0.55, anchor="n")
        
        self.year_optionmenu = customtkinter.CTkOptionMenu(
                                frame, 
                                width=200,
                                height=40,
                                font=customtkinter.CTkFont(size=18),
                                dropdown_font=customtkinter.CTkFont(size=18),
                                values=["First Year", "Second Year", "Third Year", "Final Year"],
                                corner_radius=10
                                )
        self.year_optionmenu.place(relx=0.45, rely=0.61, anchor="n")
        
        gender_label = customtkinter.CTkLabel(
                        frame,
                        text="Gender",
                        font=customtkinter.CTkFont(size=20),
                        width=50,
                        height=25,
                        corner_radius=0
                        )
        gender_label.place(relx=0.7, rely=0.15, anchor="n")
        
        self.gender_radio_var = customtkinter.StringVar(value="Male")
        
        self.gender_radio_button_1 = customtkinter.CTkRadioButton(
                                frame, 
                                text="Male", 
                                font=customtkinter.CTkFont(size=18),
                                variable=self.gender_radio_var, 
                                value="Male"
                                )
        self.gender_radio_button_1.place(relx=0.72, rely=0.21, anchor="n")
        
        self.gender_radio_button_2 = customtkinter.CTkRadioButton(
                                frame, 
                                text="Female", 
                                font=customtkinter.CTkFont(size=18),
                                variable=self.gender_radio_var, 
                                value="Female"
                                )
        self.gender_radio_button_2.place(relx=0.79, rely=0.21, anchor="n")
        
        role_label = customtkinter.CTkLabel(
                        frame,
                        text="Role",
                        font=customtkinter.CTkFont(size=20),
                        width=50,
                        height=25,
                        corner_radius=0
                        )
        role_label.place(relx=0.69, rely=0.35, anchor="n")
        
        self.role_radio_var = customtkinter.StringVar(value="USER")
        
        self.role_radio_button_1 = customtkinter.CTkRadioButton(
                                frame, 
                                text="Admin", 
                                font=customtkinter.CTkFont(size=18),
                                variable=self.role_radio_var, 
                                value="ADMIN",
                                )
        self.role_radio_button_1.place(relx=0.72, rely=0.41, anchor="n")
        
        self.role_radio_button_2 = customtkinter.CTkRadioButton(
                                frame, 
                                text="User", 
                                font=customtkinter.CTkFont(size=18),
                                variable=self.role_radio_var, 
                                value="USER"
                                )
        self.role_radio_button_2.place(relx=0.79, rely=0.41, anchor="n")
        
        register_submit_button = customtkinter.CTkButton(
                        frame,
                        text="Register",
                        font=customtkinter.CTkFont(size=20, weight="bold"), 
                        fg_color="#D96C00",
                        hover_color="#FF8C00",  
                        width=180, 
                        height=65, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command=self.register_new_user
                        )
        register_submit_button.place(relx=0.74, rely=0.61, anchor="n")

    def register_new_user(self):
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
                except Exception as error:
                    raise Exception("Error", str(error))  
                else:
                    if not False:
                        messagebox.showinfo("Registration Successful", f"Registration Successful!\n\nUsername added: {self.username}")
                        print("Registration Successful. Username added: " + self.username)
                        UsersSection(self.the_frame)
