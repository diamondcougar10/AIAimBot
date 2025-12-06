import onnxruntime as ort
import numpy as np
import cv2
import time
import win32api
import torch
from utils.general import non_max_suppression
from config import (
    aaMovementAmp, useMask, maskSide, maskHeight, maskWidth, aaQuitKey, confidence,
    headshot_mode, cpsDisplay, visuals, onnxChoice, centerOfScreen
)
import gameSelection


def apply_mask(image):
    """
    Applies a mask to the image to exclude certain areas, useful for third-person games.
    The mask is applied to the bottom-left corner of the screen.
    """
    if useMask:
        height, width = image.shape[:2]  # Get image dimensions
        if maskSide.lower() == "right":
            # Mask bottom-right corner
            image[height - maskHeight :, width - maskWidth :] = 0
        elif maskSide.lower() == "left":
            # Mask bottom-left corner
            image[height - maskHeight :, :maskWidth] = 0
    return image


def preprocess_image(image):
    """
    Preprocess the image for ONNX model inference.
    - Resizes to (320, 320)
    - Converts to RGB
    - Normalizes and converts to float16
    """
    image = cv2.resize(image, (320, 320))  # Resize to model input dimensions
    image = image[:, :, :3]  # Ensure it has 3 channels (RGB)
    image = image / 255.0  # Normalize pixel values to [0, 1]
    image = np.moveaxis(image, -1, 0)  # Convert to channels-first format (C, H, W)
    return image.astype(np.float16)  # Ensure float16 data type


def move_mouse_to_target(target, region, crosshair_offset=(30, -50)):
    """
    Moves the mouse to the target's absolute position based on the capture region and crosshair offset.

    Args:
        target: Dictionary containing target coordinates within the region.
        region: The capture region of the screen (left, top, right, bottom).
        crosshair_offset: Offset for third-person crosshair (x_offset, y_offset).
    """
    xMid, yMid = target["current_mid_x"], target["current_mid_y"]
    region_left, region_top, _, _ = region

    # Apply crosshair offset to align the aim with the third-person crosshair
    xMid += crosshair_offset[0]
    yMid += crosshair_offset[1]

    # Calculate absolute coordinates for the mouse
    absolute_x = int(region_left + xMid)
    absolute_y = int(region_top + yMid)

    # Debugging info
    print(f"Target Coords (Region): xMid={xMid}, yMid={yMid}")
    print(f"Calculated Absolute Position: x={absolute_x}, y={absolute_y}")

    # Move the mouse directly to the calculated absolute position
    win32api.SetCursorPos((absolute_x, absolute_y))


