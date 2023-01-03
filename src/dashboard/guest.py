import customtkinter
import mysql.connector
import time

from tkinter import ttk
from ..database.db_connect import cursor

customtkinter.set_appearance_mode("light") 
customtkinter.set_default_color_theme("dark-blue")

class GuestDashboard:
    def __init__(self, window):
        window.iconify()
        dialogue_window = customtkinter.CTkToplevel(fg_color=("#EDF6FA", "#1B1B24"))
        dialogue_window.geometry("950x400")
        dialogue_window.title("Guest View | AEM")
        dialogue_window.resizable(False, False)
        dialogue_window.protocol("WM_DELETE_WINDOW", self.on_close(window))
            
        _label = customtkinter.CTkLabel(
                            dialogue_window,
                            text="Upcoming Events",
                            font=customtkinter.CTkFont(size=20, weight="bold"),
                            )
        _label.place(relx=0.5, rely=0.1, anchor="n")
        
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
        
        treeview = ttk.Treeview(dialogue_window )
        treeview["columns"] = ("sr", "event_name", "event_description", "event_date", "event_time", "event_venue")
        treeview["show"] = "headings"
        
        treeview.column("sr", width=50, anchor="center")
        treeview.column("event_name", width=200, anchor="center")
        treeview.column("event_description", width=350, anchor="center")
        treeview.column("event_date", width=80, anchor="center")
        treeview.column("event_time", width=80, anchor="center")
        treeview.column("event_venue", width=150, anchor="center")
        
        treeview.heading("sr", text="Sr. No")
        treeview.heading("event_name", text="Title")
        treeview.heading("event_description", text="Description")
        treeview.heading("event_date", text="Date")
        treeview.heading("event_time", text="Time")
        treeview.heading("event_venue", text="Location")

        treeview.place(relx=0.5, rely=0.3, anchor="n")
        
        query = "SELECT event_name, event_description, event_date, event_time, event_venue FROM events;"
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
                    treeview.insert("", "end", text="", values=(i, row[0], row[1], row[2], row[3], row[4]))
            
    def on_close(self, window):
        window.deiconify()






