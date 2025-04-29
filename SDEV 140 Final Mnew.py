import tkinter as tk

class SyllableCountingTextEditor():

    def __init__(self):

        window_title = "MSCTE (Tkinter)"
        initial_width = 500
        initial_height = 300
        primaryColor = "#333333" # Dark grey background
        textColor = "#FFFFFF"     # White text

        self.root = tk.Tk()
        self.root.title(window_title)
        self.root.geometry(f"{initial_width}x{initial_height}")
        self.root.config(background=primaryColor)

        text_area = tk.Text(self.root,
                    background=primaryColor,
                    foreground=textColor,
                    wrap='word',           
                    borderwidth=0,         
                    highlightthickness=0,  
                    relief=tk.FLAT,        
                    padx=0,                
                    pady=0)      

        text_area.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)


app = SyllableCountingTextEditor()
app.root.mainloop()