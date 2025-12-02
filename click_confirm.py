# IMPORTANT PROJECT RULE:
# Do NOT modify existing print statements or comments.
# Only add new prints or comments if absolutely necessary.

import os, pyautogui, time, threading, random, sys, cv2
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS


load_dotenv()



# =========================
# Image Path Helpers (for running on multiple systems with different resolutions, colors, fonts, etc)
# =========================

# Get current file path
IMG_DIR = os.getcwd()

# Update file path based on keywords defined for each system, based on what's defined in .env
if os.getenv('FILE_PATH_1_KEYWORD') in IMG_DIR:
    IMG_DIR = os.getenv('FILE_PATH_1')
elif os.getenv('FILE_PATH_2_KEYWORD') in IMG_DIR:
    IMG_DIR = os.getenv('FILE_PATH_2')
elif os.getenv('FILE_PATH_3_KEYWORD') in IMG_DIR:
    IMG_DIR = os.getenv('FILE_PATH_3')


# Helper function to get full path to an image file
def image(name):
    return str(IMG_DIR + "/" + name)


# Universal Constants
CONFIDENCE = 0.9
OFFSET_X = -1

# kill switch initiation
KILL_SWITCH_PATH = os.path.join(os.path.dirname(__file__), "kill_switch.txt")
def kill_switch_active():
    if os.path.exists(KILL_SWITCH_PATH):
        print("Kill switch activated")
        return True
    else:
        return False


# Timing Constants
#TIME_BETWEEN_SWAPS = 25 #seconds, minimum time between swaps
#VARIANCE_TIME = 55 #seconds, used to extend and randomize time between swaps
INTERVAL = 0.15 #seconds, used to time keystrokes
STEP_DELAY = 1.5 #seconds, used to add time between actions
SLEEP_TIME = 20 #seconds, used to pause between certain steps
TIMEOUT = 10  #seconds, used to time out page loads and such
MAX_ATTEMPTS = 15
MAX_SWAP_DURATION = 30  # seconds before we give up on a swap cycle
MAX_REFRESH_ATTEMPTS = 5




#image assets
CONFIRM_IMAGES = [image("phantom_confirm.png"), image("phantom_confirm2.png")]
PHANTOM_ERROR_IMAGES = [image("phantom_slippage.png"), image("ur_broke.png"), image("phantom_simulation.png"), image("phantom_blocked.png")]
PHANTOM_CANCEL_IMAGES = [image("phantom_cancel.png"),image("phantom_close.png"),image("phantom_cancel2.png")]
PHANTOM_UNLOCK = image("extension_unlock.png")

# =========================
# User Config (editable)
# =========================
USER_CONFIG = {
    "log-level" : "INFO"            # choose from: "DEBUG", "INFO", "WARN", "ERROR"
}




# ================================
# ScreenHelper Class
# +Finds and clicks things
# +Calculates resolution and scaling
# ================================

