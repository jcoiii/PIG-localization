from pypylon import pylon
import cv2
import numpy as np
import time

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

# image capture resolution
camera.Width.SetValue(1600)
camera.Height.SetValue(1200)
camera.PixelFormat.SetValue('BayerRG8')

# converter object
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

# Initialize variables for FPS calculation
frame_count = 0
t0 = time.time()

while camera.IsGrabbing():
    grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grab_result.GrabSucceeded():
        # Convert the image to OpenCV format
        image = converter.Convert(grab_result)
        img_array = image.GetArray()

        # Resize for display
        display_img = cv2.resize(img_array, (800, 600))  # Adjust this based on your needs

        # Calculate FPS
        frame_count += 1
        elapsed_time = time.time() - t0
        fps = frame_count / elapsed_time

        # Display FPS on the image
        cv2.putText(display_img, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the image
        cv2.imshow('Live Preview', display_img)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    grab_result.Release()

# Release resources
cv2.destroyAllWindows()
camera.Close()
