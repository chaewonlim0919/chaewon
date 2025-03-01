import cv2
import numpy as np

# ============================= Visualizer =============================
class Visualizer:
    def __init__(self, overlay_opacity=0.3, lane_color=(0, 255, 0), center_color=(0, 255, 255), thickness=5):

        self.overlay_opacity = overlay_opacity # ������ 
        self.lane_color = lane_color
        self.center_color = center_color
        self. thickness = thickness

    def draw_lane_area(self, frame, left_fit_x, right_fit_x, lane_y, src_point, dst_point):
        print("==================Draw Lane===================")
        print(f"X Fit Shape:", {left_fit_x.shape}, {right_fit_x.shape})
        print(f"Y Fit Shape:", {lane_y.shape})

        # pts_left_lane = np.array([np.transpose(np.vstack([left_fit_x, lane_y]))], dtype=np.int32)
        # pts_right_lane = np.flipud(np.array(np.transpose(np.vstack([right_fit_x, lane_y]))))
        pts_left_lane = np.column_stack((left_fit_x, lane_y)).astype(np.int32)
        pts_right_lane = np.flipud(np.column_stack((right_fit_x, lane_y))).astype(np.int32)
        print(f"Left Lane Points Shape :", (pts_left_lane.shape))
        print(f"Left Right Points Shape :", (pts_right_lane.shape))
        pts_lane = np.vstack([pts_left_lane, pts_right_lane])
        print(pts_lane.shape)
        # fillPoly ��� ���� ���߱� 
        pts_lane = pts_lane.reshape((-1,1,2))
        print(pts_lane.shape)
        
        lane_visualization = np.zeros_like(frame)
        cv2.fillPoly(lane_visualization, [pts_lane], self.lane_color)
        cv2.imshow("Lane Visualization Check", lane_visualization)
        
        inverse_transform_matrix = cv2.getPerspectiveTransform(dst_point, src_point)
        lane_visualization = cv2.warpPerspective(lane_visualization, inverse_transform_matrix, (frame.shape[1], frame.shape[0]))
        
        draw_lane_frame = cv2.addWeighted(frame, 1, lane_visualization, self.overlay_opacity, 0)
        return draw_lane_frame

    def draw_center_lane(self, frame, center_fit_x, center_lane_y, src_point, dst_point):
        # pts_center_lane = np.array([np.transpose(np.vstack([center_fit_x, center_lane_y]))], dtype=np.int32)
        pts_center_lane = np.column_stack((center_fit_x, center_lane_y)).astype(np.int32)
        print(f"Center Lane Point Shape :", (pts_center_lane.shape))
        center_lane_visualization = np.zeros_like(frame)
        cv2.polylines(center_lane_visualization, [pts_center_lane], isClosed=False, color=self.center_color, thickness=self. thickness)
        cv2.imshow("Center Lane Visualization Check", center_lane_visualization)

        inverse_transform_matrix = cv2.getPerspectiveTransform(dst_point, src_point)
        center_lane_visualization = cv2.warpPerspective(center_lane_visualization, inverse_transform_matrix, (frame.shape[1], frame.shape[0]))
        
        draw_center_lane_frame = cv2.addWeighted(center_lane_visualization, 1, frame, 1, 0)
        cv2.imshow("Lane Frame Check", draw_center_lane_frame)
        return draw_center_lane_frame

    def draw_final_output(self, frame, left_fit_x, right_fit_x, center_fit_x, lane_y, center_lane_y, src_point, dst_point):
        frame_with_lane = self.draw_lane_area(frame, left_fit_x, right_fit_x, lane_y, src_point, dst_point)
        final_frame = self.draw_center_lane(frame_with_lane, center_fit_x, center_lane_y, src_point, dst_point)
        return final_frame
