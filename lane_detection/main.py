import cv2
from camera import Camera
from control import PurePursuitController
from hardware import MotorController
from lane_detection.line_detection import LaneDetectionPipeline

def main():
    camera = Camera()
    controller = PurePursuitController()
    motor = MotorController()
    
    src = [[100, 480], [540, 480], [200, 200], [440, 200]]
    dst = [[200, 480], [440, 480], [200, 0], [440, 0]]
    
    lane_detector = LaneDetectionPipeline(src, dst)
    
    while True:
        frame = camera.get_frame()
        if frame is None:
            break
        
        detected_frame = lane_detector.process_frame(frame)
        
        left_fitx, right_fitx = lane_detector.lane_fitter.fit_side_lane_polynomial(
            detected_frame, lane_detector.lane_detector.left_lane_x, lane_detector.lane_detector.left_lane_y,
            lane_detector.lane_detector.right_lane_x, lane_detector.lane_detector.right_lane_y
        )
        
        look_ahead_x = (left_fitx[-1] + right_fitx[-1]) / 2
        look_ahead_y = frame.shape[0] - 100
        steering_angle = controller.calculate_steering((320, 480), 0, (look_ahead_x, look_ahead_y))
        
        print(f"Steering Angle: {steering_angle:.2f} degrees")
        motor.send_command(50, steering_angle)
        
        cv2.imshow("Lane Detection", detected_frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    camera.release()
    motor.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
