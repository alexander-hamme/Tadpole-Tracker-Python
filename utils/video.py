from typing import Union
from threading import Thread
from time import sleep
from cv2 import VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT


# Because cv2.VideoCapture.read() is a blocking function,
# reading frames from the camera continuously in a separate thread like this
# provides a 10-20x increase in the main app fps
class VideoStream:
    # https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
    TARGET_RES = (640, 480)

    def __init__(self, src: Union[int, str]=0, target_res=TARGET_RES):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = VideoCapture(src)
        self.stream.set(CAP_PROP_FRAME_WIDTH, target_res[0])
        self.stream.set(CAP_PROP_FRAME_HEIGHT, target_res[1])
        self.grabbed, self.frame = self.stream.read()

        # initialize the variable flag used to indicate if the thread should be stopped
        self.stopped = True

        # if VideoStream.AUTO_START:
        # self.start()

    def start(self):
        # start the thread to read frames from the video stream
        self.stopped = False
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            self.grabbed, self.frame = self.stream.read()

    def read(self):  # (non-blocking)
        # return the frame most recently read
        return self.frame

    def is_streaming(self):
        return not self.stopped

    def stop(self):

        if not self.stopped:
            self.stopped = True       # set flag first to return from update function
            self.thread.join()        # thread needs to be terminated before stream is released
            self.stream.release()
