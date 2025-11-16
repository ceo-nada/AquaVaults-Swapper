# AquaVaults Swapper Setup Guide
---

🪐 Running the AquaVaults HTML Swapper Locally (Phantom + Custom RPC)

This project is a single HTML file that must be served via a local server to connect to Phantom Wallet and a Solana RPC. Opening it directly in the browser will not work.

This guide walks you through downloading the file, setting up Python, and running it locally.

Please see https://github.com/RaptorCapture247/AquaVaults-Swapper/blob/main/SummaryandOverview.md for technical details.

> You will need an autoclicker of some kind to click the wallet popups while using the Auto Swapper function. You can use a generic clicker such as OPautoclicker or use one of my PyatuoGUI clickers found at: [Windows-Pyatuo-Auto-Clicker](https://github.com/RaptorCapture247/Windows-Pyatuo-Auto-Clicker) / [Mac-PyAuto-Auto-Clicker](https://github.com/RaptorCapture247/Mac-PyAuto-Auto-Clicker)


---

## There is no guarantee your swaps will count towards participation on Pond0x. While I have used and tested this swapper there is no guarantee it is safe. Please do your due diligence and use a burner wallet before connecting a main wallet. If you are unfamiliar with code, please copy the Swapper-UI.html file and give it to an AI and ask about its functions and risks.


------------------------------------------------

### Step 1 – Download the project from GitHub

1. Create a folder in your Documents named **AquaVaults-Swapper**

2. Download the entire the repository from Github and move them all from **Downloads** to **Documents/AquaVaults-Swapper**

------------------------------------------------

### Step 2 - Check for Python and Install if needed

**macOS**

1. Open **Terminal**. Run:
```bash
python3 --version
```
If you see Python 3.x.x, you're good.

If not, install Python from: https://www.python.org/downloads/

**Windows**
1. Open **Command Prompt** or **PowerShell**. Run:
```bash
python --version
```

If not installed, download from: https://www.python.org/downloads/windows/During install, check: “Add Python to PATH”.


### Step 3 – Create and Configure a venv
A virtual environment (venv) keeps your computer clean and tidy by serving as a home base for all the dependencies (aka software packages) needed to run a specific project.

You'll use two separate locations to run this project:
- venv folder: must be local-only, meaning it is not synched to the cloud
- project folder: may be in an iCloud or OneDrive folder

**macOS** 
1. Choose where to create your venv:
You can use the recommended layout or adapt to your own file structure. These instructions assume the former. 

Recommended layout: 
`~/venvs/aquavaults-venv`            ← venv
`~/Documents/AquaVaults-Swapper`     ← project

2. Create the venv. From **Terminal**, run: 
```bash
mkdir -p ~/venvs
python3 -m venv ~/venvs/aquavaults-venv
```

3. Activate the venv
Run this the first time you set up the venv and every time you start AquaVaults swapper:
```bash
source ~/venvs/aquavaults-venv/bin/activate
```
You should see (aquavaults-venv) showing in Terminal.

4. Install project dependencies: still in **Terminal**, run:
```bash
cd ~/Documents/AquaVaults-Swapper
pip install -r requirements.txt
```
Or install manually:
```bash
pip install flask flask-cors pyautogui opencv-python pillow
```

5. Set macOS Accessibility & Screen Recording Permissions

Go to **System Settings** → **Privacy & Security**.

Find and click into **Accessibility** then add:
- **Terminal** (located in Applications)
- **Flask** (located in `venvs/aquavaults-venv/bin`)
- **Python** (typically located in `/Library/Frameworks/Python.framework/Versions/3.13/bin`)

*if you can't select Python3.xx from the venv folder, right-click it and select **show original**. A new finder window may open. Drag and drop Python3.xx into Settings.*

Go back to the previous menu and find **Screen Recording**. Repeat the previous steps. 

*If automation or screenshots fail, it's usually permissions. Ask your favorite LLM for help if this happens.*

6. Verify the venv is active. Run from **Terminal**:
```bash
python -m site
```
You should see paths under ~/venvs/aquavaults-venv/....

**Windows** 
1. Choose where to create your venv.
You can use the recommended layout or adapt to your own file structure. These instructions assume the former. 

`C:\Users\YourName\Documents\AquaVaults-Swapper`   ← project
`C:\venvs\aquavaults-venv `                        ← venv

2. Create the venv from Command Prompt or PowerShell:
```bash
mkdir C:\venvs
python -m venv C:\venvs\aquavaults-venv
```

3. Activate the venv

From **Command Prompt**:
```bash
C:\venvs\aquavaults-venv\Scripts\activate
```

From **PowerShell**:
```bash
C:\venvs\aquavaults-venv\Scripts\Activate.ps1
```
If PowerShell blocks activation:
```bash
Set-ExecutionPolicy RemoteSigned
```

4. Install dependency packages
```bash
cd C:\Users\YourName\Documents\AquaVaults-Swapper
pip install -r requirements.txt
```

Or manually:
```bash
pip install flask flask-cors pyautogui opencv-python pillow
```

5. Set Windows Permissions
Windows generally works without special permissions, but you should: 
- Approve Windows Defender prompts
- Avoid running in restricted corporate environments

6. Confirm you're using the venv by running:
```bash
python -m site
```
You should see:
`C:\venvs\aquavaults-venv\Lib\site-packages`

------------------------------------------------

### Step 3 – Configure RPC and Default Port
1. Go to your project folder. Make a copy of these files: 
- `config-example.js`
- `env-example.txt`

2. Rename them:
`config.js`
`.env` (yes, include the period and remove any/all file extension)

3. Open `config.js` in a text editor. 

This file lets you set a custom RPC as the default. If this isn't for you: 
-add **//** to comment-out the line, so that your computer will ignore it,  e.g. `//DEFAULT_RPC: "{{RPC_URL}}",`

And if you're fancy:
- Replace  `"{{RPC_URL}}"` with  `"http://your-rpc-url"` 
- Leave the `LOCAL_BRIDGE_URL` as is unless you're doing advanced shit. 

4. Open `.env` in a text editor. 
The .env file holds information that you may not want to be public. Aquavaults Swapper uses these values to load services and find images that are needed to automate clicks. 

- If you're using a custom RPC, replace the **RPC_URL** value. If not, delete the entire line. 
- Set **LOCAL_PORT** to any 4-digit number you like. The port defines the URL you will use to run AquaVaults Swapper. 
- Leave **LOCAL_BRIDGE_URL** as is unless you're doing fancy stuff
- Set **FILE_PATH_1_KEYWORD** and **FILE_PATH_1** as needed to allow this app to run on multiple systems, which typically require their own screenshots. 
- If you're running on just one system, delete all of the related lines. 
- Remove the comment at the top.
- Remove any empty lines. 
- Save the file.

**Important**: Remember to actually create the subfolders you'll need for each system and use the same names as you entered into the .env

*Tips*: 
- *If you can't see .env in Finder or Windows Explorer, enable viewing of hidden files and folders.*
- *If you can't see any file extensions, enable that too.*

------------------------------------------------

### Step 4 – Start the Local Server 

1. Activate the venv (if not already activated)
Run this the first time you set up the venv and every time you start AquaVaults swapper:

**macOS Terminal**
```bash
source ~/venvs/aquavaults-venv/bin/activate
```

**Windows Command Prompt**:
```bash
C:\venvs\aquavaults-venv\Scripts\activate
```

2. Fire it up by running this command:
```bash
python run_all.py
```

3. Copy the URL that prints in Terminal or Command Prompt:
```bash
Serving AquaVaults-Swapper on http://localhost:8000/swapper-ui.html
```

------------------------------------------------

### Step 5 – Open Aquavaults Swapper in Your Browser

1. Open your browser.
2. Go to the URL you copied in step 4 or http://localhost:8000/Swapper-UI.html 

------------------------------------------------

### Step 6 – Configure RPC Endpoint

When you first open the swapper, you are required to confirm RPC choice. The app will remember your choice. 

1. Click whichever RPC option you want:

- **Default RPC**: Defaults to the public Solana RPC or the RPC you defined in `config.js`, 
- **Custom RPC**: Enter an RPC URL for a different provider (recommended for better performance)

2. Click **Confirm RPC**

3. To change RPC later, click "Change RPC" button.

> ⚡ **Recommended**: Use a custom RPC from providers like Helius (https://helius.dev) or QuickNode for faster, more reliable performance.

> ⚡ Solana's RPC is free, but may be slower, apply crushing rate limits, or refuse your requests for no apparent reason.

------------------------------------------------

### Step 7 - Swap Harder

Aquavaults Swapper is ez and doesn't need a lot of instruction. 

1. Choose your tokens from the dropdowns. The tokens available are known to contribute to mining boost. 

2. Connect Phantom wallet. 

3. Choose between swapping once or auto-swapping. 

After you initiate a swap or set up auto-swapping, an automation will run on each swap to click Confirm in Phantom, or cancel if it sees an error. 

You will need to capture your own screenshots—see instructions at the bottom.

If the automation is failing to find things to click or not recognizing Phantom errors, then your issue is probably the screenshots. 

------------------------------------------------

### Step 8 – Stop the Server

1. Click into **Terminal** or **Command Prompt**.
2. Press *Ctrl + C*

------------------------------------------------

✅ You're Done!

The AquaVaults Swapper (Swapper-UI.html) is running locally. It calls a `pyAutoGUI` automation to handle clicking confirm or cancelling transactions with errors. 

The RPC endpoint is configured through the UI or your custom settings. 

Choose your options and swap harder! 


### Troubleshooting Tips:

- Make sure you've configured an RPC endpoint in the UI before trying to connect your wallet.
- Ensure Phantom Wallet is installed, unlocked, and the page is served via localhost.
- Check that Terminal or Command Prompt is still running the local server from the venv
- If using a custom RPC, verify your endpoint URL is correct and has sufficient credits/quota.

------------------------------------------------
### Capturing screenshots
Every system, browser, and display is a little different, so screenshots taken on one system are not likely to work on another. 

Hence, you'll need to make your own version of each example screenshot. 

For each image:

1. From your venv, run the following command to capture a perfect screenshot:
```bash
python3 screenshot_debug.py
```
2. Go to your project folder and find the new image named **debug_screenshot.png**
3. Open the image in **Preview** or **Paint**. 
4. Crop the image to be very similar to the examples. Crop the images *tightly* to the element that needs to be recognized or clicked; any extra can confuse the program. 
5. Close and save the image. 
6. Rename it, matching the names used for the example images.
7. Move it to the **images** subfolder, or into the next-level subfolder if you're using this program on multiple systems and have set up folders for each inside **images**



