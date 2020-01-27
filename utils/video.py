from typing import Union
from threading import Thread
from time import sleep
from cv2 import VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT


# Because cv2.VideoCapture.read() is a blocking function,
# reading frames from the camera continuously in a separate thread like this
# provides a 10-20x increase in the main app fps
class CameraStream:
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
        self.thread = None

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


class VideoStream:

    def __init__(self, video_file_path: str):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = VideoCapture(video_file_path)
        grabbed, frame = self.stream.read()
        assert grabbed and frame is not None, f"Error reading frame from video file '{video_file_path}'"
        self.height, self.width = frame.shape[:2]
        self.is_closed = False

    def read(self):  # (non-blocking)
        # return the frame most recently read
        grabbed, frame = self.stream.read()
        if not grabbed:
            self.close()
        return frame

    def close(self):
        self.is_closed = True
        self.stream.release()


def benchmark_test_1():
    import time
    import cv2
    t = time.time()
    n_frames = 10000
    c = 0
    cap = cv2.VideoCapture('/home/alex/Documents/coding/Tadpole_Tracker/data/videos/4tads/IMG_5193.MOV')
    while c < n_frames:
        grabbed, frame = cap.read()
        if not grabbed:
            break
        cv2.imshow('frame', frame)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break
        c += 1
    cv2.destroyAllWindows()
    print("{:.3f}s --> {}fps".format(time.time() - t, int(n_frames / (time.time() - t))))


def benchmark_test_2():
    import time
    import cv2
    t = time.time()
    n_frames = 1000
    c = 0
    stream = VideoStream('/home/alex/Documents/coding/Tadpole_Tracker/data/videos/4tads/IMG_5193.MOV')
    while c < n_frames:
        frame = stream.read()
        if stream.is_closed or frame is None:
            break
        cv2.imshow('frame', frame)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break
        c += 1
    cv2.destroyAllWindows()
    print("{:.3f}s --> {}fps".format(time.time() - t, int(n_frames / (time.time() - t))))

if __name__ == "__main__":
    # benchmark_test_1()
    benchmark_test_2()
