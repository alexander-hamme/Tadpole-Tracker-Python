import time

from qimage2ndarray import array2qimage
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import sys

from utils.video import VideoStream


class MainApp(QWidget):

    WINDOW_SIZE = (720, 720)
    CAM_RESOLUTION = (640, 480)

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)

        self.setup_main_window()

        self.video_size = QSize(*MainApp.CAM_RESOLUTION)
        self.create_components()


        self.video_stream = VideoStream(src=0, target_res=MainApp.CAM_RESOLUTION).start()

        # self.capture = cv2.VideoCapture(0)
        # self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        # self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.height())

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(10)

        self.EXITING = False


    def setup_main_window(self):
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("My Dank Little Webcam")
        self.resize(*MainApp.WINDOW_SIZE)

    def create_components(self):
        """Initialize widgets.
        """
        self.image_label = QLabel()
        self.image_label.setFixedSize(self.video_size)

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self._close)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.quit_button)

        self.setLayout(self.main_layout)


    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """

        t = time.time()

        frame = self.video_stream.read()
        # frame = self.capture.read()[1]

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)

        qimage = array2qimage(frame)

        # image = QImage(frame, frame.shape[1], frame.shape[0],       # faster, but potentially causes memory leak?
        #                frame.strides[0], QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qimage))
        print("\r{:.2}".format(time.time()-t), end='')

    def _close(self):
        self.video_stream.stop()
        self.close()


        # listen for CloseEvent


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    win = MainApp()
    win.show()

    sys.exit(app.exec_())


