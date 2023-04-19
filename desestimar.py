try: 
    import tkinter as tk
except:
    print("error")

class Main:
    def __init__(self, parent):
        #parameters
        self.parent = parent

    


if __name__== "__main__":
    root = tk.Tk()
    ventana = Main(root)
    
    root.mainloop()

