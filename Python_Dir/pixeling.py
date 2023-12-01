from pypylon import pylon
import cv2
import numpy as np

# Create an instant camera object with the camera device found first.
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

# Get the available pixel formats
pixel_formats = camera.PixelFormat.GetSymbolics()

print("Available Pixel Formats:", pixel_formats)

camera.Close()