import customtkinter

from tkinter import ttk
customtkinter.set_appearance_mode("light") 
customtkinter.set_default_color_theme("dark-blue")

class ComSection:
    def __init__(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
    
        dashboard_label1 = customtkinter.CTkLabel(
                            frame, 
                            text="ACES Committee 2022-23", 
                            font=customtkinter.CTkFont(size=30, weight="bold")
                            )
        dashboard_label1.place(relx=0.5, rely=0.1, anchor="n")
        
        style = ttk.Style()    
        style.theme_use("default")  
        style.configure("Treeview",
                        font=customtkinter.CTkFont(size=15),
                        background="#2A2D2E",
                        foreground="#EDF6FA",
                        rowheight=35,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=3)
        style.map('Treeview', background=[('selected', '#22559b')])
    
        style.configure("Treeview.Heading",
                        font=customtkinter.CTkFont(size=18, weight="bold"),
                        background="#3D3D3D",
                        foreground="#EDF6FA",
                        relief="flat")
        style.map("Treeview.Heading", background=[('active', '#0065D9')])
        
        treeview = ttk.Treeview(frame, columns=("name", "position"))
        treeview["show"] = "headings"
        
        treeview.column("name", width=400, anchor="center")
        treeview.column("position", width=400, anchor="center")

        treeview.heading("name", text="Name")
        treeview.heading("position", text="Position")


        treeview.place(relx=0.5, rely=0.25, anchor="n")
        
        treeview.insert("", "end", text="", values=("Aditya Navgare", "President"))
        treeview.insert("", "end", text="", values=("Aishwarya Rudrawar", "Vice-President"))
        treeview.insert("", "end", text="", values=("Shadab Shaikh", "Treasurer"))
        treeview.insert("", "end", text="", values=("Tushar Patil, Bhargavi Deshmukh", "Cultural Secretary"))
        treeview.insert("", "end", text="", values=("Yoesh Deolalkar, Ram Agrawal", "Technical Secretary"))
        treeview.insert("", "end", text="", values=("Rushikesh Thakare, Nupur Sawant", "Sport Secretary"))
    
    