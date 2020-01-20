import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import sys

from utils.video import VideoStream


class MainApp(QWidget):

    RESOLUTION = (640, 480)

    def __init__(self):
        super(MainApp, self).__init__()
        self.video_size = QSize(*MainApp.RESOLUTION)
        self.setup_ui()


        # self.setup_camera()
        self.video_stream = VideoStream(src=0).start()    #, target_res=MainApp.RESOLUTION)


        # self.capture = cv2.VideoCapture(0)
        # self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        # self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.height())

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

    def setup_ui(self):
        """Initialize widgets.
        """
        self.image_label = QLabel()
        self.image_label.setFixedSize(self.video_size)

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.close)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.quit_button)

        self.setLayout(self.main_layout)

    def setup_camera(self):
        """Initialize camera.
        """
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        t = time.time()
        frame = self.video_stream.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        image = QImage(frame, frame.shape[1], frame.shape[0],
                       frame.strides[0], QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(image))
        print("\r{:.2}".format(time.time()-t), end='')

    def _close(self):
        self.video_stream.stop()

        # listen for CloseEvent

        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainApp()
    win.show()
    sys.exit(app.exec_())