class ScreenHelper:
    """
    Handles screen-related operations like locating and clicking images, refreshing the page.
    Uses global constants: CONFIDENCE, OFFSET_X
    """

    def __init__(self, confidence=CONFIDENCE, offset_x=OFFSET_X,region=None, interval=INTERVAL, step_delay=STEP_DELAY):
        # Pull in universal constants
        self.confidence = confidence
        self.offset_x = offset_x
        self.interval = interval
        self.step_delay = step_delay

        # Configure scaling and physical dimensions
        self.scaling_factor, self.physical_width, self.physical_height = self.detect_scaling_factor()
        
        # Define region = full screen (always safe ints)
        self.default_region = (0, 0, self.physical_width, self.physical_height)
        
        # Allow override region, else use default
        if region is None:
            self.region = self.default_region
        else:
            # sanitize user-provided region to integers
            self.region = tuple(map(int, region))
        
        self.excluded_regions = []  # list of (x1, y1, x2, y2) tuples
        Logger.debug(f"[INIT] ScreenHelper initialized. Scaling={self.scaling_factor}, Region={self.region}, Screen={self.physical_width}x{self.physical_height}")

    def detect_scaling_factor(self):
        logical_width, logical_height = pyautogui.size()
        physical_width, physical_height = pyautogui.screenshot().size
        
        scale_x = physical_width / logical_width
        scale_y = physical_height / logical_height
        scaling = round((scale_x + scale_y) / 2, 2)

        Logger.debug(f"Detected scaling factor: {scaling}")
        return scaling, int(physical_width), int(physical_height)

    def cursor_wiggle(self):
        pyautogui.moveRel(random.randint(-9, 9), random.randint(-8, 8), duration=0.10)
        pyautogui.moveRel(random.randint(-8, 8), random.randint(-7, 7), duration=0.05)
        pyautogui.moveRel(random.randint(-6, 6), random.randint(-8, 8), duration=0.08)
        return None

    #returns a Point (x, y)
    def find_center(self, image_path, region=None, apply_scaling=True):
        """
        Safely locates the center of an image on screen.
        Returns a pyautogui.Point or None.
        """
        try:
            # Fallback to default region if none provided
            search_region = self.region if region is None else tuple(map(int, region))
            
            center = pyautogui.locateCenterOnScreen(
                image_path, confidence=self.confidence, region=search_region
            )

            Logger.debug(f"Match result: {center}, confidence={self.confidence}")

            if not center:
                Logger.info(f"[find_center] Image not found: {image_path}")
                return None
            
            if apply_scaling:
                center = pyautogui.Point(
                    int(center.x / self.scaling_factor),
                    int(center.y / self.scaling_factor)
                )
            return center
        
        except pyautogui.ImageNotFoundException:
            Logger.debug(f"{image_path} not found while running find_center()")
            return None
        # except Exception as e:
        #     Logger.error(f"[find_center] Exception: {e}")
        #     return None
        
        except Exception as e:
            Logger.warn(f"Unexpected error in find_center() with {image_path}: {e}")
            return None

    def exclude_region(self, image_path, apply_scaling=True):
        """Locate one or more images on screen and mark their bounding box as excluded.
        - image_path can be a single string or a list of strings.
        Uses scaling correction if requested.
        """

        images = image_path if isinstance(image_path, (list, tuple)) else [image_path]

        for img in images:
            box = pyautogui.locateOnScreen(img, confidence=self.confidence, region=self.region)
            if not box:
                Logger.warn(f"Could not locate {img}, no exclusion region set.")
                continue

            x1, y1, w, h = box
            x2, y2 = x1 + w, y1 + h

            if apply_scaling:
                x1, y1, x2, y2 = [int(v / self.scaling_factor) for v in (x1, y1, x2, y2)]

            self.excluded_regions.append((x1, y1, x2, y2))
            Logger.info(f"Exclusion zone set for {image_path}: {x1},{y1} → {x2},{y2}")
            return
        
    def _is_excluded(self, point):
        """
        Return True if the given (x,y) point is inside any excluded region.
        """
        for (x1, y1, x2, y2) in self.excluded_regions:
            if x1 <= point[0] <= x2 and y1 <= point[1] <= y2:
                Logger.info(f"Point {point} blocked (inside exclusion zone {x1},{y1} → {x2},{y2})")
                return True
        return False

    def clear_excluded_regions(self):
        """Remove all exclusion zones (reset state)."""
        self.excluded_regions = []
        Logger.debug("Cleared all exclusion zones.")

    def click_image(self, image_path, region=None, apply_scaling=True, offset_x=None, offset_y=None):
        """
        Locate and click the center of an image on screen...
        ...unless it falls in an excluded region.
        Supports optional per-click pixel offsets.
        """
        search_region = self.region if region is None else tuple(map(int, region))

        try:
            center = self.find_center(image_path, region=search_region, apply_scaling=apply_scaling)

            if center:
                # Use per-click offset if provided, otherwise fall back to self.offset_x
                x = center.x + (offset_x if offset_x is not None else self.offset_x)
                y = center.y + (offset_y if offset_y is not None else 0)

                # 🔒 Check exclusion zones
                if hasattr(self, "excluded_regions") and self._is_excluded((x, y)):
                    Logger.warn(
                        f"Click on {image_path} blocked (inside excluded region). Skipping click."
                    )
                    time.sleep(self.step_delay)
                    return False

                pyautogui.moveTo(x, y, duration=self.interval)
                self.cursor_wiggle()
                time.sleep(self.step_delay)
                pyautogui.moveTo(x, y, duration=self.interval)
                pyautogui.click()
                return True
            else:
                Logger.debug(f"{image_path} not found on screen while running click_image().")
                return False
        except Exception as e:
            Logger.debug(f"Unexpected error in click_image(): {e}")
            return False

               
# ================================
# Timing Utility Class
# +handles timing, pacing, generating timestamps 
# ================================

