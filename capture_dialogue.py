import os
import cv2
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QFont, QPainter
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFormLayout, QSizePolicy, QMessageBox, QHBoxLayout

class CaptureDialogueBox(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.capture_index = 0
        self.countdown = 8
        self.angles = ["straight","left", "right", "slight left", "slight right", "far away"]
        self.base_filename = ""

        if not os.path.exists('Images'):
            os.makedirs('Images')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        
        self.camera_timer = QTimer(self)
        self.camera_timer.timeout.connect(self.update_camera_feed)

        self.cap = cv2.VideoCapture(0)
        self.camera_timer.start(30)

    def initUI(self):
        self.setWindowTitle("Image Capture App")
        self.setGeometry(100, 100, 800, 600)
        
        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.filename_input = QLineEdit(self)
        self.form_layout.addRow(QLabel("Enter your name:"), self.filename_input)
        self.layout.addLayout(self.form_layout)
        
        # Label to instruct the user
        self.label = QLabel("Press Capture to start", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Camera feed
        self.image_label = QLabel(self)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        # Capture button centered below the camera feed
        button_layout = QHBoxLayout()
        self.capture_button = QPushButton("Capture", self)
        self.capture_button.setFixedSize(250, 40)
        self.capture_button.clicked.connect(self.handle_capture)
        button_layout.addStretch()
        button_layout.addWidget(self.capture_button)
        button_layout.addStretch()
        self.layout.addLayout(button_layout)

        self.face_recognition_button = QPushButton("Go to Face Recognition", self)
        self.face_recognition_button.setFixedSize(200, 40)
        self.face_recognition_button.clicked.connect(self.switch_to_face_recognition)
        self.face_recognition_button.setVisible(False)
        self.layout.addWidget(self.face_recognition_button)

        self.back_button = QPushButton("Back", self)
        self.back_button.setFixedSize(100, 40)
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)
        self.show()

    def handle_capture(self):
        if not self.base_filename:
            self.base_filename = self.filename_input.text().strip()
            if not self.base_filename:
                self.label.setText("Please enter your name.")
                return
            self.label.setText(f"Take image from the {self.angles[self.capture_index]} angle")
            self.countdown = 8
            self.timer.start(1000)
        else:
            self.capture_image()

    def start_countdown(self):
        self.label.setText(f"Take image from the {self.angles[self.capture_index]} angle")
        self.countdown = 8
        self.timer.start(1000)

    def update_countdown(self):
        if self.countdown > 0:
            self.countdown -= 1
        else:
            self.timer.stop()
            self.capture_image()

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame_rgb.shape
            step = channel * width
            qImg = QImage(frame_rgb.data, width, height, step, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)

            # Display the captured image
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            # Stop the camera feed to show the preview
            self.camera_timer.stop()
            self.confirm_save_image(frame)
        else:
            self.label.setText("Failed to capture image. Please try again.")
            self.start_countdown()

    def confirm_save_image(self, frame):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Save Image")
        msg_box.setText("Do you want to save this image?")
        msg_box.setStandardButtons(QMessageBox.Save | QMessageBox.Retry)
        msg_box.setDefaultButton(QMessageBox.Save)

        response = msg_box.exec_()
        if response == QMessageBox.Save:
            self.save_image(frame)
        else:
            self.camera_timer.start(30)  # Restart the camera feed for retry
            self.start_countdown()

    def save_image(self, frame):
        # Use the format "user_X" where X is the index + 1
        filename = os.path.join('Images', f"{self.base_filename}_{self.capture_index + 1}.png")
        cv2.imwrite(filename, frame)
        self.capture_index += 1
        if self.capture_index < len(self.angles):
            self.camera_timer.start(30)  # Restart the camera feed for the next capture
            self.start_countdown()
        else:
            self.label.setText("All images have been captured.")
            self.capture_button.setVisible(False)
            self.face_recognition_button.setVisible(True)
            self.cap.release()
            self.camera_timer.stop()


    def update_camera_feed(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            step = channel * width
            qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)

            # Scale the pixmap to fit the QLabel size
            pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

            if self.timer.isActive():
                # Create a temporary QImage to draw text
                temp_img = QImage(pixmap.size(), QImage.Format_RGB888)
                temp_img.fill(Qt.black)
                painter = QPainter(temp_img)
                painter.drawPixmap(0, 0, pixmap)
                painter.setPen(Qt.white)
                painter.setFont(QFont('Arial', 150))
                painter.drawText(temp_img.rect(), Qt.AlignCenter, str(self.countdown))
                painter.end()

                pixmap = QPixmap.fromImage(temp_img)

            self.image_label.setPixmap(pixmap)

    def switch_to_face_recognition(self):
        self.label.setText("Switching to Face Recognition...")
        self.parent().setCurrentIndex(2)

    def go_back(self):
        self.parent().setCurrentIndex(0)

    def closeEvent(self, event):
        self.cap.release()
        self.camera_timer.stop()
        event.accept()
