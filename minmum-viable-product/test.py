from tkinter import *
import threading

class App(threading.Thread):

    def __init__(self, tk_root):
        self.root = tk_root
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        loop_active = True
        while loop_active:
            user_input = raw_input("Give me your command! Just type \"exit\" to close: ")
            if user_input == "exit":
                loop_active = False
                self.root.quit()
                self.root.update()
            else:
                label = Label(self.root, text=user_input)
                label.pack()

ROOT = Tk()
APP = App(ROOT)
LABEL = Label(ROOT, text="Hello, world!")
LABEL.pack()
ROOT.mainloop()
print('hey')
    # import tkinter as  tk
    # from threading import Thread as thread
    # import time

    # class T():
    #     def det2(self,x):
    #         time.sleep(2)
    #         x.destroy()

    # x = tk.Tk()
    # ts = thread(target=T().det2, args=(x,))
    # ts.daemon = True
    # ts.start()
    # x.mainloop()