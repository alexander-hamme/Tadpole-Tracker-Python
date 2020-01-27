import tkinter as tk
from typing import Union

from PIL import ImageTk, Image

import cv2

from utils.video import CameraStream


class TrackerApp(tk.Frame):

    TITLE = "Tracker"
    CAMERA_SRC = 0

    def __init__(self, master=None, cam_src: Union[int,str]=CAMERA_SRC):
        super().__init__(master)

        self.master = master
        self.master.title(TrackerApp.TITLE)
        self.master.config(cursor="arrow", )

        self.pack()
        self.create_widgets()

        self.video_stream = CameraStream().start()

        self.mainloop()

    def create_widgets(self):

        self.img_label = tk.Label(self.master)  # initialize image panel
        self.img_label.pack(padx=10, pady=10)

        self.test_butt = tk.Button(self, text="Test butt", command=self.test)
        # self.test_butt.config(text="Test butt", command=self.test)
        self.test_butt.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.tear_down)
        self.quit.pack(side="bottom")

    @staticmethod
    def convert(frame):
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        return ImageTk.PhotoImage(image=img)

    def mainloop(self, n=0):
        frame = self.video_stream.read()
        self.img_label.imgtk = self.convert(frame)
        self.img_label.config(image=self.convert(frame))
        super(TrackerApp, self).mainloop()

    def test(self):
        print('yo')

    def tear_down(self):

        # self.vs.close
        self.master.destroy()
        self.video_stream.close()
    # def __init__(self, window, window_title):
    #     self.window = window
    #     self.window.title(window_title)
    #     self.window.mainloop()


    # function for video streaming

        # lmain.imgtk = imgtk
        # lmain.configure(image=imgtk)
        # lmain.after(1, video_stream)

if __name__ == "__main__":
    # Create a window and pass it to the Application object
    app = TrackerApp(tk.Tk())


