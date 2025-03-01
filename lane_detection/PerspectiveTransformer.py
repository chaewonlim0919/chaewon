import cv2
import numpy as np

# ============================= Perspective Transformer =============================
class PerspectiveTransformer:
    def __init__(self, src_points, dst_points):
        self.src_points = np.float32(src_points)
        self.dst_points = np.float32(dst_points)
        self.transform_matrix = cv2.getPerspectiveTransform(self.src_points, self.dst_points)
        self.inverse_transform_matrix = cv2.getPerspectiveTransform(self.dst_points, self.src_points)

    def perspective_transform(self, image):
        print("====================Perspective Transformer=================")
        bird_eye_view = cv2.warpPerspective(image, self.transform_matrix, (image.shape[1], image.shape[0]))
        print(type(bird_eye_view)) # numpy.ndarray
        print({bird_eye_view.shape}) # {(480, 640)}
        return bird_eye_view

    def inverse_perspective_transform(self, image):
        origin_view = cv2.warpPerspective(image, self.inverse_transform_matrix, (image.shape[1], image.shape[0]))
        return origin_view 

    def apply_lane_roi(self, image):

        height, width = image.shape[:2]
        vertices = np.array([[
            (int(width * 0.1), height),
            (int(width * 0.25), int(height * 0.3)),
            (int(width * 0.75), int(height * 0.3)),
            (int(width * 0.9), height)
        ]], dtype=np.int32)

        mask = np.zeros_like(image)
        cv2.fillPoly(mask, vertices, 255)
        return cv2.bitwise_and(image, mask)
