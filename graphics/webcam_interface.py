import time

from qimage2ndarray import array2qimage
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import sys

from utils.video import VideoStream

class _MainApp(QDialog):
    pass


class MainApp(QWidget):   # QDialog

    WINDOW_SIZE = (720, 720)
    CAM_RESOLUTION = (640, 480)

    PRINT_CAM_LATENCY = True

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)

        self.WEBCAM_IS_STREAMING = False

        self.video_stream = None
        self.video_stream_timer = QTimer()
        self.video_stream_timer.timeout.connect(self.display_video_stream)

        self.CAN_EXIT = False

        # Only add ones to here that may be changed during run
        self.dynamic_inputs = {
            "dial": None,
            "slider": None,
        }

        self.setup_main_window()

        self.create_left_side_box()

        self.create_video_stream_box()

        self.do_final_construction()

        # self.initialize_video_stream()

    def vs_radio_button1(self):
        toggled = self.sender().isChecked()
        print("Button 1 is {}".format("on" if toggled else "off"))

    def vs_radio_button2(self):
        toggled = self.sender().isChecked()
        print("Button 2 is {}".format("on" if toggled else "off"))

    def vs_check_box(self, val):
        print("Check box: ")
        toggled = self.sender().isChecked()
        MainApp.PRINT_CAM_LATENCY = not MainApp.PRINT_CAM_LATENCY

    def on_user_input(self):
        print("New Dial value is {}".format(self.dynamic_inputs.get("dial")))

    def setup_main_window(self):
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("My Dank Little Webcam")

        QApplication.setStyle(QStyleFactory.create('Fusion'))

        self.resize(*MainApp.WINDOW_SIZE)
        frame_geom = self.frameGeometry()
        current_active_screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_pos = QApplication.desktop().screenGeometry(current_active_screen).center()
        frame_geom.moveCenter(center_pos)
        self.move(frame_geom.topLeft())

    def create_left_side_box(self):
        """Initialize widgets.
        """

        self.left_side_box = QGroupBox("Lotsa Buttons")
        # self.left_side_box.setCheckable(True)
        # self.left_side_box.setChecked(True)

        lineEdit = QLineEdit('s3cRe7')
        lineEdit.setEchoMode(QLineEdit.Password)

        spinBox = QSpinBox(self.left_side_box)
        spinBox.setValue(50)

        dateTimeEdit = QDateTimeEdit(self.left_side_box)
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        slider = QSlider(Qt.Horizontal, self.left_side_box)
        slider.setValue(40)

        scrollBar = QScrollBar(Qt.Horizontal, self.left_side_box)
        scrollBar.setValue(60)

        dial = QDial(parent=self.left_side_box)
        dial.setMinimum(0)
        dial.setMaximum(420)
        dial.setValue(69)
        dial.setNotchTarget(30.0)
        dial.valueChanged.connect(self.on_user_input)
        dial.setNotchesVisible(True)

        layout = QGridLayout()
        layout.addWidget(lineEdit, 0, 0, 1, 2)
        layout.addWidget(spinBox, 1, 0, 1, 2)
        layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
        layout.addWidget(slider, 3, 0)
        layout.addWidget(scrollBar, 4, 0)
        layout.addWidget(dial, 3, 1, 2, 1)
        layout.setRowStretch(5, 1)
        self.left_side_box.setLayout(layout)

        # self.quit_button = QPushButton("Quit")
        # self.quit_button.clicked.connect(self.test)
        #
        # self.main_layout = QVBoxLayout()
        # self.main_layout.addWidget(self.quit_button)
        #
        # self.setLayout(self.main_layout)

    def create_video_stream_box(self):

        self.video_size = QSize(*MainApp.CAM_RESOLUTION)

        self.video_stream_box = QGroupBox("Video Stream")

        radio_button1 = QRadioButton("Radio button 1")
        radio_button1.toggled.connect(self.vs_radio_button1)
        radio_button2 = QRadioButton("Radio button 2")
        radio_button2.toggled.connect(self.vs_radio_button2)
        radio_button1.setChecked(True)

        checkBox = QCheckBox("Regular check box")
        checkBox.setTristate(False)
        checkBox.setCheckState(Qt.Checked)

        self._video_stream_qlabel = QLabel()
        self._video_stream_qlabel.setFixedSize(self.video_size)
        # self.image_label.setAlignment(Alignment)
        # self.main_layout.addWidget(self._video_stream_qlabel)

        self._toggle_webcam_button = QPushButton("Start Camera")
        self._toggle_webcam_button.setStyleSheet(
            "background-color: rgba(46, 204, 113, 1.0)")
        self._toggle_webcam_button.setCheckable(True)
        self._toggle_webcam_button.setChecked(False)
        self._toggle_webcam_button.toggled.connect(self.toggle_webcam)


        layout = QVBoxLayout()
        layout.addWidget(radio_button1)
        layout.addWidget(radio_button2)
        layout.addWidget(checkBox)
        layout.addWidget(self._video_stream_qlabel)
        layout.addWidget(self._toggle_webcam_button)

        layout.addStretch(stretch=1)
        self.video_stream_box.setLayout(layout)

    def toggle_webcam(self):

        # print(self.sender().isChecked())

        # if self.WEBCAM_IS_STREAMING:
        if self.sender().isChecked():
            assert not self.WEBCAM_IS_STREAMING
            self.video_stream = VideoStream(src=0, target_res=MainApp.CAM_RESOLUTION).start()
            self.video_stream_timer.start()
            self._toggle_webcam_button.setText("Stop Camera")
            self._toggle_webcam_button.setStyleSheet("background-color: red")#"background-color: rgba(46, 204, 113, 1.0)")
            self.WEBCAM_IS_STREAMING = True

        else:
            self.video_stream.stop()
            self.video_stream_timer.stop()
            self._toggle_webcam_button.setText("Start Camera")
            self._toggle_webcam_button.setStyleSheet("background-color: rgba(46, 204, 113, 1.0)") #rgba(200, 200, 200, 1.0)")
            self.WEBCAM_IS_STREAMING = False
    '''
    def initialize_video_stream(self):

        if self.WEBCAM_IS_STREAMING:
            return

        self.video_stream = VideoStream(src=0, target_res=MainApp.CAM_RESOLUTION)#.start()
        self.video_stream_timer = QTimer()
        self.video_stream_timer.timeout.connect(self.display_video_stream)
        # self.video_stream_timer.start(10)

        #if TOGGLE
        #self.timer.stop()
    '''

    def do_final_construction(self):

        mainLayout = QGridLayout()
        # mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.left_side_box, 1, 0)
        mainLayout.addWidget(self.video_stream_box, 1, 1)
        # mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        # mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        # mainLayout.addWidget(self.left_side_box, 2, 1)
        # mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)



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
        self._video_stream_qlabel.setPixmap(QPixmap.fromImage(qimage))

        if MainApp.PRINT_CAM_LATENCY:
            print("\r{:.2}".format(time.time()-t), end='')



    # def close(self):
    #     self.video_stream.stop()
    #     super(MainApp, self).close()

    def test(self):
        print('yo')

    def attempt_exit(self):

        if not self.video_stream.is_streaming():
            self.CAN_EXIT = True
            return
        else:
            # Ask User are you sure you want to exit?
            self.video_stream.stop()
            self.CAN_EXIT = True

    # overridden
    def closeEvent(self, event):

        self.attempt_exit()

        if self.CAN_EXIT:
            event.accept()  # let the window close
        else:
            event.ignore()

        super(MainApp, self).close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    win = MainApp()
    win.show()

    sys.exit(app.exec_())


