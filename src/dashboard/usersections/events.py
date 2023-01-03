import customtkinter
import csv
import mysql.connector
import openpyxl
import time


from tkinter import ttk, filedialog
from ...database.db_connect import cursor, cnx

customtkinter.set_appearance_mode("light") 
customtkinter.set_default_color_theme("dark-blue")

class ViewEventSection:
    def __init__(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        
        completed_events_button = customtkinter.CTkButton(
                        frame,
                        text='Show Completed',
                        font=customtkinter.CTkFont(size=18), 
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        width=180, 
                        height=80, 
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command= lambda: CompletedEvents(frame)
                        )
        completed_events_button.grid(row=0, column=0, sticky="s", padx=35, pady=5)
        
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
                        command= lambda: ExportData(frame)
                        )
        export_data_button.grid(row=1, column=0, sticky="s", padx=35, pady=5)
        
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
        treeview["columns"] = ("sr", "event_name", "event_description", "event_date", "event_time", "event_venue")
        treeview["show"] = "headings"
        
        treeview.column("sr", width=50, anchor="center")
        treeview.column("event_name", width=200, anchor="center")
        treeview.column("event_description", width=350, anchor="center")
        treeview.column("event_date", width=130, anchor="center")
        treeview.column("event_time", width=130, anchor="center")
        treeview.column("event_venue", width=200, anchor="center")
        
        treeview.heading("sr", text="Sr. No")
        treeview.heading("event_name", text="Title")
        treeview.heading("event_description", text="Description")
        treeview.heading("event_date", text="Date")
        treeview.heading("event_time", text="Time")
        treeview.heading("event_venue", text="Location")

        treeview.grid(row=0, column=2, rowspan=6, sticky="nsew", padx=10, pady=10)
        
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
                    
class CompletedEvents:
    def __init__(self, frame):
        self.the_frame = frame
        for widget in frame.winfo_children():
            widget.destroy()
        self.completed_events(frame)
    
    def completed_events(self, frame):
        
        go_back_button = customtkinter.CTkButton(
                        frame,
                        text="Go Back",
                        font=customtkinter.CTkFont(size=16),
                        fg_color="Green",
                        hover_color="#2AAAFA",
                        border_width=3,
                        border_color=("#EDF6FA", "#1B1B24"),
                        corner_radius=15,
                        command=lambda: ViewEventSection(frame)
                        )
        go_back_button.grid(row=1, column=1, sticky="n", padx=35, pady=15)
        
        event_history_label = customtkinter.CTkLabel(
                        frame,
                        text='Completed Events',
                        font=customtkinter.CTkFont(size=24, weight="bold"),
                        )
        event_history_label.grid(row=1, column=2, columnspan=2, sticky="n", padx=35, pady=15)
        
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
                        command=self.export_data
                        )
        export_data_button.grid(row=3, column=1, sticky="n", padx=35, pady=5)
        
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
        
        self.treeview = ttk.Treeview(frame)
        self.treeview["columns"] = ("sr", "event_name", "event_description", "event_date", "event_time", "event_venue")
        self.treeview["show"] = "headings"
        
        self.treeview.column("sr", width=50, anchor="center")
        self.treeview.column("event_name", width=200, anchor="center")
        self.treeview.column("event_description", width=300, anchor="center")
        self.treeview.column("event_date", width=130, anchor="center")
        self.treeview.column("event_time", width=130, anchor="center")
        self.treeview.column("event_venue", width=200, anchor="center")
        
        self.treeview.heading("sr", text="Sr. No")
        self.treeview.heading("event_name", text="Title")
        self.treeview.heading("event_description", text="Description")
        self.treeview.heading("event_date", text="Date")
        self.treeview.heading("event_time", text="Time")
        self.treeview.heading("event_venue", text="Location")

        self.treeview.grid(row=2, column=2, rowspan=7, sticky="nsew", padx=10, pady=10)
        
        query = "SELECT event_name, event_description, event_date, event_time, event_venue FROM completed_events;"
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
                for row in self.treeview.get_children():
                    self.treeview.delete(row)
                i=0
                for row in results:
                    i=i+1
                    self.treeview.insert("", "end", text="", values=(i, row[0], row[1], row[2], row[3], row[4]))
    
    def export_data(self):
        self.dialogue_window = customtkinter.CTkToplevel(fg_color=("#EDF6FA", "#1B1B24"))
        self.dialogue_window.geometry("500x400")
        self.dialogue_window.title("Export Data")
        self.dialogue_window.resizable(False, False)
        
        question_label = customtkinter.CTkLabel(
                        self.dialogue_window,
                        text="Select the format in which you want to export the data.",
                        font=customtkinter.CTkFont(size=16),
                        )
        question_label.place(x=250, y=80, anchor="center")
        
        csv_button = customtkinter.CTkButton(
                        self.dialogue_window,
                        text=".CSV (Comma Separated Values)",
                        width=200,
                        height=60,
                        font=customtkinter.CTkFont(size=16),
                        fg_color="#0065D9",
                        hover_color="#19941B", 
                        border_width=2,
                        border_color=("#1B1B24","#EDF6FA"),
                        corner_radius=15,
                        command=self.export_data_csv
                        )
        csv_button.place(x=250, y=160, anchor="center")
        
        xlsx_button = customtkinter.CTkButton(
                        self.dialogue_window,
                        text=".XLSX (Excel Spreadsheet)",
                        width=200,
                        height=60,
                        font=customtkinter.CTkFont(size=16),
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        border_width=2,
                        border_color=("#1B1B24","#EDF6FA"),
                        corner_radius=15,
                        command=self.export_data_xlsx
                        )
        xlsx_button.place(x=250, y=240, anchor="center")   
    
    def export_data_csv(self):
        self.dialogue_window.destroy()
        filepath = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv'), ('All files', '*')]) 
        try:   
            cursor.execute("""SELECT event_name, event_description, event_date, event_time, event_venue FROM completed_events;""")
            data = cursor.fetchall()
        except Exception as error:
            raise Exception("Error", error)  
        else:
            if filepath:
                with open(filepath, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Sr. No.", "Event Name", "Event Description", "Event Date", "Event Time", "Event Venue"])
                    i = 0
                    for row in data:
                        i = i + 1
                        data = [i, row[0], row[1], row[2], row[3], row[4]]
                        writer.writerow(data)      
        finally:        
            CompletedEvents(self.the_frame)  
            
    def export_data_xlsx(self):
        self.dialogue_window.destroy()
        filepath = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[('Excel files', '*.xlsx'), ('All files', '*')])
        try:
            cursor.execute("""SELECT event_name, event_description, event_date, event_time, event_venue FROM completed_events;""")
            data = cursor.fetchall()
        except Exception as error:
            raise Exception("Error", error)
        else:
            if filepath:
                workbook = openpyxl.Workbook()
                sheet = workbook.active
                sheet.append(["Sr. No.", "Event Name", "Event Description", "Event Date", "Event Time", "Event Venue"])
                i = 0
                for row in data:
                    i= i + 1
                    newrow = [i, row[0], row[1], row[2], row[3], row[4]]
                    sheet.append(newrow)
                workbook.save(filepath)
        finally:        
            CompletedEvents(self.the_frame)

