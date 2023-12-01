import cv2
import numpy as np
import pypylon.pylon as py
import time

camera = py.InstantCamera(py.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()
camera.Width.SetValue(800)
camera.Height.SetValue(600)
camera.PixelFormat.SetValue('BayerRG8')
camera.StartGrabbing(py.GrabStrategy_LatestImageOnly)

# For FPS calculation
prev_frame_time = 0

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, py.TimeoutHandling_ThrowException)
    if grabResult.GrabSucceeded():
        # Convert to OpenCV image format
        img = cv2.cvtColor(grabResult.Array, cv2.COLOR_BGR2RGB)
        
        # Convert the image to HSV format
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        # Define range for red color
        lower_red = np.array([0, 120, 50])
        upper_red = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        lower_red = np.array([170, 120, 50])
        upper_red = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red, upper_red)
        
        mask = mask1 + mask2
        
        # Morphological operations to reduce noise
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Finding contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw the contours
        for contour in contours:
            # Ensure contour is sufficiently large
            if cv2.contourArea(contour) > 20:
                (x, y), radius = cv2.minEnclosingCircle(contour)
                center = (int(x), int(y))
                radius = int(radius)
                cv2.circle(img, center, radius, (0, 255, 0), 2)
                cv2.putText(img, f"Coord: {center}", (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # FPS calculation
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        cv2.putText(img, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Show the image
        cv2.imshow('Live View', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    grabResult.Release()

camera.StopGrabbing()
cv2.destroyAllWindows()
