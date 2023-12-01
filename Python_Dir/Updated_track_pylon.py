from pypylon import pylon
import cv2
import numpy as np
import time

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()
camera.Width.SetValue(1600)
camera.Height.SetValue(1200)
camera.PixelFormat.SetValue('BayerRG8')

converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

frame_count = 0
t0 = time.time()

camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
while camera.IsGrabbing():
    grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grab_result.GrabSucceeded():
        image = converter.Convert(grab_result)
        img_array = image.GetArray()
        display_img = cv2.resize(img_array, (800, 600))
        
        hsv = cv2.cvtColor(display_img, cv2.COLOR_BGR2HSV)
        lower_orange = np.array([10, 100, 100])
        upper_orange = np.array([25, 255, 255])
        mask = cv2.inRange(hsv, lower_orange, upper_orange)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rect_center = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)

            if len(approx) == 4:
                cv2.drawContours(display_img, [approx], 0, (0, 255, 0), 5)
                x, y, w, h = cv2.boundingRect(contour)
                rect_center = (x + w // 2, y + h // 2)
                cv2.rectangle(display_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if rect_center:
            cv2.putText(display_img, f"Coord: {rect_center}", (500, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


        frame_count += 1
        elapsed_time = time.time() - t0
        fps = frame_count / elapsed_time
        cv2.putText(display_img, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Live Preview', display_img)

        # q --> break loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    grab_result.Release()

cv2.destroyAllWindows()
camera.Close()
