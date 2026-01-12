import pyautogui
import os

output_path = os.path.abspath("debug_screen.png")
print(f"Saving screenshot to: {output_path}")

try:
    screenshot = pyautogui.screenshot()
    screenshot.save(output_path)
    print("Screenshot saved successfully.")
except Exception as e:
    print(f"Screenshot failed: {e}")
