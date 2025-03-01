import cv2

class Camera:
    def __init__(self, cam_index=0, width=640, height=480):
        self.cap = cv2.VideoCapture(cam_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        if not self.cap.isOpened():
            print("Error: Could not open camera.")
    
    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Could not read frame.")
            return None
        return frame
    
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
