import cv2
import numpy as np

# ============================= Preprocessor =============================
class Preprocessor:
    def __init__(self, enable_lab_mask, enable_hsv_mask, enable_morph_mask):
        self.enable_lab_mask = enable_lab_mask
        self.enable_hsv_mask = enable_hsv_mask
        self.enable_morph_mask = enable_morph_mask

    def pick_hsv(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            hsv_frame = cv2.cvtColor(param, cv2.COLOR_BGR2HSV)
            pixel_hsv = hsv_frame[y, x]
            print(f"Clicked Pixel HSV: {pixel_hsv}")

    def hsv_filter(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0, 0, 80], dtype=np.uint8)
        upper_white = np.array([255, 50, 220], dtype=np.uint8)
        white_mask = cv2.inRange(hsv, lower_white, upper_white)
        return white_mask

    def lab_filter(self, frame):
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        lower_white = np.array([130, 120, 120], dtype=np.uint8)
        upper_white = np.array([255, 135, 135], dtype=np.uint8)
        white_mask = cv2.inRange(lab, lower_white, upper_white)
        return white_mask

    def morphology(self, frame):
        kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 12))
        morphed = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel2)
        # morphed = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel1)
        return morphed

    def preprocess_frame(self, frame):
        print("======================Preprocessor===================")
        cv2.imshow("Original", frame)
        cv2.setMouseCallback("Original", self.pick_hsv, frame)

        lab_mask = True
        hsv_mask = None
        morphed = True

        if self.enable_hsv_mask:
            hsv_mask = self.hsv_filter(frame)
            cv2.imshow("HSV", hsv_mask)

        if self.enable_lab_mask:
            lab_mask = self.lab_filter(frame)
            cv2.imshow("LAB", lab_mask)

        if self.enable_morph_mask:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 150, 250, cv2.THRESH_BINARY)
            # cv2.imshow("Binary Frame", binary)
            morphed = self.morphology(binary)
            cv2.imshow("Morphology", morphed)

        combined_mask = self.combine_masks(hsv_mask, lab_mask, morphed)
        cv2.imshow("Combined Mask", combined_mask)
        return combined_mask
    
    def combine_masks(self, hsv_mask, lab_mask, morphed):
        # Ȱ��ȭ�� ����ũ �ɼǿ� ���� ����ũ���� ����
        if self.enable_lab_mask and self.enable_hsv_mask and not self.enable_morph_mask:
            combined_mask = cv2.bitwise_and(lab_mask, hsv_mask)
        elif self.enable_lab_mask and not self.enable_hsv_mask and self.enable_morph_mask:
            combined_mask = cv2.bitwise_and(lab_mask, morphed)
        elif not self.enable_lab_mask and self.enable_hsv_mask and self.enable_morph_mask:
            combined_mask = cv2.bitwise_and(hsv_mask, morphed)
        elif self.enable_lab_mask and self.enable_hsv_mask and self.enable_morph_mask:
            combined_mask = cv2.bitwise_and(lab_mask, hsv_mask)
            combined_mask = cv2.bitwise_and(combined_mask, morphed)
        else:
            print("Mask filter configuration is not proper. Check configuration params.")
            combined_mask = morphed

        return combined_mask
