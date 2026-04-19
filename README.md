[README.md](https://github.com/user-attachments/files/26870173/README.md)
# ⚡ Ultra Fast Discord Nitro Sniper V2

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![aiohttp](https://img.shields.io/badge/Library-aiohttp-red)
![discord.py-self](https://img.shields.io/badge/discord.py--self-Wrapper-7289DA)

A blazingly fast, lightweight, and undetectable Discord Nitro Sniper with **multi-account support**. It connects to all your accounts simultaneously, monitors every guild and DM across all of them, and fires redemption attempts from every account at once the moment a gift code is detected.

## ✨ Features

*   **⚡ Ultra Fast Redemption:** Uses raw `aiohttp` API requests to redeem codes in milliseconds.
*   **👥 Multi-Account:** Run as many accounts as you want simultaneously. All accounts race to redeem every detected code at the same time.
*   **🔒 Deduplication:** If multiple accounts spot the same code at once, redemption is only triggered once — no duplicate spam.
*   **🛠️ In-App Token Manager:** Add or remove tokens directly from the menu without editing any files manually.
*   **🛡️ Undetectable & Safe:** Only passively reads messages. Does NOT spam Discord's API.
*   **🎨 Beautiful CLI:** Clean, colorful, and interactive Command-Line Interface using `colorama`. Each log line is tagged with `[Acc#N]` so you always know which account did what.
*   **🔍 Regex Scanner:** Efficiently parses `discord.gift`, `discordapp.com/gifts/`, and `discord.com/gifts/` codes from any message instantly.

## ⚠️ Important Disclaimer
*This project is made for educational purposes and Proof of Concept only.*
Automating User Accounts (Self-Botting) is strictly against Discord's Terms of Service. By deciding to use this software, you take full responsibility for your actions and any consequence (such as account termination) that may occur. Please do not use this to harm or spam communities.

## 🛠️ Prerequisites

*   [Python 3.8+](https://www.python.org/downloads/)
*   One or more Discord **User Tokens**.
    *(Note: Do NOT use Bot Tokens from the Developer Portal. This requires actual user account tokens).*

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
Simply double-click the `start.bat` file to automatically install dependencies and launch the interactive menu.

**Linux / Mac:**
```bash
python sniper.py
```

### Main Menu

*   **[1] Start Nitro Sniper:** Connects all configured accounts and starts monitoring. Keep the CLI window open!
*   **[2] Manage Tokens:** Add or remove Discord user tokens without touching any config file.
*   **[3] Exit:** Closes the application.

### Token Manager

Accessible from option `[2]` in the main menu:

*   **[A] Add token:** Enter one or more tokens (blank line to stop). Duplicates are automatically skipped.
*   **[R] Remove token:** Shows a numbered list of all saved tokens (masked for safety). Enter the number to remove.
*   **[B] Back:** Return to the main menu.

### Configuration

Tokens are stored in `config.json` as a list under `"user_tokens"`. The file is created automatically on first launch. If you have an old `config.json` with a single `"user_token"` string, it will be migrated to the new format automatically.

## 📝 About
This sniper was designed to show how asynchronous web requests combined with WebSocket listeners can outperform standard heavy Python GUI bots. The multi-account architecture runs all clients in a single event loop via `asyncio.gather()`, meaning there is zero overhead between accounts detecting a code and all of them firing redemption requests simultaneously.
