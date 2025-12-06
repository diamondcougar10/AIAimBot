import sys

with open('gameSelection.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the region calculation to ensure proper alignment
old_code = '''    # Ensure the capture region is dynamically calculated based on the monitor resolution
    screenWidth, screenHeight = pyautogui.size()
    screenCenterX = screenWidth // 2
    screenCenterY = screenHeight // 2
    left = screenCenterX - (screenShotWidth // 2)
    top = screenCenterY - (screenShotHeight // 2)
    right = left + screenShotWidth
    bottom = top + screenShotHeight

    # Validate and adjust the region if needed
    if left < 0 or top < 0 or right > screenWidth or bottom > screenHeight:
        print(f"Invalid region detected ({left}, {top}, {right}, {bottom}). Adjusting...")
        left = max(0, left)
        top = max(0, top)
        right = min(screenWidth, right)
        bottom = min(screenHeight, bottom)
    region = (left, top, right, bottom)'''

new_code = '''    # Ensure the capture region is dynamically calculated based on the monitor resolution
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
    
    region = (left, top, right, bottom)'''

content = content.replace(old_code, new_code)

# Also update the cWidth and cHeight calculation
old_calc = '''    # Calculating the center of the auto-aim box
    cWidth: int = screenShotWidth // 2
    cHeight: int = screenShotHeight // 2
    print(f"Region dimensions validated: cWidth={cWidth}, cHeight={cHeight}")'''

new_calc = '''    # Calculating the center of the auto-aim box using actual region dimensions
    actual_width = right - left
    actual_height = bottom - top
    cWidth: int = actual_width // 2
    cHeight: int = actual_height // 2
    print(f"Region dimensions validated: Width={actual_width}, Height={actual_height}, cWidth={cWidth}, cHeight={cHeight}")'''

content = content.replace(old_calc, new_calc)

with open('gameSelection.py', 'w', encoding='utf-8') as f:
    f.write(content)
    
print('gameSelection.py has been fixed to align capture region for YOLOv5!')
