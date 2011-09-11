from Tkinter import * 

class ScrolledCanvas(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        #self.pack(expand=YES, fill=BOTH)                  
        self.pack()
        canv = Canvas(self, bd=2, bg="blue")
        canv.config(width=300, height=200)                
        canv.config(scrollregion=(0,0,300, 1000))         

        sbar = Scrollbar(self)
        sbar.config(command=canv.yview)                   
        canv.config(yscrollcommand=sbar.set)              
        sbar.pack(side=RIGHT, fill=Y)
        canv.pack(side=LEFT, expand=YES, fill=BOTH)       
        
        
        for i in range(10):
#            frame = Frame(canv, bd=1, bg="black")
#            label = Label(frame, text="sdf %s" % i)
#            label.pack(side=LEFT, expand=YES, fill=BOTH)
#            frame.pack(expand=YES, fill=BOTH)
#             canv.create_text(150, 50+(i*100), text='spam'+str(i))
            label = Label(canv, text="sdf %s" % i)
            label.pack()
        self.canvas = canv

if __name__ == '__main__': ScrolledCanvas().mainloop()
