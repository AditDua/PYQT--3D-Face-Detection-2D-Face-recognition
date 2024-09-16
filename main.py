import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from main_screen import MainApp
from capture_dialogue import CaptureDialogueBox
from face_recognition import FaceRecognitionApp
from three_d_face_detection import ThreeDFaceDetectionApp 

def main():
    app = QApplication(sys.argv)
    
    main_window = QStackedWidget()
    main_screen = MainApp()
    image_capture_screen = CaptureDialogueBox()
    face_recognition_screen = FaceRecognitionApp()
    three_d_detection_screen = ThreeDFaceDetectionApp()  # Add the 3D detection screen
    
    main_window.addWidget(main_screen)            # Index 0
    main_window.addWidget(image_capture_screen)   # Index 1
    main_window.addWidget(face_recognition_screen)  # Index 2
    main_window.addWidget(three_d_detection_screen)  # Index 3
    
    main_window.setCurrentIndex(0)
    main_window.setWindowTitle("Face Recognition System")
    main_window.setGeometry(100, 100, 800, 600)
    main_window.show()    
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

