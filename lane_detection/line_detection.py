# -*- coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt

from Preprocessor import Preprocessor
from PerspectiveTransformer import PerspectiveTransformer
from LaneDetector import LaneDetector
from LaneFitter import LaneFitter
# from LaneTracker import LaneTracker
from Visualizer import Visualizer

# ============================= Pipeline =============================
class LaneDetectionPipeline:
    def __init__(self, src_point, dst_point):
        self.src_point = src_point
        self.dst_point = dst_point

        self.preprocessor = Preprocessor(True, False, True)
        self.perspective_transformer = PerspectiveTransformer(self.src_point, self.dst_point)
        self.lane_detector = LaneDetector()
        self.lane_fitter = LaneFitter()
        # self.lane_tracker = LaneTracker()
        self.visualizer = Visualizer()

        self.prev_lane_frame = None # previous frmae save

    def process_frame(self, frame): 
        preprocessed = self.preprocessor.preprocess_frame(frame)
        bird_eye_view = self.perspective_transformer.perspective_transform(preprocessed)
        roi_lane_frame = self.perspective_transformer.apply_lane_roi(bird_eye_view)
        cv2.imshow("ROI Lane Frame", roi_lane_frame)

        left_lane_base_x, right_lane_base_x = self.lane_detector.histogram_lane_search(roi_lane_frame) # �ʱ�������ġ�� ����� x��ǥ �ΰ� 

        try:
            detected_line_img, left_lane_x, left_lane_y, right_lane_x, right_lane_y = \
                self.lane_detector.sliding_window_lane_search(roi_lane_frame, left_lane_base_x, right_lane_base_x)
            cv2.imshow("Detected Lines", detected_line_img)
            print(detected_line_img.shape) # (480, 640, 3)

            # �� �迭���� Ȯ�� (�� ��� np.polyfit ������ �߻���)
            if len(left_lane_x) == 0 or len(left_lane_y) == 0 or len(right_lane_x) == 0 or len(right_lane_y) == 0:
                raise ValueError("Empty lane detection arrays.")

            left_lane_fit_x, right_lane_fit_x, lane_y = self.lane_fitter.fit_side_lane_polynomial(roi_lane_frame, 
                left_lane_x, left_lane_y, right_lane_x, right_lane_y)

            center_lane_coefficients, center_lane_fit_x, center_lane_y = self.lane_fitter.fit_center_lane_polynomial(
                left_lane_x, left_lane_y, right_lane_x, right_lane_y, self.src_point, self.dst_point)

            # self.lane_tracker.update_lane_positions(left_lane_fit_x, right_lane_fit_x)
            # smoothed_left_x, smoothed_right_x = self.lane_tracker.get_smoothed_lane_positions()
            
            final_frame = self.visualizer.draw_final_output(
                frame, left_lane_fit_x, right_lane_fit_x, center_lane_fit_x, lane_y, center_lane_y, self.src_point, self.dst_point)
            
            # ��� ���� (���� �����ӿ��� Ȱ��)
            self.prev_lane_frame = final_frame

        except Exception as e:
            print("==============================Error=============================")
            print("Error details:", e)
            if self.prev_lane_frame is not None:
                final_frame = self.prev_lane_frame
            else:
                final_frame = frame

        return final_frame


# ============================= Main Function =============================
def main():
    video_path = "./track1.mp4"
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video at {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30
    frame_delay = int(1000 / fps)
    print(f"Video FPS: {fps}, Frame delay: {frame_delay} ms")

    ret, frame = cap.read()
    if not ret:
        print("Error: Cannot read the first frame from the video.")
        cap.release()
        return

    height, width = frame.shape[:2]
    print(f"Video resolution: {width}x{height}")

    src_point = np.float32([
        [width * 0.1, height],       # ���� �ϴ�
        [width * 0.9, height],       # ���� �ϴ�
        [width * 0.2, height * 0.6],   # ���� ���
        [width * 0.8, height * 0.6]    # ���� ���
    ])
    dst_point = np.float32([
        [200, height],
        [width - 200, height],
        [100, 0],
        [width - 100, 0]
    ])

    pipeline = LaneDetectionPipeline(src_point, dst_point)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video or error reading frame.")
            break

        output_frame = pipeline.process_frame(frame)
        cv2.imshow("Lane Detection (Pipline Process Frmae Output", output_frame)

        if cv2.waitKey(60) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
