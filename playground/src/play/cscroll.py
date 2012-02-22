from Tkinter import *

class ScrolledCanvas:
    def __init__(self, master, width=500, height=350):
        Label(master, text="This window displays a canvas widget "
            "that can be scrolled either using the scrollbars or "
            "by dragging with button 3 in the canvas. If you "
            "click button 1 on one of the rectangles, its indices "
            "will be printed on stdout.",
            wraplength="4i", justify=LEFT).pack(side=TOP)
        self.control=Frame(master)
        self.control.pack(side=BOTTOM, fill=X, padx=2)
        Button(self.control, text='Quit', command=master.quit).pack()
        self.grid = Frame(master, bd=2, bg="red")
        self.canvas = Canvas(master, relief=SUNKEN, borderwidth=2, 
                             scrollregion=('-11c', '-11c', '50c', '20c')) 
        self.hscroll = Scrollbar(master, orient=HORIZONTAL, 
                                 command=self.canvas.xview) 
        self.vscroll = Scrollbar(master, command=self.canvas.yview) 
        self.canvas.configure(xscrollcommand=self.hscroll.set,
                              yscrollcommand=self.vscroll.set) 
        self.grid.pack(expand=YES, fill=BOTH, padx=1, pady=1)
        self.grid.rowconfigure(0, weight=1, minsize=0)
        self.grid.columnconfigure(0, weight=1, minsize=0)
        self.canvas.grid_propagate(False)
        self.canvas.grid(padx=1, in_=self.grid, pady=1, row=0,
                         column=0, rowspan=1, columnspan=1, sticky='news')
        self.vscroll.grid(padx=1, in_=self.grid, pady=1, row=0,
                          column=1, rowspan=1, columnspan=1, sticky='news')
        self.hscroll.grid(padx=1, in_=self.grid, pady=1, row=1,
                          column=0, rowspan=1, columnspan=1, sticky='news')
        self.oldFill = None
#        self.canvas = self.fillCanvas(self.canvas)
        self.canvas = self.fillCanvas2(self.canvas)
        
        self.canvas.tag_bind('rect', '<Any-Enter>', self.scrollEnter)
        self.canvas.tag_bind('rect', '<Any-Leave>', self.scrollLeave)
        self.canvas.bind_all('<1>', self.scrollButton)
        self.canvas.bind('<3>',
                         lambda e, s=self: s.canvas.scan_mark(e.x, e.y))
        self.canvas.bind('<B3-Motion>',
                         lambda e, s=self: s.canvas.scan_dragto(e.x, e.y))
        
    def scrollEnter(self, event):
        id = self.canvas.find_withtag(CURRENT)[0]
        if 'text' in self.canvas.gettags(CURRENT):
            id = id-1
        self.canvas.itemconfigure(id, fill='SeaGreen1')

    def scrollLeave(self, event):
        id = self.canvas.find_withtag(CURRENT)[0]
        if 'text' in self.canvas.gettags(CURRENT):
            id = id-1
        self.canvas.itemconfigure(id, fill=self.canvas['background'])
        
    def scrollButton(self, event):
        ids = self.canvas.find_withtag(CURRENT)
        if ids:
            id = ids[0]
            if not 'text' in self.canvas.gettags(CURRENT):
                id = id+1
            print 'You clicked on %s' % \
                self.canvas.itemcget(id, 'text')
                
    def fillCanvas(self, theCanvas):
        bg = theCanvas['background']
        for i in range(20):
             x = -10 + 3*i
             y = -10
             for j in range(10):
                 theCanvas.create_rectangle('%dc'%x, '%dc'%y,
                                              '%dc'%(x+2), '%dc'%(y+2), outline='black',
                                              fill=bg, tags='rect')
                 theCanvas.create_text('%dc'%(x+1), '%dc'%(y+1),
                                         text='%d,%d'%(i,j), anchor=CENTER,
                                         tags=('text', 'rect'))
                 y = y + 3
        return theCanvas
    
    def fillCanvas2(self, theCanvas):
        for i in range(20):
            frame = Frame(theCanvas)
            Label(frame, text="left %s" % i).pack(side="left")
            Label(frame, text="right %s" % i).pack(side="right")
            frame.pack()
        return theCanvas
    
                    

if __name__ == '__main__':
    root = Tk()
    root.option_add('*Font', 'Verdana 10')
    root.title('Scrolled Canvas')
    scroll = ScrolledCanvas(root)
    root.mainloop()
