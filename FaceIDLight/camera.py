import threading
import cv2
import time


class Camera:
    def __init__(self, stream_id=0):
        self.stream_id = stream_id
        self.currentFrame = None
        self.ret = False
        self.stop = False
        self.capture = cv2.VideoCapture(stream_id)
        self.thread = threading.Thread(target=self.update_frame)

    # Continually updates the frame
    def update_frame(self):
        while True:
            self.ret, self.currentFrame = self.capture.read()
            while self.currentFrame is None:  # Continually grab frames until we get a good one
                self.capture.read()
            if self.stop:
                break

    # Get current frame
    def get_frame(self):
        return self.ret, self.currentFrame

    def screen(self, function):
        self.thread.start()
        window_name = "Streaming from {}".format(self.stream_id)
        cv2.namedWindow(window_name)
        last = 0
        while True:
            ret, frame = self.get_frame()
            if ret:
                frame = function(frame)
                frame = cv2.putText(
                    frame,
                    "FPS{:5.1f}".format(1 / (time.time() - last)),
                    (frame.shape[1] - 80, 30),
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    (0, 255, 0),
                )
                last = time.time()
                cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        self.stop = True
        self.thread.join()
        cv2.destroyWindow(window_name)
        self.capture.release()
