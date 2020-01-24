import time

from qimage2ndarray import array2qimage
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from os import path
import cv2
import sys

from utils.video import VideoStream

class _MainApp(QDialog):
    pass


class MainApp(QWidget):   # QDialog

    APP_NAME = "My Dank Little App"
    WINDOW_SIZE = (720, 720)
    WINDOW_NAME = "My Dank Little Webcam"
    CAM_RESOLUTION = (640, 480)

    APP_ICON = "{}/icons/tracker_icon.png".format(path.dirname(__file__))

    PRINT_CAM_LATENCY = True

    WEBCAM_START_BUTTON_CSS = "background-color: rgba(46, 190, 140, 1.0);"
    WEBCAM_STOP_BUTTON_CSS = "background-color: red; color: black;"
    WEBCAM_STREAM_BG_CSS = "background-color: rgb(240,240,240);"  # rgb(120,120,130)
    WEBCAM_STREAM_BG_IMG = "background-color: rgb(200,220,250);"

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)

        self.WEBCAM_IS_STREAMING = False

        self.video_stream = None
        self.video_stream_timer = QTimer()
        self.video_stream_timer.timeout.connect(self.display_video_stream)

        self.CAN_EXIT = False

        self.setup_main_window()

        self.create_left_side_box()

        self.create_video_stream_box()

        self.do_final_construction()

    def setup_main_window(self):

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(MainApp.WINDOW_NAME)


        self.setWindowIcon(QIcon(MainApp.APP_ICON))

        QApplication.setStyle(QStyleFactory.create('Fusion'))

        self.resize(*MainApp.WINDOW_SIZE)
        frame_geom = self.frameGeometry()
        current_active_screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_pos = QApplication.desktop().screenGeometry(current_active_screen).center()
        frame_geom.moveCenter(center_pos)
        self.move(frame_geom.topLeft())


    def webcam_radio_button1(self):
        toggled = self.sender().isChecked()
        print("Button 1 is {}".format("on" if toggled else "off"))

    def webcam_radio_button2(self):
        toggled = self.sender().isChecked()
        print("Button 2 is {}".format("on" if toggled else "off"))

    def webcam_check_box(self):
        print("Check box: {}".format(self.sender().isChecked()))
        toggled = self.sender().isChecked()
        MainApp.PRINT_CAM_LATENCY = not MainApp.PRINT_CAM_LATENCY

    def webcam_toggle_button(self):

        if self.sender().isChecked():
            assert not self.WEBCAM_IS_STREAMING
            self.video_stream = VideoStream(src=0, target_res=MainApp.CAM_RESOLUTION).start()
            self.video_stream_timer.start()
            self._webcam_toggle_button.setText("Stop Camera")
            self._webcam_toggle_button.setStyleSheet(MainApp.WEBCAM_STOP_BUTTON_CSS)#"background-color: rgba(46, 204, 113, 1.0)")
            self.WEBCAM_IS_STREAMING = True

        else:
            self.video_stream_timer.stop()
            self.video_stream.stop()
            self._webcam_stream_qlabel.clear()
            self._webcam_toggle_button.setText("Start Camera")
            self._webcam_toggle_button.setStyleSheet(MainApp.WEBCAM_START_BUTTON_CSS) #rgba(200, 200, 200, 1.0)")
            self._webcam_stream_qlabel.setStyleSheet(MainApp.WEBCAM_STREAM_BG_CSS)
            self._webcam_stream_qlabel.update()
            self.WEBCAM_IS_STREAMING = False

    def radio_dial(self):
        print(self.sender().value())

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Create a New Data File","example_data.csv",
            "Text Files (*.txt);;CSV Files (*.csv);;Dat Files (*.dat);;All Files (*)",
            options=options)

        if fileName is not None:
            print(fileName)

    def create_left_side_box(self):
        """Initialize widgets.
        """

        self.left_side_box = QGroupBox("Lotsa Buttons")
        # self.left_side_box.setCheckable(True)
        # self.left_side_box.setChecked(True)

        lineEdit = QLineEdit('my_data')
        # lineEdit.setEchoMode(QLineEdit.)
        # lineEdit.setEchoMode(QLineEdit.Password)

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
        dial.valueChanged.connect(self.radio_dial)
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

        wc_radio_button1 = QRadioButton("Radio button 1")
        wc_radio_button1.toggled.connect(self.webcam_radio_button1)
        wc_radio_button2 = QRadioButton("Radio button 2")
        wc_radio_button2.toggled.connect(self.webcam_radio_button2)
        wc_radio_button1.setChecked(True)

        wc_check_box = QCheckBox("Regular check box")
        wc_check_box.setTristate(False)
        wc_check_box.toggled.connect(self.webcam_check_box)
        wc_check_box.setCheckState(Qt.Checked)

        # save_data_line_entry = QLineEdit('save_data_name')
        # save_data_line_entry.selectedText()
        # save_data_line_entry.hasFocus()
        #
        # extensions_dropdown = QComboBox()
        # extensions_dropdown.setWindowTitle("Extensions")
        # extensions_dropdown.addItems(['.csv', '.txt', '.dat'])


        save_data_button = QPushButton("Save Data")
        save_data_button.setShortcut("Ctrl+S")
        # save_data_button.setStyleSheet(MainApp.WEBCAM_START_BUTTON_CSS)
        # self._webcam_toggle_button.setCheckable(True)
        # self._webcam_toggle_button.setChecked(False)
        save_data_button.clicked.connect(self.saveFileDialog)


        self._webcam_stream_qlabel = QLabel()
        self._webcam_stream_qlabel.setFixedSize(self.video_size)
        self._webcam_stream_qlabel.setAutoFillBackground(True)
        self._webcam_stream_qlabel.setStyleSheet(MainApp.WEBCAM_STREAM_BG_CSS)
        # self.image_label.setAlignment(Alignment)
        # self.main_layout.addWidget(self._video_stream_qlabel)

        self._webcam_toggle_button = QPushButton("Start Camera")
        self._webcam_toggle_button.setStyleSheet(MainApp.WEBCAM_START_BUTTON_CSS)
        self._webcam_toggle_button.setCheckable(True)
        self._webcam_toggle_button.setChecked(False)
        self._webcam_toggle_button.toggled.connect(self.webcam_toggle_button)

        layout = QVBoxLayout()
        layout.addWidget(wc_radio_button1)
        layout.addWidget(wc_radio_button2)
        layout.addWidget(wc_check_box)
        layout.addWidget(save_data_button)
        layout.addWidget(self._webcam_stream_qlabel)
        layout.addWidget(self._webcam_toggle_button)

        layout.addStretch(stretch=1)
        self.video_stream_box.setLayout(layout)

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
        self._webcam_stream_qlabel.setPixmap(QPixmap.fromImage(qimage))
        self._webcam_stream_qlabel.update()

        if MainApp.PRINT_CAM_LATENCY:
            print("\r{:.2}".format(time.time()-t), end='')

    # def close(self):
    #     self.video_stream.stop()
    #     super(MainApp, self).close()

    def test(self):
        print('yo')

    def attempt_exit(self):

        if self.video_stream is None or not self.WEBCAM_IS_STREAMING:  # or not self.video_stream.is_streaming()
            self.CAN_EXIT = True
            return
        else:
            # Ask User are you sure you want to exit?
            self.video_stream_timer.stop()
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

    '''
    todo: subclass QApplication in a new file instead of doing this
    '''

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    app.setApplicationName(MainApp.APP_NAME)
    # app.setApplicationDisplayName(MainApp.APP_NAME)

    win = MainApp()
    win.show()

    sys.exit(app.exec_())


