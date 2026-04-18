import discord
import re
import aiohttp
import asyncio
import json
import os
import sys
from datetime import datetime
from colorama import init, Fore, Style

# Initialize Colorama for Console colors
init(autoreset=True)
sys.stdout.reconfigure(encoding='utf-8')

CONFIG_FILE = 'config.json'

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_console()
    banner = f"""{Fore.MAGENTA}{Style.BRIGHT}
  _   _ _ _             _____       _                 
 | \ | (_) |           / ____|     (_)                
 |  \| |_| |_ _ __ ___| (___  _ __  _ _ __   ___ _ __ 
 | . ` | | __| '__/ _ \\___ \| '_ \| | '_ \ / _ \ '__|
 | |\  | | |_| | | (_) |___) | | | | | |_) |  __/ |   
 |_| \_|_|\__|_|  \___/_____/|_| |_|_| .__/ \___|_|   
                                     | |              
                                     |_|              
 {Fore.CYAN}       ╔═════════════════════════════════╗
        ║    {Fore.WHITE}ULTRA FAST NITRO SNIPER V1{Fore.CYAN}   ║
        ║           {Fore.YELLOW}Made by @_m13{Fore.CYAN}         ║
        ╚═════════════════════════════════╝
"""
    print(banner)

def get_time():
    return datetime.now().strftime("%H:%M:%S")

def log(level, message):
    time_str = f"{Fore.BLACK}{Style.BRIGHT}[{get_time()}]{Style.RESET_ALL}"
    
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
        
    print(f"{time_str} {prefix} {message}")

def load_config():
    if not os.path.exists(CONFIG_FILE):
        log("WARNING", "config.json not found. Creating a new one...")
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"user_token": ""}, f, indent=4)
        return {"user_token": ""}
    
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

# ----------------- SNIPER MODULE -----------------
class NitroSniper(discord.Client):
    def __init__(self, token):
        super().__init__()
        self.user_token = token
        self.nitro_regex = re.compile(r'(discord.gift/|discordapp.com/gifts/|discord.com/gifts/)([a-zA-Z0-9]{16,24})')

    async def on_ready(self):
        log("SUCCESS", f"Successfully logged in as {self.user.name}!")
        log("INFO", f"Sniper is now monitoring all your {len(self.guilds)} servers & DMs... Keep this window open.\n")

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        match = self.nitro_regex.search(message.content)
        
        if match:
            code = match.group(2)
            colorized = f"{code[:4]}{Fore.MAGENTA}.....{Style.RESET_ALL}{code[-4:]}"
            log("WARNING", f"Nitro Code detected: {colorized} [Sent by {message.author}]")
            asyncio.create_task(self.redeem_code(code, message.channel.id))

    async def redeem_code(self, code, channel_id):
        url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}/redeem"
        headers = {
            "Authorization": self.user_token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        payload = {"channel_id": str(channel_id), "payment_source_id": None}

        start_time = datetime.now()
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                latency = round((datetime.now() - start_time).total_seconds() * 1000)

                if response.status == 200:
                    log("SUCCESS", f"🔥 SUCCESSFULLY REDEEMED NITRO! (Latency: {latency}ms) [Code: {code}]")
                elif response.status == 400:
                    log("ERROR", f"Invalid Code. (Latency: {latency}ms)")
                elif response.status == 404:
                    log("ERROR", f"Unknown / Expired Code. (Latency: {latency}ms)")
                elif response.status == 429:
                    log("ERROR", f"Rate Limit - You are sniping too many codes! (Latency: {latency}ms)")
                else:
                    data = await response.text()
                    if "has been redeemed already" in data:
                        log("ERROR", f"Code already redeemed by someone else! (Latency: {latency}ms)")
                    else:
                        log("ERROR", f"Failed to redeem. HTTP Code: {response.status}")

def main():
    print_banner()
    
    config = load_config()
    token = config.get("user_token", "").strip()
    
    if not token or token == "":
        log("ERROR", "User token is not configured.")
        token = input(f"{Fore.MAGENTA} > Enter your Discord USER Token: {Style.RESET_ALL}").strip()
        
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump({"user_token": token}, f, indent=4)
        except Exception:
            pass

    if not token:
        log("ERROR", "No token provided. Exiting.")
        sys.exit(0)

    # Main Menu
    print(f"\n{Fore.CYAN}[1]{Style.RESET_ALL} Start Nitro Sniper")
    print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Exit\n")
    
    choice = input(f"{Fore.MAGENTA} > Choose an option: {Style.RESET_ALL}").strip()
    
    if choice == "1":
        log("INFO", "Initializing Sniper Engine...")
        client = NitroSniper(token=token)
        try:
            client.run(token, log_handler=None)
        except Exception as e:
            log("ERROR", f"Failed to connect: {e}\n(Check your Token)")
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()