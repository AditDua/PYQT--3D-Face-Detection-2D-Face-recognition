from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication, QHBoxLayout
from PyQt5.QtCore import Qt
from FaceIDLight.demo import Demonstrator

class FaceRecognitionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Face Recognition App")
        self.setGeometry(100, 100, 800, 600)
        
        # Main vertical layout
        main_layout = QVBoxLayout()
        
        # Center content layout
        center_layout = QVBoxLayout()
        
        self.label = QLabel("Face Recognition Screen", self)
        self.label.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(self.label)
        
        # Centered Run Face Recognition button
        run_button_layout = QHBoxLayout()
        self.run_button = QPushButton("Run Face Recognition", self)
        self.run_button.setFixedSize(200, 40)
        self.run_button.clicked.connect(self.run_face_recognition)
        run_button_layout.addStretch()
        run_button_layout.addWidget(self.run_button)
        run_button_layout.addStretch()
        center_layout.addLayout(run_button_layout)
        
        # Add center layout to the main layout
        main_layout.addLayout(center_layout)
        
        # Bottom buttons layout
        bottom_layout = QHBoxLayout()
        
        # Back button
        self.back_button = QPushButton("Back", self)
        self.back_button.setFixedSize(100, 40)
        self.back_button.clicked.connect(self.go_back)
        bottom_layout.addWidget(self.back_button)
        
        # Quit button
        self.quit_button = QPushButton("Quit", self)
        self.quit_button.setFixedSize(100, 40)
        self.quit_button.clicked.connect(self.quit_application)
        bottom_layout.addWidget(self.quit_button)
        
        # Add bottom layout to the main layout
        bottom_layout.addStretch()  # Add stretch to push buttons to the bottom
        main_layout.addLayout(bottom_layout)
        
        self.setLayout(main_layout)

    def run_face_recognition(self):
        self.label.setText("Running Face Recognition...")
        # Start face recognition process
        Demonstrator(gal_dir="Images").run()

    def go_back(self):
        self.parent().setCurrentIndex(0)  # Switch to the main screen

    def quit_application(self):
        QApplication.instance().quit()
