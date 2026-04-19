import discord
import re
import aiohttp
import asyncio
import json
import os
import sys
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)
sys.stdout.reconfigure(encoding='utf-8')

CONFIG_FILE = 'config.json'

_redeemed_codes = set()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_console()
    banner = f"""{Fore.MAGENTA}{Style.BRIGHT}
  _   _ _ _             _____       _
 | \\ | (_) |           / ____|     (_)
 |  \\| |_| |_ _ __ ___| (___  _ __  _ _ __   ___ _ __
 | . ` | | __| '__/ _ \\___ \\| '_ \\| | '_ \\ / _ \\ '__|
 | |\\  | | |_| | | (_) |___) | | | | | |_) |  __/ |
 |_| \\_|_|\\__|_|  \\___/_____/|_| |_|_| .__/ \\___|_|
                                     | |
                                     |_|
 {Fore.CYAN}       ╔══════════════════════════════════════╗
        ║    {Fore.WHITE}ULTRA FAST NITRO SNIPER V2{Fore.CYAN}      ║
        ║       {Fore.YELLOW}Multi-Account Edition{Fore.CYAN}         ║
        ║           {Fore.YELLOW}Made by @_m13{Fore.CYAN}             ║
        ╚══════════════════════════════════════╝
"""
    print(banner)

def get_time():
    return datetime.now().strftime("%H:%M:%S")

def log(level, message, tag=""):
    time_str = f"{Fore.BLACK}{Style.BRIGHT}[{get_time()}]{Style.RESET_ALL}"
    tag_str = f"{Fore.BLUE}[{tag}]{Style.RESET_ALL} " if tag else ""

    if level == "INFO":
        prefix = f"{Fore.CYAN}[INFO]{Style.RESET_ALL}"
    elif level == "SUCCESS":
        prefix = f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL}"
    elif level == "WARNING":
        prefix = f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL}"
    elif level == "ERROR":
        prefix = f"{Fore.RED}[ERROR]{Style.RESET_ALL}"
    else:
        prefix = f"{Fore.WHITE}[*]{Style.RESET_ALL}"

    print(f"{time_str} {prefix} {tag_str}{message}")

def load_config():
    if not os.path.exists(CONFIG_FILE):
        log("WARNING", "config.json not found. Creating a new one...")
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"user_tokens": []}, f, indent=4)
        return {"user_tokens": []}

    with open(CONFIG_FILE, 'r') as f:
        data = json.load(f)

    # Migrate old single-token format to list
    if "user_token" in data and "user_tokens" not in data:
        old = data["user_token"]
        data = {"user_tokens": [old] if old else []}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    return data

# ----------------- SNIPER MODULE -----------------
class NitroSniper(discord.Client):
    def __init__(self, token, all_tokens, account_index):
        super().__init__()
        self.user_token = token
        self.all_tokens = all_tokens
        self.tag = f"Acc#{account_index + 1}"
        self.nitro_regex = re.compile(
            r'(discord\.gift/|discordapp\.com/gifts/|discord\.com/gifts/)([a-zA-Z0-9]{16,24})'
        )

    async def on_ready(self):
        log("SUCCESS", f"Logged in as {self.user.name} | Monitoring {len(self.guilds)} servers & DMs", self.tag)

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        match = self.nitro_regex.search(message.content)
        if match:
            code = match.group(2)
            colorized = f"{code[:4]}{Fore.MAGENTA}....{Style.RESET_ALL}{code[-4:]}"
            log("WARNING", f"Code detected: {colorized} [From: {message.author}]", self.tag)
            asyncio.create_task(self._redeem_on_all(code, message.channel.id))

    async def _redeem_on_all(self, code, channel_id):
        # Deduplicate: if another account already triggered redemption, skip
        if code in _redeemed_codes:
            return
        _redeemed_codes.add(code)

        # All tokens attempt to redeem simultaneously
        await asyncio.gather(*[
            self._redeem(code, channel_id, token, f"Acc#{i + 1}")
            for i, token in enumerate(self.all_tokens)
        ])

    async def _redeem(self, code, channel_id, token, tag):
        url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}/redeem"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        payload = {"channel_id": str(channel_id), "payment_source_id": None}

        start_time = datetime.now()
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                latency = round((datetime.now() - start_time).total_seconds() * 1000)

                if response.status == 200:
                    log("SUCCESS", f"REDEEMED NITRO! (Latency: {latency}ms) [Code: {code}]", tag)
                elif response.status == 400:
                    log("ERROR", f"Invalid code. ({latency}ms)", tag)
                elif response.status == 404:
                    log("ERROR", f"Unknown/expired code. ({latency}ms)", tag)
                elif response.status == 429:
                    log("ERROR", f"Rate limited! ({latency}ms)", tag)
                else:
                    data = await response.text()
                    if "has been redeemed already" in data:
                        log("ERROR", f"Already redeemed by someone else. ({latency}ms)", tag)
                    else:
                        log("ERROR", f"Failed. HTTP {response.status}", tag)