def process_predictions(outputs, region, npImg, exclusion_zone_radius=100):
    """
    Process the predictions from the model and move the mouse to a valid target.
    Excludes targets within the exclusion zone around the screen center.

    Args:
        outputs: Model output.
        region: The capture region of the screen (left, top, right, bottom).
        npImg: The image frame for drawing visuals.
        exclusion_zone_radius: Radius around the screen center to exclude targets.
    """
    predictions = torch.from_numpy(outputs[0]).to('cpu')  # Convert outputs to tensor
    pred = non_max_suppression(predictions, confidence, confidence, 0, False, max_det=10)

    if pred is not None and len(pred) > 0:
        targets = []
        for det in pred:
            for *xyxy, conf, cls in reversed(det):
                x_mid = (xyxy[0].item() + xyxy[2].item()) / 2
                y_mid = (xyxy[1].item() + xyxy[3].item()) / 2
                targets.append({
                    "current_mid_x": x_mid,
                    "current_mid_y": y_mid,
                    "confidence": conf.item(),
                    "xyxy": [int(x) for x in xyxy]  # For drawing boxes
                })

        if targets:
            # Screen center coordinates
            center_x = (region[2] - region[0]) / 2
            center_y = (region[3] - region[1]) / 2

            # Filter out targets within the exclusion zone
            filtered_targets = [
                t for t in targets if ((t["current_mid_x"] - center_x)**2 + (t["current_mid_y"] - center_y)**2) > exclusion_zone_radius**2
            ]

            if filtered_targets:
                # Sort by proximity to the center
                filtered_targets = sorted(
                    filtered_targets,
                    key=lambda t: abs(t["current_mid_x"] - center_x) + abs(t["current_mid_y"] - center_y)
                )

                # Move to the closest target
                move_mouse_to_target(filtered_targets[0], region)

                # Visualize targets if enabled
                if visuals:
                    for t in filtered_targets:
                        x_min, y_min, x_max, y_max = t["xyxy"]
                        cv2.rectangle(npImg, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                        label = f"Conf: {t['confidence']:.2f}"
                        cv2.putText(npImg, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


def main():
    # Run game selection and get the region
    result = gameSelection.gameSelection()
    if result is None:
        print("Failed to initialize the game window or camera. Exiting...")
        return
    camera, cWidth, cHeight = result
    region = camera.region  # Use the region directly from `gameSelection`

    # Choosing the correct ONNX Provider based on config.py
    onnxProvider = ""
    if onnxChoice == 1:
        onnxProvider = "CPUExecutionProvider"
    elif onnxChoice == 2:
        onnxProvider = "DmlExecutionProvider"
    elif onnxChoice == 3:
        import cupy as cp
        onnxProvider = "CUDAExecutionProvider"

    so = ort.SessionOptions()
    so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    ort_sess = ort.InferenceSession('yolov5s320Half.onnx', sess_options=so, providers=[onnxProvider])

    # Main loop
    while win32api.GetAsyncKeyState(ord(aaQuitKey)) == 0:
        # Capture frame
        npImg = np.array(camera.get_latest_frame())

        # Apply mask
        npImg = apply_mask(npImg)

        # Preprocess image
        im = preprocess_image(npImg)

        # Inference
        outputs = ort_sess.run(None, {'images': im[None]})

        # Process predictions
        process_predictions(outputs, region, npImg, exclusion_zone_radius=100)

        # Display visuals if enabled
        if visuals:
            cv2.imshow("Live Feed", npImg)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    camera.stop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exception(e)
        print("ERROR:", str(e))


# import onnxruntime as ort
# import numpy as np
# import gc
# import cv2
# import time
# import win32api
# import win32con
# import pandas as pd
# from utils.general import (cv2, non_max_suppression, xyxy2xywh)
# import torch

# # Could be do with
# # from config import *
# # But we are writing it out for clarity for new devs
# from config import aaMovementAmp, useMask, maskHeight, maskWidth, aaQuitKey, confidence, headshot_mode, cpsDisplay, visuals, onnxChoice, centerOfScreen
# import gameSelection

# def apply_red_filter(image):
#     # Convert the image to HSV color space
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # Define the lower and upper bounds for dark red color in HSV
#     lower_dark_red1 = np.array([0, 70, 30])   # Adjusted for lower brightness
#     upper_dark_red1 = np.array([10, 255, 100])

#     lower_dark_red2 = np.array([170, 70, 30]) # Upper hue range for dark red
#     upper_dark_red2 = np.array([180, 255, 100])

#     # Create a mask for dark red color
#     mask1 = cv2.inRange(hsv, lower_dark_red1, upper_dark_red1)
#     mask2 = cv2.inRange(hsv, lower_dark_red2, upper_dark_red2)
#     dark_red_mask = cv2.bitwise_or(mask1, mask2)

#     # Apply the mask to the original image
#     filtered_image = cv2.bitwise_and(image, image, mask=dark_red_mask)
#     return filtered_image


#     # Apply the red mask to the original image
#     filtered_image = cv2.bitwise_and(image, image, mask=red_mask)
#     return filtered_image

# def main():
#     # External Function for running the game selection menu (gameSelection.py)
#     camera, cWidth, cHeight = gameSelection.gameSelection()

#     # Used for forcing garbage collection
#     count = 0
#     sTime = time.time()

#     # Choosing the correct ONNX Provider based on config.py
#     onnxProvider = ""
#     if onnxChoice == 1:
#         onnxProvider = "CPUExecutionProvider"
#     elif onnxChoice == 2:
#         onnxProvider = "DmlExecutionProvider"
#     elif onnxChoice == 3:
#         import cupy as cp
#         onnxProvider = "CUDAExecutionProvider"

#     so = ort.SessionOptions()
#     so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
#     ort_sess = ort.InferenceSession('yolov5s320Half.onnx', sess_options=so, providers=[
#                                     onnxProvider])

#     # Used for colors drawn on bounding boxes
#     COLORS = np.random.uniform(0, 255, size=(1500, 3))

#     # Main loop Quit if Q is pressed
#     last_mid_coord = None
#     while win32api.GetAsyncKeyState(ord(aaQuitKey)) == 0:

#         # Getting Frame
#         npImg = np.array(camera.get_latest_frame())
#         npImg = cv2.resize(npImg, (320, 320))

#         # Apply red filter to isolate enemies
#         npImg = apply_red_filter(npImg)

#         from config import maskSide # "temporary" workaround for bad syntax
#         if useMask:
#             maskSide = maskSide.lower()
#             if maskSide == "right":
#                 npImg[-maskHeight:, -maskWidth:, :] = 0
#             elif maskSide == "left":
#                 npImg[-maskHeight:, :maskWidth, :] = 0
#             else:
#                 raise Exception('ERROR: Invalid maskSide! Please use "left" or "right"')

#         # If Nvidia, do this
#         if onnxChoice == 3:
#             # Normalizing Data
#             im = torch.from_numpy(npImg).to('cuda')
#             if im.shape[2] == 4:
#                 # If the image has an alpha channel, remove it
#                 im = im[:, :, :3,]

#             im = torch.movedim(im, 2, 0)
#             im = im.half()
#             im /= 255
#             if len(im.shape) == 3:
#                 im = im[None]
#         # If AMD or CPU, do this
#         else:
#             # Normalizing Data
#             im = np.array([npImg])
#             if im.shape[3] == 4:
#                 # If the image has an alpha channel, remove it
#                 im = im[:, :, :, :3]
#             im = im / 255
#             im = im.astype(np.half)
#             im = np.moveaxis(im, 3, 1)

#         # Run inference
#         if onnxChoice == 3:
#             outputs = ort_sess.run(None, {'images': cp.asnumpy(im)})
#         else:
#             outputs = ort_sess.run(None, {'images': np.array(im)})

#         im = torch.from_numpy(outputs[0]).to('cpu')

#         pred = non_max_suppression(
#             im, confidence, confidence, 0, False, max_det=10)

#         targets = []
#         for i, det in enumerate(pred):
#             if len(det):
#                 for *xyxy, conf, cls in reversed(det):
#                     x_min, y_min, x_max, y_max = map(int, xyxy)

#                     # Ensure bounding box is within the image
#                     x_min = max(0, x_min)
#                     y_min = max(0, y_min)
#                     x_max = min(npImg.shape[1], x_max)
#                     y_max = min(npImg.shape[0], y_max)

#                     cropped_region = npImg[y_min:y_max, x_min:x_max]

#                     # Check the average red intensity in the region
#                     avg_red = np.mean(cropped_region[:, :, 2])  # Red channel
#                     avg_blue = np.mean(cropped_region[:, :, 0])  # Blue channel

#                     # Only keep predictions with significant red dominance
#                     if avg_red > avg_blue * 1.5:  # Adjust multiplier as needed
#                         targets.append({
#                             "xyxy": (x_min, y_min, x_max, y_max),
#                             "conf": float(conf),
#                         })

#         # Process targets
#         if targets:
#             targets_df = pd.DataFrame([
#                 {
#                     "current_mid_x": (target["xyxy"][0] + target["xyxy"][2]) / 2,
#                     "current_mid_y": (target["xyxy"][1] + target["xyxy"][3]) / 2,
#                     "width": target["xyxy"][2] - target["xyxy"][0],
#                     "height": target["xyxy"][3] - target["xyxy"][1],
#                     "confidence": target["conf"],
#                 }
#                 for target in targets
#             ])
#         else:
#             targets_df = pd.DataFrame(columns=['current_mid_x', 'current_mid_y', 'width', "height", "confidence"])

#         center_screen = [cWidth, cHeight]

#         # If there are targets
#         if len(targets_df) > 0:
#             if centerOfScreen:
#                 # Compute distance from the center
#                 targets_df["dist_from_center"] = np.sqrt(
#                     (targets_df.current_mid_x - center_screen[0])**2 +
#                     (targets_df.current_mid_y - center_screen[1])**2
#                 )
#                 # Sort targets by distance from the center
#                 targets_df = targets_df.sort_values("dist_from_center")

#             # Get the closest target's midpoint
#             xMid = targets_df.iloc[0].current_mid_x
#             yMid = targets_df.iloc[0].current_mid_y

#             box_height = targets_df.iloc[0].height
#             headshot_offset = box_height * (0.38 if headshot_mode else 0.2)

#             mouseMove = [xMid - cWidth, (yMid - headshot_offset) - cHeight]

#             # Move the mouse
#             if win32api.GetKeyState(0x14):  # Check CAPS_LOCK state
#                 win32api.mouse_event(
#                     win32con.MOUSEEVENTF_MOVE,
#                     int(mouseMove[0] * aaMovementAmp),
#                     int(mouseMove[1] * aaMovementAmp),
#                     0, 0
#                 )
#             last_mid_coord = [xMid, yMid]
#         else:
#             last_mid_coord = None

#         # Visualize results
#         if visuals:
#             for target in targets:
#                 x_min, y_min, x_max, y_max = target["xyxy"]
#                 cv2.rectangle(npImg, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

#             cv2.imshow('Filtered Targets', npImg)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         # Forced garbage cleanup every second
#         count += 1
#         if (time.time() - sTime) > 1:
#             if cpsDisplay:
#                 print("CPS: {}".format(count))
#             count = 0
#             sTime = time.time()

#     camera.stop()

# if __name__ == "__main__":
#     try:
#         main()
#     except Exception as e:
#         import traceback
#         traceback.print_exception(e)
#         print("ERROR: " + str(e))
#         print("Ask @Wonder for help in our Discord in the #ai-aimbot channel ONLY: https://discord.gg/rootkitorg")         