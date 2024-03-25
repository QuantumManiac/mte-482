import cv2
import math
from pyzbar.pyzbar import decode
import time
import zmq
import json


SHOW_VIDEO = False
ZMQ_PUB = "tcp://172.20.10.4:5556"


def calculate_angle(p1, p2):
    # Calculate the angle in degrees between two points (p1 and p2) and the x-axis
    return math.degrees(math.atan2(-(p2[1] - p1[1]), p2[0] - p1[0]))  # Make rise negative, as y axis is inversed in cv2

def process_frame(frame, qr):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect QR codes in the frame
    decoded_objects = decode(gray)

    if not decoded_objects:
        return None, None, None, None
    qr_data = decoded_objects[0].data.decode().split(',')
    pos_x = qr_data[0]
    pos_y = qr_data[1]
    
    ret_qr, rect_points = qr.detect(frame)
    if not ret_qr or rect_points is [[]]:
        return None, None, None, None
    rect_points = rect_points[0]  # remove outer list

    # Extract the top edge coordinates
    top_left, top_right, bot_right, bot_left = rect_points[0], rect_points[1], rect_points[2], rect_points[3]

    if SHOW_VIDEO:
        # # Draw only the top edge
        cv2.putText(frame, "0", tuple(map(int, top_left)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,0,0), thickness=2)
        cv2.putText(frame, "1", tuple(map(int, bot_left)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,0,0), thickness=2)
        cv2.putText(frame, "2", tuple(map(int, bot_right)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,0,0), thickness=2)
        cv2.putText(frame, "3", tuple(map(int, top_right)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,0,0), thickness=2)

        cv2.line(frame, tuple(map(int, top_left)), tuple(map(int, top_right)), (0, 255, 0), 5)

    # Calculate the angle of the top edge with respect to the x-axis
    qr_angle = calculate_angle(top_left, top_right)
    cart_angle = 90 - qr_angle
    if cart_angle > 180:
        cart_angle = -(qr_angle+180)  # make it 0 -> +-180

    return frame, pos_x, pos_y, cart_angle


if __name__ == "__main__":
    # Setup interprocess communication 
    context = zmq.Context()
    pub = context.socket(zmq.PUB)
    pub.connect(ZMQ_PUB)

    # Set runtime parameters
    FRAME_RATE = 15

    # Start capturing video from the default camera (index 0)
    cap = cv2.VideoCapture(0)
    qr = cv2.QRCodeDetector()

    if not cap.isOpened():
        print("Error: Couldn't open video stream")
        exit()

    prev = 0
    print("Camera started successfully")
    processed_frame = None
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Couldn't capture frame")
            break

        # Process the frame
        time_elapsed = time.time() - prev
        if time_elapsed >= (1/FRAME_RATE):
            prev = time.time()
            try:
                processed_frame, pos_x, pos_y, angle = process_frame(frame, qr)
                print(f"pos_x: {pos_x}, pos_y: {pos_y}, angle: {angle}")
                # Publish the resulting position and angle
                if (pos_x is not None) and (pos_y is not None) and (angle is not None):
                    msg = {
                        "pos_x": float(pos_x),
                        "pos_y": float(pos_y),
                        "angle": float(angle)
                    }
                    pub.send_string(f"qr {json.dumps(msg)}")
                    print(f"angle: {angle} position: {pos_x} {pos_y}")
            except Exception as e:  # Sometimes the camera hallucinates QR codes when there are none, this prevents crashing
                print(f"Some camera exception: {e}, continuing")
                continue


        # Display the processed frame
        if processed_frame is not None and SHOW_VIDEO:
            cv2.imshow("Processed Frame", processed_frame)

        # Check for 'q' key press to exit the loop
        if cv2.waitKey(int(1000/FRAME_RATE)) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()
