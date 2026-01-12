# AquaVaults Swapper Setup Guide
---

> ⚠️ **QUICK TIP**: GitHub may save the HTML file as `.txt` - see Step 1 for how to fix this!

🪐 Running the AquaVaults HTML Swapper Locally (Phantom + Custom RPC + Jupiter API)

This project is a single HTML file that must be served via a local server to connect to Phantom Wallet and a Solana RPC. Opening it directly in the browser will not work.

This guide walks you through downloading the file, setting up Python, and running it locally.

Please see https://github.com/RaptorCapture247/AquaVaults-Swapper/blob/main/SummaryandOverview.md for technical details.

> You will need an autoclicker of some kind to click the wallet popups while using the Auto Swapper function. You can use a generic clicker such as OPautoclicker or use one of my PyatuoGUI clickers found at: [Windows-Pyatuo-Auto-Clicker](https://github.com/RaptorCapture247/Windows-Pyatuo-Auto-Clicker) / [Mac-PyAuto-Auto-Clicker](https://github.com/RaptorCapture247/Mac-PyAuto-Auto-Clicker)


---

## ⚠️ IMPORTANT: Jupiter API Migration (December 2024)

**Jupiter has migrated to an authenticated API system. You MUST obtain a FREE API key to use this swapper.**

### What Changed?
- ✅ **NEW REQUIREMENT**: Jupiter API key (free, takes 2 minutes to get)
- ✅ **Migration Deadline**: December 31, 2025
- ✅ **Free Tier**: 60 requests per minute (plenty for normal use)
- ✅ **One-Time Setup**: Configure once, works forever

### Get Your FREE Jupiter API Key (Required)

**Before you can use the swapper, you need an API key:**

1. Visit **https://portal.jup.ag**
2. Click "Connect via Email"
3. Enter your email and verify
4. Click "Generate API Key"
5. **Copy and save your API key** (you'll need it in Step 7)

> 🔑 **This is required** - The swapper will not work without an API key after December 31, 2025.


---

## There is no guarantee your swaps will count towards participation on Pond0x. While I have used and tested this swapper there is no guarantee it is safe. Please do your due diligence and use a burner wallet before connecting a main wallet. If you are unfamiliar with code, please copy the Swapper-UI.html file and give it to an AI and ask about its functions and risks.


---

### Step 1 – Download the project from GitHub

1. Create a folder in your Documents named **AquaVaults-Swapper**

2. Download the entire the repository from Github and move all the files from **Downloads** to **Documents/AquaVaults-Swapper**

---

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

---

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

---

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

---

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

---

### Step 5 – Open Aquavaults Swapper in Your Browser

1. Open your browser.
2. Go to the URL you copied in step 4 or http://localhost:8000/Swapper-UI.html 

## Step 6 – Configure Jupiter API Key (NEW - REQUIRED)

When you first open the swapper, you'll see the **Jupiter API Key Configuration** panel at the top:

### Configure Your API Key

1. **Enter Your API Key**
   - Paste the API key you got from https://portal.jup.ag
   - Click "Confirm API Key"

2. **Verify Configuration**
   - Status should change to "✅ Configured"
   - You'll see a masked version of your key (e.g., `abcd1234...xyz9`)

3. **Your API Key is Saved**
   - Stored locally in your browser
   - Automatically loaded on future visits
   - Can be changed anytime by clicking "Change API Key"

> 🔑 **Security Note**: Your API key is stored locally in your browser and only sent to Jupiter's API for authentication. It is never shared with anyone else.

> ⚠️ **Important**: You MUST configure the API key before you can configure RPC or connect your wallet.


---

## Step 7 – Configure RPC Endpoint

When you first open the swapper, you are required to confirm RPC choice. The app will remember your choice. 

1. Click whichever RPC option you want:

- **Default RPC**: Defaults to the public Solana RPC or the RPC you defined in `config.js`, 
- **Custom RPC**: Enter an RPC URL for a different provider (recommended for better performance)

2. Click **Confirm RPC**

3. To change RPC later, click "Change RPC" button.


> ⚡ **Recommended**: Use a custom RPC from providers such as Helius (https://helius.dev) or QuickNode for faster, more reliable performance.

> ⚡ Solana's RPC is free, but may be slower, apply crushing rate limits, or refuse your requests for no apparent reason.

---

## Step 8 – Connect Wallet and Start Swapping

1. **Connect Phantom Wallet**
   - Click "Connect Wallet"
   - Approve the connection in Phantom

2. **Choose Your Affiliate**
   - Toggle between Pond0x (swap rewards & mining boost) or AquaVaults (support development)

3. **Configure Your Swap**
   - Select tokens (From/To)
   - Enter amount
   - Adjust slippage and fees if needed

4. **Execute Swap**
   - Click "Swap"
   - Approve transaction in Phantom
   - Wait for confirmation

### Optional: Auto Swap Features

- Check "🤖 Enable Auto Swap Control" to access automated swapping
- Configure number of swaps, wait time, and optional random amounts
- Use with an auto-clicker for fully automated operation

### Step 7 - Swap Harder

Aquavaults Swapper is ez and doesn't need a lot of instruction. 

## Step 9 – (Mac Only) Permissions

If macOS asks:
- "Python wants to accept incoming network connections" → click **Allow**
- If asked for folder access → click **OK**
- If Python is blocked → System Settings → Privacy & Security → **Allow Anyway**

If the automation is failing to find things to click or not recognizing Phantom errors, then your issue is probably the screenshots. 

---

### Step 10 – Stop the Server

1. Click into **Terminal** or **Command Prompt**.
2. Press *Ctrl + C*

---

## ✅ You're Done!

The AquaVaults Swapper is running locally with:
- ✅ Jupiter API authentication configured
- ✅ RPC endpoint configured through the UI or config.js and .env
- ✅ Phantom Wallet connection ready
- ✅ Full swapping functionality available

- ✅ This version also runs a `pyAutoGUI` automation to handle clicking Confirm on Phantom or to click Cancel when it detects a Phantom error or warning. 


---

## Troubleshooting Tips

### File downloaded as .txt instead of .html
**Problem**: GitHub saved the file as `Swapper-UI.html.txt`  
**Solution**: 
- **Windows**: Enable file extensions (View → File name extensions), then rename file to remove `.txt`
- **Mac**: Select file, press Enter, remove `.txt` from filename
- **Alternative**: See Step 1 above for alternative download methods
- **Verify**: File icon should look like a web browser, not a text document

### Page shows code instead of the swapper interface
**Problem**: Browser is displaying the HTML code as text  
**Solution**: This happens if file has wrong extension
- Check the file is named `.html` not `.html.txt`
- Make sure you opened it through `localhost:8000` not by double-clicking
- Follow the .txt fix instructions in Step 1

### "Please configure Jupiter API key first"
**Solution**: You need to enter your API key from portal.jup.ag in the Jupiter API Key panel before you can proceed.

### "401 Unauthorized" errors
**Solution**: Your API key may be incorrect. Click "Change API Key" and re-enter it.

### Cannot configure RPC
**Solution**: Make sure you've configured your Jupiter API key first. The API key is required before RPC setup.

### Rate limit errors
**Problem**: Hitting the 60 requests/minute limit  
**Solution**: Use longer wait times in auto swap, or consider upgrading at portal.jup.ag

### Wallet won't connect
**Solution**: 
- Make sure you've configured both API key AND RPC endpoint
- Ensure Phantom Wallet is installed and unlocked
- Verify the page is served via `localhost:8000` (or the port you specified in the .env file) and not `file://`

### RPC configuration not working
**Solution**: 
- Ensure Phantom Wallet is installed, unlocked
- Check the terminal is still running the local server
- If using custom RPC, verify your endpoint URL is correct and has sufficient credits/quota. 
- Also verify that your custom RPC URL are correct and in the .env and/or config.js files. 

### API key not saving
**Problem**: localStorage may be disabled  
**Solution**: 
- Check browser settings allow localStorage
- Try a different browser
- Make sure you're on `localhost:8000` not `file://`


---

## Configuration Summary

### Required Steps (In Order)
1. ✅ Get Jupiter API key from portal.jup.ag
2. ✅ Configure API key in swapper
3. ✅ Configure RPC endpoint
4. ✅ Connect Phantom wallet
5. ✅ Start swapping!

### What Gets Saved
Your configuration is automatically saved in your browser:
- Jupiter API key (masked in UI for security)
- RPC endpoint preference (Default or Custom)
- Custom RPC URL (if using custom)
- Affiliate selection (Pond0x or AquaVaults)

### Subsequent Sessions
On your next visit:
- API key automatically loaded ✅
- RPC settings automatically loaded ✅
- Just connect wallet and swap! ✅


---

## Additional Resources

### Jupiter API
- **Get API Key**: https://portal.jup.ag
- **API Documentation**: https://dev.jup.ag
- **Migration Guide**: https://dev.jup.ag/portal/migrate-from-lite-api
- **Rate Limits**: https://dev.jup.ag/portal/rate-limit

### RPC Providers
- **Helius**: https://helius.dev (recommended)
- **QuickNode**: https://quicknode.com
- **Alchemy**: https://alchemy.com

### Auto-Clickers (for Auto Swap)
- **Windows**: [Windows-Pyatuo-Auto-Clicker](https://github.com/RaptorCapture247/Windows-Pyatuo-Auto-Clicker)
- **Mac**: [Mac-PyAuto-Auto-Clicker](https://github.com/RaptorCapture247/Mac-PyAuto-Auto-Clicker)
- **Generic**: OPautoclicker or similar


---

## FAQ

### Do I need to pay for the Jupiter API key?
**No!** The free tier provides 60 requests per minute, which is plenty for normal use.

### What happens if I don't migrate?
After December 31, 2025, the old API endpoints will stop working and swaps will fail.

### Can I use the same API key on multiple computers?
**Yes!** You can use the same API key across different browsers and computers.

### Is my API key safe?
**Yes** - it's stored locally in your browser and only sent to Jupiter's API for authentication.

### Do I need a custom RPC?
**No, but recommended.** The default RPC works but custom RPCs (Helius, QuickNode) provide better performance.

### How many swaps can I do with the free API tier?
60 requests per minute = approximately 30 swaps per minute (each swap uses 2 requests).


---

## Version Notes

### Current Version Features
- ✅ Jupiter authenticated API (api.jup.ag)
- ✅ API key configuration UI
- ✅ Custom RPC support
- ✅ Dual affiliate system (Pond0x/AquaVaults)
- ✅ Auto swap with random amounts
- ✅ Token vault fee collection
- ✅ Comprehensive error handling

### Migration from Old Version
If you're upgrading from the old swapper:
1. Get your Jupiter API key
2. Download the new version
3. Configure API key (one-time setup)
4. Everything else works the same!


---

**Need Help?** Check the troubleshooting section above or review the detailed migration guide in the repository.


---
## Capturing screenshots
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
7. Move it to the **images** subfolder and overwrite the examples with screenshots from your system. 
 
 If you will use Aquavaults on multiple systems from one shared folder:
 - Set up a next-level subfolder for each system inside **images**
 - Update **.env** with the filepaths for each system, using **env-example.txt** as your template. 