class Timing:
    """
    Timing utility for retry loops, randomized delays, and timestamp helpers.
    Replaces Waiter with a minimal, efficient retry system.
    """

    def __init__(self, timeout: int = TIMEOUT, interval: float = INTERVAL, debug: bool = False):
        """
        Args:
            timeout (int): Default max seconds to wait before giving up.
            interval (float): Default interval between attempts.
            debug (bool): Whether to log retry attempts.
        """
        self.timeout = timeout
        self.interval = interval
        self.debug = debug

    def wait_for(self, func, *args, timeout=None, interval=None, debug=None, **kwargs) -> bool:
        """
        Repeatedly calls func until it returns True or timeout is reached.
        """
        timeout = timeout or self.timeout
        interval = interval or self.interval
        debug = self.debug if debug is None else debug

        start = time.time()
        attempt = 0
        while (time.time() - start) < timeout:
            attempt += 1
            try:
                if func(*args, **kwargs):
                    return True
            except Exception as e:
                if debug:
                    Logger.debug(f"Timing: attempt {attempt} raised {e}")
            if debug:
                Logger.debug(f"Timing: attempt {attempt} failed, retrying...")
            time.sleep(interval)

        Logger.warn(f"Timing: condition not met after {timeout}s, giving up.")
        return False

    def get_pacific_time_str(self) -> str:
        """
        Returns a string of the current Pacific Time, formatted for logs.
        """
        pacific = ZoneInfo("America/Los_Angeles")
        return datetime.now(pacific).strftime("%D %m, %I:%M %p")

# ================================
# Logger Class - handles logging
# ================================
class Logger:
    """
    Lightweight logger with basic level support.
    Can later expand to file-writing or GUI output.
    """
    # Define numeric levels (like Python's logging)
    LEVELS = {"DEBUG": 10, "INFO": 20, "WARN": 30, "ERROR": 40}
    
    # Initialize from user config (default to INFO if missing/invalid)
    current_level = LEVELS.get(USER_CONFIG.get("log-level", "INFO").upper(), 20)

    @classmethod
    def _should_log(cls, level_name):
        """Return True if the given level should be logged at current_level"""
        return cls.LEVELS[level_name] >= cls.current_level

    @classmethod
    def set_level(cls, level_name):
        """Change the active logging level"""
        if level_name in cls.LEVELS:
            cls.current_level = cls.LEVELS[level_name]
        else:
            raise ValueError(f"Unknown log level: {level_name}")

    @staticmethod
    def log(msg, level="INFO"):
        now = datetime.now().strftime("%d %b %-I:%M:%S %p")
        print(f"[{now}] {level}: {msg}")

    @classmethod
    def debug(cls, msg):
        if cls._should_log("DEBUG"):
            cls.log(msg, "DEBUG")

    @classmethod
    def info(cls, msg):
        if cls._should_log("INFO"):
            cls.log(msg, "INFO")

    @classmethod
    def warn(cls, msg):
        if cls._should_log("WARN"):
            cls.log(msg, "WARN")

    @classmethod
    def error(cls, msg):
        if cls._should_log("ERROR"):
            cls.log(msg, "ERROR")


