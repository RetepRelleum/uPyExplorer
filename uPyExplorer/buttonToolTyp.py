from tkinter import *

class ButtonToolTip(Button):
    def __init__(self, master=None, toolTip="", **kw):
        super().__init__(master=master,  **kw)
        self.toolTip=toolTip

        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.close)

    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.bbox("insert")
        x += self.winfo_rootx() + 40
        y += self.winfo_rooty() + 10
        # creates a toplevel window
        self.tw = Toplevel(self.master)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.toolTip, justify='left',
                       background='yellow', relief='solid', borderwidth=1,
                       font=("times", "8", "normal"))
        label.pack(ipadx=1)

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()