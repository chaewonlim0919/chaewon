from turtle import left
import cv2
import numpy as np

# ============================= Lane Fitter =============================
class LaneFitter:
    def __init__(self, polynomial_order=3):
        self.polynomial_order = polynomial_order

    def fit_side_lane_polynomial(self, image, left_lane_x, left_lane_y, right_lane_x, right_lane_y):
        print("====================Lane Fitter====================")
        # ���� �� None ���� �ִ°�� �� �迭 ��ȯ
        if left_lane_x is None or len(left_lane_x) == 0 or left_lane_y is None or len(left_lane_y) == 0:
            raise ValueError("Left lane data is empty or None.")
        if right_lane_x is None or len(right_lane_x) == 0 or right_lane_y is None or len(right_lane_y) == 0:
            raise ValueError("Right lane data is empty or None.")


        # ���̰� 2 �̸��̸� ���׽� ���� �Ұ���
        if len(left_lane_x) < 2 or len(left_lane_y) < 2 or len(right_lane_x) < 2 or len(right_lane_y) < 2:
            raise ValueError("No Data!.")

        # 1���� �迭�� ����� (�̵̹Ǿ������� Ȥ�� ����)
        left_lane_x = np.ravel(left_lane_x)
        left_lane_y = np.ravel(left_lane_y)
        right_lane_x = np.ravel(right_lane_x)
        right_lane_y = np.ravel(right_lane_y)

        # ���� x, y ������ ���� ���߱� (�̵̹Ǿ������� �� Ȥ�� ����)
        min_len_left = min(len(left_lane_x), len(left_lane_y))
        min_len_right = min(len(right_lane_x), len(right_lane_y))

        left_lane_x = left_lane_x[:min_len_left]
        left_lane_y = left_lane_y[:min_len_left]
        right_lane_x = right_lane_x[:min_len_right]
        right_lane_y = right_lane_y[:min_len_right]

        try:
            left_lane_coefficients = np.polyfit(left_lane_y, left_lane_x, self.polynomial_order)
            right_lane_coefficients = np.polyfit(right_lane_y, right_lane_x, self.polynomial_order)
            print(f"Len of Left Lane Coefficients :" ,len(left_lane_coefficients)) # 3�� ���׽����� ��� 4 ���
            print(f"Len of Right Lane Coefficients :", len(right_lane_coefficients))       
        except np.linalg.LinAlgError as e:
            raise ValueError("Poly Fitting Failed : {f-string}")

        lane_y = np.linspace(0, image.shape[0] - 1, image.shape[0])

        left_fit_x = left_lane_coefficients[0] * lane_y**3 + left_lane_coefficients[1] * lane_y**2 + left_lane_coefficients[2] * lane_y + left_lane_coefficients[3]
        right_fit_x = right_lane_coefficients[0] * lane_y**3 + right_lane_coefficients[1] * lane_y**2 + right_lane_coefficients[2] * lane_y + right_lane_coefficients[3]
        print(f"Left Fit X Shape : {left_fit_x.shape}") # (480,) : 480���� x ��ǥ ������ 1���� �迭 
        # print(f"Left Fit X Value : {left_fit_x}") # ���� �ʹ� ũ�ų� �ʹ� ������ Ȯ�� 
        print(f"Right Fit X Shape : {right_fit_x.shape}")
        # print(f"Right Fit X Value : {right_fit_x}")

        return left_fit_x, right_fit_x, lane_y

    def fit_center_lane_polynomial(self, left_lane_x, left_lane_y, right_lane_x, right_lane_y, src_point, dst_point):
        min_len = min(len(left_lane_x), len(right_lane_x))
        left_lane_x = left_lane_x[:min_len]
        right_lane_x = right_lane_x[:min_len]
        left_lane_y = left_lane_y[:min_len]
        right_lane_y = right_lane_y[:min_len]

        if len(left_lane_y) > len(right_lane_y):
            center_lane_y = right_lane_y
        else:
            center_lane_y = left_lane_y
        
        center_lane_x = (left_lane_x + right_lane_x) / 2
        center_lane_coefficients = np.polyfit(center_lane_y, center_lane_x, self.polynomial_order)
        center_lane_fit_x = np.polyval(center_lane_coefficients, center_lane_y)
        print(f"Len of Center Lane Coefficients :", len(center_lane_coefficients))  
        return center_lane_coefficients, center_lane_fit_x, center_lane_y