# ================================
# SwapFlow Class - runs the swaps
# ================================
class SwapFlow:
    """
    These methods orchestrate the full swap flow using 
    ScreenHelper + Timing classes
    and provided Constants and user settings
    """

    def __init__(self, screen: ScreenHelper, timing: Timing, config: dict):
        """
        Orchestrates swaps using provided config.
        """
        self.screen = screen
        self.timing = timing

    
    def unlock_phantom(self):
        """
        Check if Phantom wallet is locked and wait for user to unlock.
        Returns (success).
        """
        attempts = 0
        max_attempts = 3
        wait_time = SLEEP_TIME     # pause between attempts

        time.sleep(STEP_DELAY)  # short delay after Swap click

        while attempts < max_attempts:
            found = self.screen.find_center(PHANTOM_UNLOCK)
            if found:
                Logger.info("Phantom is locked. Please unlock manually.")
                time.sleep(wait_time)
                attempts += 1
            else:
                Logger.debug("Phantom is unlocked, continuing swap.")
                return True

        Logger.error("Phantom stayed locked after max attempts.")
        return False

    def click_confirm_button(self, max_attempts=MAX_ATTEMPTS, simulate=False):
        """
        Attempt to click the Confirm button in Phantom extension or DEX UI.
        Retries until the button disappears.
        Returns (success).
        """
        if simulate:
            Logger.info("[SIMULATION] Pretending to not see confirm button")
            return False
        
        time.sleep(STEP_DELAY)

        for errorImg in PHANTOM_ERROR_IMAGES:
                if self.screen.find_center(errorImg):
                    Logger.warn(f"Phantom error detected: {errorImg}")
                    Logger.info(f"Looking for phantom error: {errorImg}")
                    
                    #Try to cancel transaction:
                    cancelled = False
                    for cancelImg in PHANTOM_CANCEL_IMAGES:
                        if self.screen.click_image(cancelImg):
                            Logger.info(f"Clicked {cancelImg} button to cancel transaction")
                            time.sleep(STEP_DELAY)
                            cancelled = True
                            break

                    # Wait for confirm button to disappear
                    disappeared = self.timing.wait_for(
                        lambda: not self.screen.find_center(errorImg),
                        timeout=TIMEOUT
                    )

                    if disappeared:
                        Logger.info(f"Phantom error: Canceled tx.")
                        #time.sleep(STEP_DELAY)
                        return True
                    else:
                        #error screen still there
                        Logger.warn(f"{errorImg} still visible after clicking it. ")
                        if cancelled and self.screen.click_image(cancelImg):
                            Logger.info(f"Retry clicking {cancelImg} button")
                            time.sleep(STEP_DELAY)
                            return True
                        return False
                    
                # Logger.debug(f"Confirm attempt {attempt+1}/{max_attempts} failed, retrying...")
                # time.sleep(STEP_DELAY) 

                # If no error message found, continue
                else:
                    continue



        for attempt in range(max_attempts):
            # Look for and click confirm images
            for confirmImg in CONFIRM_IMAGES:
                if self.screen.click_image(confirmImg):
                    #attempt += 1
                    Logger.debug(f"Clicked confirm button")
                    time.sleep(STEP_DELAY)

                    # Wait for confirm button to disappear
                    disappeared = self.timing.wait_for(
                        lambda: not self.screen.find_center(confirmImg, apply_scaling=True),
                        timeout=TIMEOUT
                    )

                    if disappeared:
                        Logger.debug(f"Confirm button is not lurking about")
                        return True
                    else:
                        Logger.warn(f"Confirm button {confirmImg} still visible after timeout. Retrying...")
                        if self.screen.click_image(confirmImg):
                            #attempt += 1
                            Logger.debug(f"Confirm button {confirmImg} clicked")
                            time.sleep(STEP_DELAY)

            
            # If no Confirm button, look for Phantom errors and cancel TX
            
            
        #Exit loop if not able to confirm transaction
        Logger.error(f"Confirm button did not disappear after {max_attempts} attempts.")
        return False


    # === Master orchestration flow -- this is the sauce! ===
    def phantom_clicker(self, delay=STEP_DELAY):
        """
        One-shot Phantom clicker:
        - Ensures wallet is unlocked.
        - Waits briefly for Phantom to animate the confirm dialog.
        - Performs a single confirm-button click.
        - Exits immediately. No watcher loop.
        """
        screenHelper = ScreenHelper()
        scaling = screenHelper.detect_scaling_factor()

        Logger.info(f"🤝 `phantomclicker()` started")
        Logger.debug(f"🔍 Scaling detected: (scale={scaling}x)")

        if not kill_switch_active(): 
            # === 1. Detect locked wallet ===
            if not self.unlock_phantom():
                Logger.info("⏱️ Timeout waiting for Phantom unlock. Exiting automation.")
                return False
            Logger.info("✅ Wallet is unlocked.")

            # === Detect and confirm transactions (handles errors internally) ===
            if SwapFlow.click_confirm_button(self):
                Logger.debug(f"✅ Confirmed Phantom transaction")
                return True

            else:
                print("🔍 No confirm button detected")
                time.sleep(delay*2)

        else:
            Logger.info(f"'❌ Found kill_switch.txt in {os.getcwd()} — exiting python_clicker()")
# ===================
# Execute run_swap_flow()
# ===================
app = Flask(__name__)
CORS(app)



@app.route("/ui-log", methods=["POST"])
def ui_log():
    """
    Pipes all debugLog messages from the UI into Flask / Terminal
    """
    data = request.json
    msg = data.get("message", "")
    ts  = data.get("timestamp", "")
    if msg:
        Logger.info(f"[Aquavaults Swapper]: [{ts}] {msg}")
    return {"status": "ok"}


@app.route("/trigger-click", methods=["POST"])
def trigger_click_confirm():
    """
    Called by AquaVaults frontend when a transaction is ready to confirm.
    Spawns a short-lived background thread that runs phantom_clicker().
    """
    delay = request.json.get("delay", 1.0)
    try:
        delay = float(delay)
    except:
        delay = 1.0
    screen = ScreenHelper()
    timing = Timing()
    config = {}   # or your real config dict
    flow = SwapFlow(screen, timing, config)
    threading.Thread(target=flow.phantom_clicker, args=(delay,), daemon=True).start()

    Logger.info(f"[trigger] Scheduled confirm click in {delay}s")
    return {"status": "ok"}

if __name__ == "__main__":
    Logger.info("🚀 Click_confirm API running at http://localhost:5555/trigger-click-confirm")
    Logger.debug(f"[python-debug] Executable: {sys.executable}")

    app.run(port=5555, debug=True)
