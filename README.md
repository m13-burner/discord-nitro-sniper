# ⚡ Ultra Fast Discord Nitro Sniper V1

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![aiohttp](https://img.shields.io/badge/Library-aiohttp-red)
![discord.py-self](https://img.shields.io/badge/discord.py--self-Wrapper-7289DA)

A blazingly fast, lightweight, and undetectable Discord Nitro Sniper. It passively connects to your user account, monitors all your guilds and DMs, and instantly redeems any Discord Nitro gift link before anyone else using a highly-optimized asynchronous HTTP request.

## ✨ Features

*   **⚡ Ultra Fast Redemption:** Uses raw `aiohttp` API requests to redeem codes in milliseconds.
*   **🛡️ Undetectable & Safe:** Only passively reads messages. It does NOT spam Discord's API, meaning you won't trigger anti-spam flags or Captchas just by running it.
*   **🎨 Beautiful CLI:** Clean, colorful, and interactive Command-Line Interface using `colorama`.
*   **🔍 Regex Scanner:** Ignores fake links and efficiently parses `discord.gift` and `discord.com/gifts/` codes from large paragraphs of text instantly.

## ⚠️ Important Disclaimer
*This project is made for educational purposes and Proof of Concept only.* 
Automating User Accounts (Self-Botting) is strictly against Discord's Terms of Service. By deciding to use this software, you take full responsibility for your actions and any consequence (such as account termination) that may occur. Please do not use this to harm or spam communities.

## 🛠️ Prerequisites

*   [Python 3.8+](https://www.python.org/downloads/)
*   Your personal Discord **User Token**.
    *(Note: Do NOT use a Bot Token from the Developer Portal. This requires an actual user account token).*

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/discord-nitro-sniper.git
   cd discord-nitro-sniper
   ```

2. Install the required python libraries (using the provided `.bat` file or manually):
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

**Windows:**
Simply double check the `start.bat` file to automatically install dependencies and run the interactive menu.

**Linux / Mac:**
```bash
python sniper.py
```

### Main Menu

*   **[1] Start Nitro Sniper:** Connects your account and starts monitoring for Nitro codes silently in the background. Keep the CLI window open!
*   **[2] Exit:** Closes the application securely.

### Configuration
The first time you launch the sniper, it will ask for your User Token. This is safely saved locally in `config.json` so you never have to type it again.

## 📝 About
This sniper was designed to show how asynchronous web requests combined with Websocket listeners can outperform standard heavy python GUI bots.