# ----------------- MAIN -----------------
def save_tokens(tokens):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"user_tokens": tokens}, f, indent=4)
    except Exception as e:
        log("ERROR", f"Could not save config: {e}")

def manage_tokens(tokens):
    while True:
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}--- Token Manager ---{Style.RESET_ALL}")
        if tokens:
            for i, t in enumerate(tokens):
                masked = f"{t[:8]}...{t[-6:]}"
                print(f"  {Fore.CYAN}[{i + 1}]{Style.RESET_ALL} {masked}")
        else:
            print(f"  {Fore.YELLOW}(no tokens){Style.RESET_ALL}")

        print(f"\n{Fore.CYAN}[A]{Style.RESET_ALL} Add token")
        print(f"{Fore.CYAN}[R]{Style.RESET_ALL} Remove token")
        print(f"{Fore.CYAN}[B]{Style.RESET_ALL} Back\n")

        action = input(f"{Fore.MAGENTA} > Choose: {Style.RESET_ALL}").strip().lower()

        if action == "a":
            while True:
                t = input(f"{Fore.MAGENTA} > Enter token (blank to stop): {Style.RESET_ALL}").strip()
                if not t:
                    break
                if t in tokens:
                    log("WARNING", "Token already in list, skipping.")
                else:
                    tokens.append(t)
                    save_tokens(tokens)
                    log("SUCCESS", f"Token added. Total: {len(tokens)}")

        elif action == "r":
            if not tokens:
                log("WARNING", "No tokens to remove.")
                continue
            idx = input(f"{Fore.MAGENTA} > Enter token number to remove: {Style.RESET_ALL}").strip()
            try:
                idx = int(idx) - 1
                if 0 <= idx < len(tokens):
                    removed = tokens.pop(idx)
                    save_tokens(tokens)
                    log("SUCCESS", f"Removed token ...{removed[-6:]}")
                else:
                    log("ERROR", "Invalid number.")
            except ValueError:
                log("ERROR", "Enter a valid number.")

        elif action == "b":
            break

def main():
    print_banner()

    config = load_config()
    tokens = [t.strip() for t in config.get("user_tokens", []) if t.strip()]

    if not tokens:
        log("INFO", "No tokens configured. Enter Discord USER tokens (one per line, blank line to finish):")
        while True:
            t = input(f"{Fore.MAGENTA} > Token #{len(tokens) + 1} (blank to finish): {Style.RESET_ALL}").strip()
            if not t:
                break
            tokens.append(t)

        if not tokens:
            log("ERROR", "No tokens provided. Exiting.")
            sys.exit(0)

        save_tokens(tokens)
        log("INFO", f"Saved {len(tokens)} token(s) to config.json.")

    while True:
        print_banner()
        log("INFO", f"Loaded {len(tokens)} token(s).")

        print(f"\n{Fore.CYAN}[1]{Style.RESET_ALL} Start Nitro Sniper ({len(tokens)} accounts)")
        print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Manage Tokens (add / remove)")
        print(f"{Fore.CYAN}[3]{Style.RESET_ALL} Exit\n")

        choice = input(f"{Fore.MAGENTA} > Choose an option: {Style.RESET_ALL}").strip()

        if choice == "1":
            break
        elif choice == "2":
            manage_tokens(tokens)
            # Reload in case tokens changed
            tokens = [t.strip() for t in load_config().get("user_tokens", []) if t.strip()]
        elif choice == "3":
            sys.exit(0)

    if not tokens:
        log("ERROR", "No tokens configured. Exiting.")
        sys.exit(0)

    log("INFO", "Initializing Sniper Engine for all accounts...")

    clients = [
        NitroSniper(token=t, all_tokens=tokens, account_index=i)
        for i, t in enumerate(tokens)
    ]

    async def run_all():
        await asyncio.gather(*[
            client.start(token)
            for client, token in zip(clients, tokens)
        ])

    try:
        asyncio.run(run_all())
    except KeyboardInterrupt:
        log("INFO", "Sniper stopped by user.")
    except Exception as e:
        log("ERROR", f"Fatal error: {e}")

if __name__ == "__main__":
    main()
