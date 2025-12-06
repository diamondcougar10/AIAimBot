import pygetwindow
import pyautogui
import time
import bettercam
from typing import Union
from config import screenShotHeight, screenShotWidth


def gameSelection() -> (bettercam.BetterCam, int, Union[int, None]):
    # Selecting the correct game window
    try:
        videoGameWindows = pygetwindow.getAllWindows()
        print("=== All Windows ===")
        for index, window in enumerate(videoGameWindows):
            # Only output the window if it has a meaningful title
            if window.title != "":
                print(f"[{index}]: {window.title}")
        # Have the user select the window they want
        try:
            userInput = int(input("Please enter the number corresponding to the window you'd like to select: "))
        except ValueError:
            print("You didn't enter a valid number. Please try again.")
            return None
        # "Save" that window as the chosen window for the rest of the script
        videoGameWindow = videoGameWindows[userInput]
    except Exception as e:
        print(f"Failed to select game window: {e}")
        return None

    # Activate that Window
    activationRetries = 30
    activationSuccess = False
    while activationRetries > 0:
        try:
            videoGameWindow.activate()
            activationSuccess = True
            break
        except pygetwindow.PyGetWindowException as we:
            print(f"Failed to activate game window: {str(we)}")
            print("Trying again... (you should switch to the game now)")
        except Exception as e:
            print(f"Failed to activate game window: {str(e)}")
            print("Read the relevant restrictions here: https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setforegroundwindow")
            activationSuccess = False
            activationRetries = 0
            break
        # Wait a little bit before the next try
        time.sleep(3.0)
        activationRetries -= 1

    # If we failed to activate the window, then exit the script now
    if not activationSuccess:
        return None
    print("Successfully activated the game window...")

    # Ensure the capture region is dynamically calculated based on the monitor resolution
    screenWidth, screenHeight = pyautogui.size()
    screenCenterX = screenWidth // 2
    screenCenterY = screenHeight // 2
    
    # Ensure dimensions are divisible by 32 for YOLOv5
    screenShotWidth_aligned = (screenShotWidth // 32) * 32
    screenShotHeight_aligned = (screenShotHeight // 32) * 32
    
    left = screenCenterX - (screenShotWidth_aligned // 2)
    top = screenCenterY - (screenShotHeight_aligned // 2)
    right = left + screenShotWidth_aligned
    bottom = top + screenShotHeight_aligned

    # Validate and adjust the region if needed
    if left < 0 or top < 0 or right > screenWidth or bottom > screenHeight:
        print(f"Invalid region detected ({left}, {top}, {right}, {bottom}). Adjusting...")
        left = max(0, left)
        top = max(0, top)
        right = min(screenWidth, right)
        bottom = min(screenHeight, bottom)
    
    # Final check to ensure width and height are divisible by 32
    width = right - left
    height = bottom - top
    width = (width // 32) * 32
    height = (height // 32) * 32
    right = left + width
    bottom = top + height
    
    region = (left, top, right, bottom)

    print(f"Final capture region: {region}")

    # Calculating the center of the auto-aim box using actual region dimensions
    actual_width = right - left
    actual_height = bottom - top
    cWidth: int = actual_width // 2
    cHeight: int = actual_height // 2
    print(f"Region dimensions validated: Width={actual_width}, Height={actual_height}, cWidth={cWidth}, cHeight={cHeight}")

    try:
        camera = bettercam.create(region=region, output_color="BGRA", max_buffer_len=512)
        if camera is None:
            print("Your Camera Failed! Ask @Wonder for help in our Discord in the #ai-aimbot channel ONLY: https://discord.gg/rootkitorg")
            return None
        camera.start(target_fps=120, video_mode=True)
    except Exception as e:
        print(f"Error initializing camera: {e}")
        return None

    return camera, cWidth, cHeight
