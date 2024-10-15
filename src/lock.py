import os
import json
import asyncio
from datetime import datetime
from colorama import *
import time
import sys
mrh = Fore.LIGHTRED_EX
pth = Fore.LIGHTWHITE_EX
hju = Fore.LIGHTGREEN_EX
kng = Fore.LIGHTYELLOW_EX
bru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL
htm = Fore.LIGHTBLACK_EX

last_log_message = None

def _banner():
    banner = r"""
╔═══════════════════════════════════════════╗
║              Bot Automation               ║
║         Developed by @ItbaArts_Dev        ║
╚═══════════════════════════════════════════╝ """ 
    print(Fore.CYAN + Style.BRIGHT + banner + Style.RESET_ALL)
    print(hju + "Snapster Auto Bot".center(48))
    log_line()
    loading_animation("Memulai bot...", 5)

def loading_animation(pesan, durasi):
    animasi = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    waktu_selesai = time.time() + durasi
    indeks = 0
    while time.time() < waktu_selesai:
        try:
            sys.stdout.write(f"\r{bru}{animasi[indeks % len(animasi)]} {pesan}".ljust(50))
            sys.stdout.flush()
        except UnicodeEncodeError:
            sys.stdout.write(f"\r{bru}• {pesan}".ljust(50))
            sys.stdout.flush()
        indeks += 1
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * (len(pesan) + 2) + "\r")
    sys.stdout.flush()

def log_pesan(pesan, warna=Style.RESET_ALL, status="", akhir='\n'):
    simbol_status = "✓" if status == "sukses" else "✗" if status == "gagal" else "•"
    sys.stdout.write(f"{warna}{simbol_status} {pesan}{Style.RESET_ALL}{akhir}")
    sys.stdout.flush()

def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def read_config():
    config_path = os.path.join(os.path.dirname(__file__), '../config.json')
    with open(config_path, 'r') as file:
        try:
            config_content = file.read()
            return json.loads(config_content)
        except json.JSONDecodeError as e:
            return {}

def log_error(message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{now} ERROR: {message}\n"
    with open("last.log", "a") as log_file:
        log_file.write(log_entry)

def log(message, **kwargs):
    warna = kwargs.pop('warna', Warna.RESET)
    status = kwargs.pop('status', "")
    log_pesan(message, warna, status, **kwargs)

def log_line():
    print(pth + "═" * 45)

async def countdown_timer(seconds):
    while seconds:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        time_left = f"{h:02d}:{m:02d}:{s:02d}"
        print(f"{pth}please wait until {time_left} ".center(50), flush=True, end="\r")
        seconds -= 1
        await asyncio.sleep(1)
    print(f"{pth}please wait until {time_left} ".center(50), flush=True, end="\r")

def _number(number):
    return "{:,.0f}".format(number)
