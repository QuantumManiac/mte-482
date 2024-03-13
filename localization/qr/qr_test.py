import cv2
import math
from pyzbar.pyzbar import decode

def calculate_angle(p1, p2):
    # Calculate the angle in degrees between two points (p1 and p2) and the x-axis
    return math.degrees(math.atan2(-(p2[1] - p1[1]), p2[0] - p1[0]))  # Make rise negative, as y axis is inversed in cv2

def process_frame(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect QR codes in the frame
    decoded_objects = decode(gray)

    if not decoded_objects:
        return None, None

    # Get the first QR code found
    qr_code = decoded_objects[0]

    # Extract the top edge coordinates
    rect_points = qr_code.polygon
    top_left, bot_left, bot_right, top_right = rect_points[0], rect_points[1], rect_points[2], rect_points[3] 

    # Draw only the top edge
    cv2.putText(frame, "0", tuple(top_left), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,0,0), thickness=2)
    cv2.putText(frame, "1", tuple(bot_left), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,0,0), thickness=2)
    cv2.putText(frame, "2", tuple(bot_right), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,0,0), thickness=2)
    cv2.putText(frame, "3", tuple(top_right), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,0,0), thickness=2)

    cv2.line(frame, tuple(top_left), tuple(top_right), (0, 255, 0), 5)
    cv2.drawMarker(frame, (qr_code.rect.left, qr_code.rect.top), (0,255,0), cv2.MARKER_CROSS, 10, 5)

    # Calculate the angle of the top edge with respect to the x-axis
    angle = calculate_angle(top_left, top_right)
    position = qr_code.data.decode()
    # print(f"angle: {angle} position: {position}")
    # print(qr_code.rect.left)

    return frame, angle

if __name__ == "__main__":
    # Start capturing video from the default camera (index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Couldn't open video stream")
        exit()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Couldn't capture frame")
            break

        # Process the frame
        processed_frame, angle = process_frame(frame)

        # Display the processed frame
        if processed_frame is not None:
            cv2.imshow("Processed Frame", processed_frame)

        # Check for 'q' key press to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()
