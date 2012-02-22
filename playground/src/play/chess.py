import Tkinter as tk
import random

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        size = 40
        menubar = tk.Menu(self)
        menubar.add_cascade(label="Game")
        menubar.add_cascade(label="Options")
        menubar.add_cascade(label="Help")
        chessboard = tk.Canvas(width=8*size, height=8*size, borderwidth = 0,
                               highlightthickness=0)
        statusbar = tk.Label(self, borderwidth=1, relief="sunken")
        right_panel = tk.Frame(self, borderwidth = 1, relief="sunken")
        scrollbar = tk.Scrollbar(orient="vertical", borderwidth=1)
        # N.B. height is irrelevant; it will be as high as it needs to be
        text = tk.Text(background="white",width=40, height=1, borderwidth=0, yscrollcommand=scrollbar.set)
        scrollbar.config(command=text.yview)

        toolbar = tk.Frame(self)
        for i in range(10):
            b = tk.Button(self, text="B%s" % i, borderwidth=1)
            b.pack(in_=toolbar, side="left")

        self.config(menu=menubar)
        statusbar.pack(side="bottom", fill="x")
        chessboard.pack(side="left", fill="both", expand=False)
        toolbar.grid(in_=right_panel, row=0, column=0, sticky="ew")
        right_panel.pack(side="right", fill="both", expand=True)
        text.grid(in_=right_panel, row=1, column=0, sticky="nsew")
        scrollbar.grid(in_=right_panel, row=1, column=1, sticky="ns")
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    app = App()
    app.mainloop()
