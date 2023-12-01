import cv2

# Create a VideoCapture object
cap = cv2.VideoCapture("rtsp://192.168.1.1:554/user=admin&password=&channel=1&stream=0.sdp")

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Failed to open camera.")
    exit()

# Capture frames from the camera
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Check if the frame is successfully read
    if not ret:
        print("Failed to grab frame.")
        break

    # Display the frame
    cv2.imshow('GigE Camera', frame)

    # Wait for a key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()