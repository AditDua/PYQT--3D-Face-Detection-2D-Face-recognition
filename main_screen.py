from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Main Screen")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # Title label
        self.title_label = QLabel("Face Recognition System", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont('Arial', 24))
        self.layout.addWidget(self.title_label)

        # Buttons layout
        self.buttons_layout = QHBoxLayout()

        # Add New User button
        self.add_user_button = self.create_button("Add New User", '#4CAF50', '#45a049', self.show_add_user)

        # Face Recognition button
        self.face_recognition_button = self.create_button("Face Recognition", '#008CBA', '#007BB5', self.show_face_recognition)

        # 3D Face Detection button
        self.three_d_detection_button = self.create_button("3D Face Detection", '#FFC107', '#FFA000', self.show_three_d_detection)

        self.buttons_layout.addWidget(self.add_user_button)
        self.buttons_layout.addWidget(self.face_recognition_button)
        self.buttons_layout.addWidget(self.three_d_detection_button)
        
        self.layout.addLayout(self.buttons_layout)
        self.layout.setAlignment(self.buttons_layout, Qt.AlignCenter)
        
        self.setLayout(self.layout)

    def create_button(self, text, bg_color, hover_color, action):
        button = QPushButton(text, self)
        button.setFont(QFont('Arial', 18))
        button.setStyleSheet(f"QPushButton {{ background-color: {bg_color}; color: white; padding: 10px; }} QPushButton:hover {{ background-color: {hover_color}; }}")
        button.clicked.connect(action)
        return button

    def show_add_user(self):
        parent = self.parent()
        if parent:
            parent.setCurrentIndex(1)  # Switch to the image capture screen

    def show_face_recognition(self):
        parent = self.parent()
        if parent:
            parent.setCurrentIndex(2)  # Switch to the face recognition screen

    def show_three_d_detection(self):
        parent = self.parent()
        if parent:
            parent.setCurrentIndex(3)  # Switch to the 3D face detection screen