class ExportData:
    def __init__(self, frame):
        self.the_frame = frame
        self.dialogue_window = customtkinter.CTkToplevel(fg_color=("#EDF6FA", "#1B1B24"))
        self.dialogue_window.geometry("500x400")
        self.dialogue_window.title("Export Data")
        self.dialogue_window.resizable(False, False)
        
        question_label = customtkinter.CTkLabel(
                        self.dialogue_window,
                        text="Select the format in which you want to export the data.",
                        font=customtkinter.CTkFont(size=16),
                        )
        question_label.place(x=250, y=80, anchor="center")
        
        csv_button = customtkinter.CTkButton(
                        self.dialogue_window,
                        text=".CSV (Comma Separated Values)",
                        width=200,
                        height=60,
                        font=customtkinter.CTkFont(size=16),
                        fg_color="#0065D9",
                        hover_color="#19941B", 
                        border_width=2,
                        border_color=("#1B1B24","#EDF6FA"),
                        corner_radius=15,
                        command=self.export_data_csv
                        )
        csv_button.place(x=250, y=160, anchor="center")
        
        xlsx_button = customtkinter.CTkButton(
                        self.dialogue_window,
                        text=".XLSX (Excel Spreadsheet)",
                        width=200,
                        height=60,
                        font=customtkinter.CTkFont(size=16),
                        fg_color="#0065D9",
                        hover_color="#19941B",  
                        border_width=2,
                        border_color=("#1B1B24","#EDF6FA"),
                        corner_radius=15,
                        command=self.export_data_xlsx
                        )
        xlsx_button.place(x=250, y=240, anchor="center")   
    
    def export_data_csv(self):
        self.dialogue_window.destroy()
        filepath = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv'), ('All files', '*')]) 
        try:   
            cursor.execute("""SELECT event_name, event_description, event_date, event_time, event_venue FROM events;""")
            data = cursor.fetchall()
        except Exception as error:
            raise Exception("Error", error)  
        else:
            if filepath:
                with open(filepath, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Sr. No.", "Event Name", "Event Description", "Event Date", "Event Time", "Event Venue"])
                    i = 0
                    for row in data:
                        i = i + 1
                        data = [i, row[0], row[1], row[2], row[3], row[4]]
                        writer.writerow(data)      
        finally:        
            ViewEventSection(self.the_frame)  
            
    def export_data_xlsx(self):
        self.dialogue_window.destroy()
        filepath = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[('Excel files', '*.xlsx'), ('All files', '*')])
        try:
            cursor.execute("""SELECT event_name, event_description, event_date, event_time, event_venue FROM events;""")
            data = cursor.fetchall()
        except Exception as error:
            raise Exception("Error", error)
        else:
            if filepath:
                workbook = openpyxl.Workbook()
                sheet = workbook.active
                sheet.append(["Sr. No.", "Event Name", "Event Description", "Event Date", "Event Time", "Event Venue"])
                i = 0
                for row in data:
                    i= i + 1
                    newrow = [i, row[0], row[1], row[2], row[3], row[4]]
                    sheet.append(newrow)
                workbook.save(filepath)
        finally:        
            ViewEventSection(self.the_frame)  