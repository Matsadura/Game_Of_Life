""" Main Window Class """
import tkinter
import customtkinter


class MainWindow(customtkinter.CTk):
    """ Main Window Class """
    def __init__(self, config=None):
        """ Intatianize Main Window """
        super().__init__()
        self.title('John Conway\'s Game Of Life')
        self.geometry('720x480')

        # TMP TEXT
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.textbox = customtkinter.CTkTextbox(master=self, width=400, corner_radius=0)
        self.textbox.grid(row=0, column=0, sticky="nsew")
        self.textbox.insert("0.0", "1 - Always create a FEATURE Branch (A temporary branch for a specific feature) from the latest \"dev\" branch\nAVOID working on big feature in one branch to always have the latest changes from other branches\n2 - After you finish implement the feature and it is MERGE ready, create a PULL REQUEST to the DEV branch and STOP WORKING ON THAT BRANCH IMMEDIATLY\n3 - Once the pull request has been approved and merged the feature branch MUST BE DELETED\n4 - Always CREATE a new feature branch and NEVER work on same branch twice\n5 - AVOID multiple people working in same branch to avoid conflicts\n6 - Read and reread the above no excuses please\n")
