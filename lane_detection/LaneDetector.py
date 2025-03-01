import cv2
import numpy as np

# ============================= Lane Detector =============================
class LaneDetector:
    def __init__(self, window_margin=50, minpix = 10, nwindows = 20):
        self.window_margin = window_margin
        self.minpix = minpix
        self.nwindows = nwindows

    def histogram_lane_search(self, roi_lane_frame):
        print("====================lane Detector==================")
        histogram = np.sum(roi_lane_frame[roi_lane_frame.shape[0] // 2:, :], axis=0)
        midpoint = int(histogram.shape[0] // 2)
        left_lane_base_x = np.argmax(histogram[:midpoint])
        right_lane_base_x = np.argmax(histogram[midpoint:]) + midpoint
        return left_lane_base_x, right_lane_base_x

    def sliding_window_lane_search(self, roi_lane_frame, left_lane_base_x, right_lane_base_x):
        window_height = 20
        # window_height = roi_lane_frame.shape[0] // self.nwindows
        nonzero = roi_lane_frame.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])

        left_lane_inds = []
        right_lane_inds = []
        leftx_current = left_lane_base_x
        rightx_current = right_lane_base_x

        output = np.dstack((roi_lane_frame, roi_lane_frame, roi_lane_frame)) * 255 # output : �����̵� ������ �׷��� �ð�ȭ�� �̹��� 

        for window in range(self.nwindows):
            win_y_low = roi_lane_frame.shape[0] - (window + 1) * window_height
            win_y_high = roi_lane_frame.shape[0] - window * window_height
            win_leftx_min = leftx_current - self.window_margin
            win_leftx_max = leftx_current + self.window_margin
            win_rightx_min = rightx_current - self.window_margin
            win_rightx_max = rightx_current + self.window_margin

            good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) &
                                (nonzerox >= win_leftx_min) & (nonzerox < win_leftx_max)).nonzero()[0]
            good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) &
                                 (nonzerox >= win_rightx_min) & (nonzerox < win_rightx_max)).nonzero()[0]

            if len(good_left_inds) > self.minpix:
                left_lane_inds.append(good_left_inds)
                cv2.rectangle(output, (win_leftx_min, win_y_low), (win_leftx_max, win_y_high), (0, 255, 0), 2)
                leftx_current = int(np.mean(nonzerox[good_left_inds]))
        
            if len(good_right_inds) > self.minpix:
                right_lane_inds.append(good_right_inds)
                cv2.rectangle(output, (win_rightx_min, win_y_low), (win_rightx_max, win_y_high), (0, 255, 0), 2)
                rightx_current = int(np.mean(nonzerox[good_right_inds]))

        # ������ ������� ���� ��� ���� ó�� 
        # �� �迭 ��� None ��ȯ 
        if not left_lane_inds or not right_lane_inds:
            print("Warning: No lane detected in sliding window search.")
            return output, None, None, None, None

        # ���� ��ǥ ������ ���� 
        if left_lane_inds:
            left_lane_inds = np.concatenate(left_lane_inds)
        else:
            left_lane_inds = np.array([])

        if right_lane_inds:
            right_lane_inds = np.concatenate(right_lane_inds)
        else:
            right_lane_inds = np.array([])

        leftx, lefty = nonzerox[left_lane_inds], nonzeroy[left_lane_inds]
        rightx, righty = nonzerox[right_lane_inds], nonzeroy[right_lane_inds]


        if len(lefty) > 0 and len(leftx) > 0:
            output[lefty, leftx] = [255, 0, 0]
        if len(righty) > 0 and len(rightx) > 0:
            output[righty, rightx] = [0, 0, 255]

        return output, leftx, lefty, rightx, righty



