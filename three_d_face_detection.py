import cv2
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,QSizePolicy
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QFont
from time import time
import FaceMeshModule as fmm  # Import your FaceMeshModule

class ThreeDFaceDetectionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Initialize FaceMeshDetector
        self.detector = fmm.FaceMeshDetector(maxFaces=10)
        self.cap = cv2.VideoCapture(0)
        self.pTime = 0

        # Timer to update the camera feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera_feed)
        self.timer.start(30)  # Update every 30 ms

    def initUI(self):
        self.setWindowTitle("3D Face Detection")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.label = QLabel("3D Face Detection Screen", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Arial', 24))
        layout.addWidget(self.label)

        self.image_label = QLabel(self)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        button_layout = QHBoxLayout()

        # Back button
        self.back_button = QPushButton("Back", self)
        self.back_button.setFixedSize(100, 40)
        self.back_button.clicked.connect(self.go_back)
        button_layout.addWidget(self.back_button)

        layout.addLayout(button_layout)
        layout.setAlignment(button_layout, Qt.AlignCenter)

        self.setLayout(layout)

    def update_camera_feed(self):
        success, img = self.cap.read()
        if success:
            img, faces = self.detector.findFaceMesh(img)
            cTime = time()
            fps = 1 / (cTime - self.pTime)
            self.pTime = cTime

            # Convert image to displayable format
            img = cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, channel = img_rgb.shape
            step = channel * width
            qImg = QImage(img_rgb.data, width, height, step, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)

            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def go_back(self):
        parent = self.parent()
        if parent:
            parent.setCurrentIndex(0)  # Switch to the main screen

    def closeEvent(self, event):
        self.cap.release()
        self.timer.stop()
        event.accept()
