from pypylon import pylon
import cv2
import numpy as np
import time

# Initialize camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()
camera.Width.SetValue(1600)
camera.Height.SetValue(1200)
camera.PixelFormat.SetValue('BayerRG8')

# Image conversion setup
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

# FPS counter initialization
frame_count = 0
t0 = time.time()

# Start capturing images
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
while camera.IsGrabbing():
    grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grab_result.GrabSucceeded():
        # Convert to usable image format
        image = converter.Convert(grab_result)
        img_array = image.GetArray()
        display_img = cv2.resize(img_array, (800, 600))

        # Convert image to HSV
        hsv = cv2.cvtColor(display_img, cv2.COLOR_BGR2HSV)
        lower_orange = np.array([5, 100, 100])
        upper_orange = np.array([20, 255, 255])
        mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

        # Find contours
        contours, _ = cv2.findContours(mask_orange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Draw bounding boxes and display dimensions
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)

            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(display_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                text = f"W: {w}px, H: {h}px, Area: {w * h}px^2"
                cv2.putText(display_img, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Calculate and display FPS
        frame_count += 1
        elapsed_time = time.time() - t0
        fps = frame_count / elapsed_time
        cv2.putText(display_img, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show live preview
        cv2.imshow('Live Preview', display_img)

        # Break on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    grab_result.Release()

cv2.destroyAllWindows()
camera.Close()
