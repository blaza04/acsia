import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from WUW_Test_Main import WUWTest #from another py file
import subprocess
from tkinter import *      
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import threading
from datetime import datetime

class KPIMeas_GUI:
    def __init__(self):

        self.timenow=datetime.now()
        self.rundirectoryname="WUW_Recognition_Testrun_"+ self.timenow.strftime("%d_%m_%H_%M")
        self.rundirectory = ""
        self.txtfilepath = ""
        self.excelfilepath = ""

        self.window = tk.Tk()
        self.window.title("IPA Test Runner for WUW Recognition")
        self.window.geometry("550x320")

        self.excel_path = None
        #self.report_path = None
        self.report_name = "WUW_Recognition_Test_Report_IPA_.xlsx"
        self.report_whole = None
        self.audio_path = None
        self.logs_path = None
        self.ip = None
        self.tech = None
 
        self.audio_combobox = None
        self.excel_combobox = None
        self.report_combobox = None
        self.report_entry = None
        self.log_combobox = None
        self.ip_entry = None
        self.error_label = None
        self.test_status_label = None
        self.tech_option = None
        self.var = None

        self.testfinished = threading.Event()

        self.df = pd.DataFrame(columns = ["0", "1", "2", "3", "4","5"])

        self.args = None


        self.create_widgets()

    def create_widgets(self):

        frame = tk.Frame(self.window)
        frame.grid()

        #######################################################################################################################

        tech_label = tk.Label(self.window, text="Select Tech Stack:")
        tech_label.grid(row=0, column=0, sticky='w')

        tech_frame = tk.Frame(self.window)
        tech_frame.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        self.var = tk.StringVar(tech_frame, value = "Please selecet the Tech Stac here!")
        self.tech_option = tk.OptionMenu(tech_frame, self.var, "Cerence", "ACA")#,command=self.select_tech)
        self.tech_option.pack(side=tk.LEFT)


        #tech1 = tk.Radiobutton(tech_frame, text="Cerence", variable=self.tech, value = "Cerence")
        #tech1.pack(side=tk.LEFT,padx=5) 
        #tech2 = tk.Radiobutton(tech_frame, text="ACA", variable=self.tech, value = "ACA")
        #tech2.pack(side=tk.LEFT,padx=10) 

        #######################################################################################################################     

        ip_label = tk.Label(self.window, text="MCU IP Adress:")
        ip_label.grid(row=3, column=0, sticky="w")

        ip_frame = tk.Frame(self.window)
        ip_frame.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        self.ip_entry = tk.Entry(ip_frame, width=45)
        self.ip_entry.pack(side=tk.LEFT)
        self.ip_entry.insert(0,"169.254.")

       
        ######################################################################################################################
        
        audio_label = tk.Label(self.window, text="WUW Audio Utterances Path:")
        audio_label.grid(row=4, column=0, sticky="w")

        audio_frame = tk.Frame(self.window)
        audio_frame.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        self.audio_combobox = ttk.Combobox(audio_frame, width=45)
        self.audio_combobox.pack(side=tk.LEFT)

        audio_select_button = ttk.Button(audio_frame, text="Select", command=self.select_audio_path)
        audio_select_button.pack(side=tk.LEFT, padx=5)

        ######################################################################################################################
        
        excel_label = tk.Label(self.window, text="WUW List File:")
        excel_label.grid(row=5, column=0, sticky="w")

        excel_frame = tk.Frame(self.window)
        excel_frame.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        self.excel_combobox = ttk.Combobox(excel_frame, width=45)
        self.excel_combobox.pack(side=tk.LEFT)

        excel_select_button = ttk.Button(excel_frame, text="Select", command=self.select_excel_path)
        excel_select_button.pack(side=tk.LEFT,padx=5)

        #######################################################################################################################

        log_label = tk.Label(self.window, text="Log & Report Storage path:")
        log_label.grid(row=6, column=0, sticky="w")

        log_frame = tk.Frame(self.window)
        log_frame.grid(row=6, column=1, sticky="w", padx=5, pady=5)

        self.log_combobox = ttk.Combobox(log_frame, width=45)
        self.log_combobox.pack(side=tk.LEFT)

        log_select_button = ttk.Button(log_frame, text="Select", command=self.select_logs_path)
        log_select_button.pack(side=tk.LEFT,padx=5)


        #######################################################################################################################

        log_label = tk.Label(self.window, text="Report File Name:")
        log_label.grid(row=8, column=0, sticky="w")

        log_frame = tk.Frame(self.window)
        log_frame.grid(row=8, column=1, sticky="w", padx=5, pady=5)

        self.report_entry = tk.Entry(log_frame, width=45)
        self.report_entry.pack(side=tk.LEFT)
        self.report_entry.insert(0,f"{self.report_name}")

        #ip_confirm_button = ttk.Button(log_frame, text="Confirm", command=self.confirm_report_input)
        #ip_confirm_button.pack(side=tk.LEFT,padx=5)

        ########################################################################################################################
        
        language_label = tk.Label(self.window, text="Select Language:")
        language_label.grid(row=9, column=0, sticky='w')

        lang_frame = tk.Frame(self.window)
        lang_frame.grid(row=9, column=1, sticky="w", padx=5, pady=5)

        self.langvar = tk.StringVar(lang_frame, value = "Please select the language here!")
        self.lang_option = tk.OptionMenu(lang_frame, self.langvar, "de_de", "en_us","fr_ca","en_uk","es_mx")#,command=self.select_tech)
        self.lang_option.pack(side=tk.LEFT)



       
        ######################################################################################################################
    

        start_button = ttk.Button(self.window, text="Start Test", command=self.start_test)
        start_button.grid(row=10, column=1, sticky="w", padx=5)

        ########################################################################################################################
        
        open_logs_button = ttk.Button(self.window, text="Open Logs Folder", command=self.open_logs_folder)
        open_logs_button.grid(row=11, column=0, sticky="w", padx=5)

        ########################################################################################################################

        self.error_label = tk.Label(self.window, fg="red")
        self.error_label.grid(row=12, column=1, sticky="w", padx=5)

        ########################################################################################################################
        
        self.test_status_label = tk.Label(self.window, text="")
        self.test_status_label.grid(row=14, column=1, sticky="w", padx=5)

        ########################################################################################################################
        



    def select_audio_path(self):
        self.audio_path = filedialog.askdirectory()
        self.audio_combobox.set(self.audio_path)
        self.audio_path = self.audio_path.replace("/","\\")
        

    def select_excel_path(self):
        self.excel_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        self.excel_combobox.set(self.excel_path)
        self.excel_path = self.excel_path.replace("/","\\")

    def select_logs_path(self):
        self.logs_path = filedialog.askdirectory()
        self.log_combobox.set(self.logs_path)
        self.logs_path = self.logs_path.replace("/","\\")
        self.rundirectory=os.path.join(self.logs_path,self.rundirectoryname)
        os.mkdir(self.rundirectory)

    
    def start_test(self):

        self.ip = self.ip_entry.get()
        self.report_name = self.report_entry.get()
        self.tech = self.var.get()
        self.lang =self.langvar.get()
        self.report_whole = "\\" + self.report_name
        

        if self.audio_path and self.excel_path and self.logs_path and self.tech != "Please selecet the Tech Stac here!" and self.ip and self.report_name and self.lang:
            self.error_label.config(text="Starting the test...")
            permission = True
        else:
            self.error_label.config(text="Please select all the paths / input & output file \n/ IP adress before starting the test.")
            self.test_status_label.config(text="")
            permission = False

        if permission:
            self.test_status_label.config(text="Running tests...")
            self.run_Wuw_Test()



    def run_Wuw_Test(self):

        if self.tech == "Cerence":
            self.args = "com.bmwgroup.speech.core"
            print("Running KPI Test for Cerence...\n")
            obj_wuwtest = WUWTest(self.rundirectory, self.ip, self.excel_path, self.report_whole, self.audio_path,self.lang)
            obj_wuwtest.test_init()
            obj_wuwtest.WUWTest()
            print(f"Test Finished\n")
            self.error_label.config(text="KPI Measurement DONE")
            self.test_status_label.config(text="")

        if self.tech == "ACA":
            self.args = "com.bmwgroup.assistant.alexa"
            print("Running KPI Test for ACA...\n")
            obj_wuwtest = WUWTest(self.rundirectory, self.ip, self.excel_path, self.report_whole, self.audio_path,self.lang)
            obj_wuwtest.test_init()
            obj_wuwtest.WUWTest()
            print(f"Test Finished\n")
            self.error_label.config(text="KPI Measurement DONE")
            self.test_status_label.config(text="")

    

      
    def open_logs_folder(self):
        logs_folder_path = self.logs_path # Replace with the actual path to your logs folder
        subprocess.Popen(f'explorer "{logs_folder_path}"')






    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    kpirunner = KPIMeas_GUI()
    kpirunner.run()
