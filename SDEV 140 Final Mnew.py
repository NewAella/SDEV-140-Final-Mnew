
# This program is a very simple text editor, it reads and writes .txt files.
# It includes a file button containing three options, one for a new file, one for opening a file
# and lastly one to save the file (save as).
# Initially the program was going to include a syllable counter but due to personal life
# and poor time management, I cut that out and settled for a simple text editor.
# Additionally, I went with tkinter over Breezy because I felt tkinter gave me a lot more control
# over the display of the window that breezy was not providing sylistically.

import tkinter as tk
from tkinter import filedialog #need this for file operations

class TextEditor():

    def __init__(self):
        window_title = "MSCTE (Tkinter)" # the title of the parent window
        # the parent windows dimensions
        initial_width = 900 
        initial_height = 450

        self.primaryColor = "#333333" # Dark grey background
        self.textColor = "#FFFFFF"     # White text
        self.borderColor = "#666666" # light grey, used for the top bar

        # initializes the tk window
        self.root = tk.Tk()
        self.root.title(window_title) # it's title
        self.root.geometry(f"{initial_width}x{initial_height}") # the dimensions
        self.root.config(background=self.primaryColor) # and the color of the background.

        topBar = tk.Frame(self.root,
                          background=self.borderColor,
                          height=30)
        topBar.pack(side=tk.TOP, fill=tk.X)
        topBar.pack_propagate(False) # prevents buttons from changing the size
                                     # of the window.

        # sets the properties of the filebutton, and issues the command to
        # open a window that has options for opening a text document, saving it and creating a new one
        self.fileButton = tk.Button(topBar,
                                    text="File",
                                    command=self.open_file_menu,
                                    background=self.borderColor,
                                    foreground=self.textColor,
                                    activebackground=self.primaryColor,
                                    activeforeground=self.textColor,
                                    borderwidth=0,
                                    relief=tk.FLAT,
                                    padx=10, pady=5
                                    )
        self.fileButton.pack(side=tk.LEFT)

        # Establishes the area in which the user is able to input text and it's properties.
        self.text_area = tk.Text(self.root,
                    background=self.primaryColor,
                    foreground=self.textColor,
                    insertbackground=self.textColor,
                    borderwidth=0,
                    highlightthickness=1,
                    highlightbackground=self.borderColor,
                    highlightcolor=self.borderColor,
                    relief=tk.FLAT,
                    padx=30,
                    pady=20)

        self.text_area.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        self.file_menu_window = None # To keep track of the file menu window

    def open_file_menu(self):
        # If the file menu window already exists and is visible, bring it to the front
        if self.file_menu_window and self.file_menu_window.winfo_exists():
            self.file_menu_window.lift()
            self.file_menu_window.focus_set()
            return

        # Create a new Toplevel window (secondary window)
        self.file_menu_window = tk.Toplevel(self.root)
        self.file_menu_window.title("Options")
        self.file_menu_window.config(background=self.primaryColor)

        self.file_menu_window.transient(self.root) # ensures that the window will minimize when the parent
                                                   # window is minimized, and stays on top of the parent.

        # Positions it relative to the file button
        # Gets the position of the file button
        x = self.fileButton.winfo_rootx()
        y = self.fileButton.winfo_rooty() + self.fileButton.winfo_height() + 5 # sets it Below the button
        self.file_menu_window.geometry(f"+{x}+{y}")

        # Defines a set of options to be applied to every button with the options window.
        menu_button_options = {
            "background": self.primaryColor,
            "foreground": self.textColor,
            "activebackground": self.borderColor,
            "activeforeground": self.textColor,
            "borderwidth": 0,
            "relief": tk.FLAT,
            "anchor": "w",
            "padx": 10, "pady": 5
        }

        # Adds buttons to the file menu window
        tk.Button(self.file_menu_window, text="New", command=self.file_new, **menu_button_options).pack(fill=tk.X) # button for a new file
        tk.Button(self.file_menu_window, text="Open...", command=self.file_open, **menu_button_options).pack(fill=tk.X) # button to open a file
        tk.Button(self.file_menu_window, text="Save As...", command=self.file_save_as, **menu_button_options).pack(fill=tk.X) # button to save as a specific name/file

        # Ensures the window is drawn and its size is calculated before trying to focus
        self.file_menu_window.update_idletasks()
        self.file_menu_window.focus_set()

    # The following methods provide the functionallity for the buttons commands:
    # Deletes everything from line 1 to the end of the file.
    def file_new(self):
        self.text_area.delete('1.0', tk.END)
        # if the file menu window is open and is visible:
        if self.file_menu_window:
            self.file_menu_window.destroy() # closes the window
            self.file_menu_window = None    # resets the file menu window back to none.

    # Opens an "Open File" window.
    # the default and only file format is .txt
    def file_open(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt")]
        )
        # if the user cancels the window, the filepath will return empty.
        if not filepath:
            self.file_menu_window.destroy() # closes the file menu upon closing the open file window.
            return
        self.text_area.delete('1.0', tk.END) # clears the text area before loading the new file.
        try:
            # opens the selected file in read mode ("r")
            with open(filepath, "r") as f:
                self.text_area.insert('1.0', f.read()) # inserts the .txt file data starting from line
                                                       # 1 all the way to the end.
            self.root.title(f"MSCTE (Tkinter) - {filepath}") # sets the title of the parent window
                                                             # to include the name of the open file.
        except FileNotFoundError:
            # handles the case where the file, for whatever reason, cannot be found.
            print(f"Error: File not found at {filepath}")

    # Similar to the "Open File" window, this window instead is meant to save the file as a .txt file.
    def file_save_as(self): 
        # also asks the user to input a name for the new file.
        filepath = filedialog.asksaveasfilename(
            filetypes=[("Text Files", "*.txt")]
        )
        # if the user closes the window, it doesn't save.
        if not filepath:
            return
        try:
            # Saves the file and opens it in write mode simultaneously.
            with open(filepath, "w") as f:
                text_content = self.text_area.get('1.0', tk.END)
                f.write(text_content)
            self.root.title(f"MSCTE (Tkinter) - {filepath}") # Updates the parent window Title.
        except Exception as e:
            print(f"Error saving file: {e}")
        if self.file_menu_window and self.file_menu_window.winfo_exists():
            self.file_menu_window.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    editor = TextEditor()
    editor.run()

# Source: https://docs.python.org/3/library/tkinter.html - The Documentation on TKinter
# Helped me understand what parts of the window are changeable through tkinter,
# Also helped with understanding how to open and save files.
# Source 2: https://youtu.be/TuLxsvK4svQ?si=tCfOb_7HVb9zuphS - Bro Code tkinter course
# I love this guy, goes very in depth on how to use tkinter.