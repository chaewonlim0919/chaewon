import numpy as np

# 차량 제어 관련 상수
WHEEL_BASE = 0.3  # 앞바퀴-뒷바퀴 거리 (m)
LOOK_AHEAD_DISTANCE = 1.0  # Look Ahead Distance (m)
LANE_WIDTH = 0.6  # 차선 폭 (m)
MAX_STEERING_ANGLE = 40  # 최대 조향각 (degrees)

class PurePursuitController:
    def __init__(self):
        self.angle_history = []  # 이동 평균 필터용

    def moving_average_filter(self, new_angle, window_size=5):
        self.angle_history.append(new_angle)
        if len(self.angle_history) > window_size:
            self.angle_history.pop(0)
        return np.mean(self.angle_history)

    def calculate_steering(self, vehicle_pos, heading, look_ahead_point):
        x_c, y_c = vehicle_pos
        x_la, y_la = look_ahead_point

        dx = x_la - x_c
        dy = y_la - y_c
        L_d = np.sqrt(dx**2 + dy**2)

        if L_d == 0:
            print("Invalid Look Ahead Point.")
            return 0

        alpha = np.arctan2(dy, dx) - heading
        curvature = 2 * np.sin(alpha) / L_d
        steering_angle_rad = np.arctan(WHEEL_BASE * curvature)
        steering_angle_deg = self.moving_average_filter(np.degrees(steering_angle_rad))
        steering_angle_deg = np.clip(steering_angle_deg, -MAX_STEERING_ANGLE, MAX_STEERING_ANGLE)

        return steering_angle_deg
