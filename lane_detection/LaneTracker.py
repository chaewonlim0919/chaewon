import cv2
import numpy as np

# ============================= Lane Tracker ==========================
class LaneTracker:
    def __init__(self, max_history=5, position_threshold=50):
        self.max_history = max_history
        self.position_threshold = position_threshold
        self.left_lane_history = []
        self.right_lane_history = []

    def update_lane_positions(self, left_fit_x, right_fit_x):
        if len(self.left_lane_history) >= self.max_history:
            self.left_lane_history.pop(0)
        if len(self.right_lane_history) >= self.max_history:
            self.right_lane_history.pop(0)

        self.left_lane_history.append(left_fit_x)
        self.right_lane_history.append(right_fit_x)

    def get_smoothed_lane_positions(self):
        
        if not self.left_lane_history or not self.right_lane_history:
            return None, None
        
        left_avg = np.mean(self.left_lane_history, axis=0)
        right_avg = np.mean(self.right_lane_history, axis=0)
        
        return left_avg, right_avg

    def validate_lane_positions(self, left_fit_x, right_fit_x):
        if not self.left_lane_history or not self.right_lane_history:
            return True  # ù ��° �������̹Ƿ� ���� ���� ���
        
        prev_left = self.left_lane_history[-1]
        prev_right = self.right_lane_history[-1]
        
        left_diff = np.abs(prev_left - left_fit_x).mean()
        right_diff = np.abs(prev_right - right_fit_x).mean()
        
        return left_diff < self.position_threshold and right_diff < self.position_threshold
