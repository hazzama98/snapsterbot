import sys
import asyncio
import aiohttp
import urllib.parse
import json
import random
import string
import os
from datetime import datetime
from colorama import *
import time

# Initialize colorama
init(autoreset=True)

# Color definitions
mrh = Fore.LIGHTRED_EX
pth = Fore.LIGHTWHITE_EX
hju = Fore.LIGHTGREEN_EX
kng = Fore.LIGHTYELLOW_EX
bru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL
htm = Fore.LIGHTBLACK_EX

# Functions from agent.py
def generate_random_user_agent(device_type='android', browser_type='chrome'):
    chrome_versions = list(range(110, 130))
    firefox_versions = list(range(90, 105))
    safari_versions = ['13.0', '14.0', '15.0', '16.0', '17.0']
    edge_versions = list(range(90, 110))

    if browser_type == 'chrome':
        major_version = random.choice(chrome_versions)
        minor_version = random.randint(0, 9)
        build_version = random.randint(1000, 9999)
        patch_version = random.randint(0, 99)
        browser_version = f"{major_version}.{minor_version}.{build_version}.{patch_version}"
    elif browser_type == 'firefox':
        browser_version = random.choice(firefox_versions)
    elif browser_type == 'safari':
        browser_version = random.choice(safari_versions)
    elif browser_type == 'edge':
        browser_version = random.choice(edge_versions)

    if device_type == 'android':
        android_versions = ['10.0', '11.0', '12.0', '13.0', '14.0']
        android_device = random.choice([
            'SM-G960F', 'Pixel 5', 'SM-A505F', 'Pixel 4a', 'Pixel 6 Pro', 'SM-N975F',
            'SM-G973F', 'Pixel 3', 'SM-G980F', 'Pixel 5a', 'SM-G998B', 'Pixel 4',
            'SM-G991B', 'SM-G996B', 'SM-F711B', 'SM-F916B', 'SM-G781B', 'SM-N986B',
            'SM-N981B', 'Pixel 2', 'Pixel 2 XL', 'Pixel 3 XL', 'Pixel 4 XL',
            'Pixel 5 XL', 'Pixel 6', 'Pixel 6 XL', 'Pixel 6a', 'Pixel 7', 'Pixel 7 Pro',
            'OnePlus 8', 'OnePlus 8 Pro', 'OnePlus 9', 'OnePlus 9 Pro', 'OnePlus Nord', 'OnePlus Nord 2',
            'OnePlus Nord CE', 'OnePlus 10', 'OnePlus 10 Pro', 'OnePlus 10T', 'OnePlus 10T Pro',
            'Xiaomi Mi 9', 'Xiaomi Mi 10', 'Xiaomi Mi 11', 'Xiaomi Redmi Note 8', 'Xiaomi Redmi Note 9',
            'Huawei P30', 'Huawei P40', 'Huawei Mate 30', 'Huawei Mate 40', 'Sony Xperia 1',
            'Sony Xperia 5', 'LG G8', 'LG V50', 'LG V60', 'Nokia 8.3', 'Nokia 9 PureView',
            'OPPO Find X3', 'OPPO Reno 6', 'Vivo X60', 'Vivo V21', 'Realme GT', 'Realme 8 Pro',
            'Motorola Edge 20', 'Motorola G Power', 'ASUS Zenfone 8', 'ASUS ROG Phone 5'
        ])
        android_version = random.choice(android_versions)
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (Linux; Android {android_version}; {android_device}) AppleWebKit/537.36 "
                    f"(KHTML, like Gecko) Chrome/{browser_version} Mobile Safari/537.36")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (Android {android_version}; Mobile; rv:{browser_version}.0) "
                    f"Gecko/{browser_version}.0 Firefox/{browser_version}.0")
        elif browser_type == 'edge':
            return (f"Mozilla/5.0 (Linux; Android {android_version}; {android_device}) AppleWebKit/537.36 "
                    f"(KHTML, like Gecko) Chrome/{browser_version} Mobile Safari/537.36 EdgA/{browser_version}")

    elif device_type == 'ios':
        ios_versions = ['13.0', '14.0', '15.0', '16.0', '17.0']
        ios_devices = ['iPhone', 'iPad']
        ios_version = random.choice(ios_versions)
        ios_device = random.choice(ios_devices)
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 ({ios_device}; CPU {ios_device} OS {ios_version.replace('.', '_')} like Mac OS X) "
                    f"AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/{browser_version} Mobile/15E148 Safari/604.1")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 ({ios_device}; CPU {ios_device} OS {ios_version.replace('.', '_')} like Mac OS X) "
                    f"AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/{browser_version} Mobile/15E148 Safari/605.1.15")
        elif browser_type == 'safari':
            return (f"Mozilla/5.0 ({ios_device}; CPU {ios_device} OS {ios_version.replace('.', '_')} like Mac OS X) "
                    f"AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{browser_version} Mobile/15E148 Safari/604.1")

    elif device_type == 'windows':
        windows_versions = ['10.0', '11.0']
        windows_version = random.choice(windows_versions)
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    f"Chrome/{browser_version} Safari/537.36")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64; rv:{browser_version}.0) "
                    f"Gecko/{browser_version}.0 Firefox/{browser_version}.0")
        elif browser_type == 'edge':
            return (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    f"Chrome/{browser_version} Safari/537.36 Edg/{browser_version}")

    elif device_type == 'macos':
        macos_versions = ['10.15', '11.0', '12.0', '13.0']
        macos_version = random.choice(macos_versions)
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (Macintosh; Intel Mac OS X {macos_version.replace('.', '_')}) AppleWebKit/537.36 "
                    f"(KHTML, like Gecko) Chrome/{browser_version} Safari/537.36")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (Macintosh; Intel Mac OS X {macos_version.replace('.', '_')}; rv:{browser_version}.0) "
                    f"Gecko/{browser_version}.0 Firefox/{browser_version}.0")
        elif browser_type == 'safari':
            return (f"Mozilla/5.0 (Macintosh; Intel Mac OS X {macos_version.replace('.', '_')}) AppleWebKit/605.1.15 "
                    f"(KHTML, like Gecko) Version/{browser_version} Safari/605.1.15")

    elif device_type == 'linux':
        linux_distributions = ['Ubuntu', 'Fedora', 'Debian', 'CentOS', 'Arch']
        linux_distribution = random.choice(linux_distributions)
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    f"Chrome/{browser_version} Safari/537.36")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (X11; {linux_distribution}; Linux x86_64; rv:{browser_version}.0) "
                    f"Gecko/{browser_version}.0 Firefox/{browser_version}.0")

    return None

def generate_random_device_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

def generate_random_app_version():
    major = random.randint(1, 5)
    minor = random.randint(0, 9)
    patch = random.randint(0, 99)
    return f"{major}.{minor}.{patch}"

def generate_random_build_number():
    return ''.join(random.choices(string.digits, k=8))

def generate_random_locale():
    locales = ['en_US', 'en_GB', 'fr_FR', 'de_DE', 'es_ES', 'it_IT', 'ja_JP', 'ko_KR', 'pt_BR', 'ru_RU']
    return random.choice(locales)

def generate_random_timezone():
    timezones = ['UTC', 'America/New_York', 'Europe/London', 'Asia/Tokyo', 'Australia/Sydney', 'Pacific/Auckland']
    return random.choice(timezones)

def generate_device_info():
    return {
        'user_agent': generate_random_user_agent(),
        'device_id': generate_random_device_id(),
        'app_version': generate_random_app_version(),
        'build_number': generate_random_build_number(),
        'locale': generate_random_locale(),
        'timezone': generate_random_timezone()
    }

# Headers from headers.py
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "if-none-match": 'W/"2cc-L/KMGs6EOmGfZznp6UXxDllJgL4"',
    "referer": "https://prod.snapster.bot/main",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": generate_random_user_agent(),
}

# Functions from lock.py
def _banner():
    banner = r"""
╔══════════════ SNAPSTER BOT ═══════════════╗
║              Bot Automation               ║
║         Developed by @ItbaArts_Dev        ║
╚═══════════════════════════════════════════╝ """ 
    print(Fore.CYAN + Style.BRIGHT + banner + Style.RESET_ALL)
    print(hju + "Snapster Auto Bot".center(48))
    log_line()
    loading_animation("Initializing bot...", 5)

def loading_animation(message, duration):
    animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    index = 0
    while time.time() < end_time:
        try:
            sys.stdout.write(f"\r{bru}{animation[index % len(animation)]} {message}".ljust(50))
            sys.stdout.flush()
        except UnicodeEncodeError:
            sys.stdout.write(f"\r{bru}• {message}".ljust(50))
            sys.stdout.flush()
        index += 1
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * (len(message) + 2) + "\r")
    sys.stdout.flush()

def log_message(message, color=Style.RESET_ALL, status="", end='\n'):
    status_symbol = "✓" if status == "success" else "✗" if status == "failure" else "•"
    sys.stdout.write(f"{color}{status_symbol} {message}{Style.RESET_ALL}{end}")
    sys.stdout.flush()

def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def read_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
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
    color = kwargs.pop('color', Style.RESET_ALL)
    status = kwargs.pop('status', "")
    log_message(message, color, status, **kwargs)

def log_line():
    print(pth + "═" * 45)

async def countdown_timer(seconds):
    while seconds:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        time_left = f"{h:02d}:{m:02d}:{s:02d}"
        print(f"{pth}Please wait for {time_left} ".center(50), flush=True, end="\r")
        seconds -= 1
        await asyncio.sleep(1)
    print(f"{pth}Please wait for {time_left} ".center(50), flush=True, end="\r")

def _number(number):
    return "{:,.0f}".format(number)

# SnapsterBot class from core.py
class SnapsterBot:
    def __init__(self, query_file="data.txt"):
        self.query_file = query_file
        self.headers = headers
        self.query_id = None
        self.user_id = None
        self.proxies = self.load_proxies()
        self.config = read_config()  # Add this line
        loading_animation("Loading configuration...", 3)

    def load_proxies(self):
        try:
            with open("proxies.txt", "r") as f:
                return [line.strip() for line in f]
        except FileNotFoundError:
            log_message("Proxies file not found.", mrh)
            return []

    async def get_proxy_for_account(self, account_number):
        if self.proxies and self.config.get("use_proxy", False):
            return f"http://{self.proxies[account_number % len(self.proxies)]}"
        return None

    async def extract_user_id(self):
        try:
            if self.query_id:
                parsed_query = urllib.parse.parse_qs(self.query_id)
                user_data = parsed_query.get("user", [None])[0]
                if user_data:
                    user_info = json.loads(urllib.parse.unquote(user_data))
                    self.user_id = user_info.get("id")
                else:
                    return None
            else:
                log_message(mrh + f"User ID not found.", mrh)
                return None
        except Exception as e:
            log_message(f"An error occurred. Please check http.log", mrh)
            log_error(f"{e}")
            return None
        
    async def get_user_data(self, session, proxy):
        if not self.user_id:
            log_message(mrh + f"User ID not found.", mrh)
            return
        
        url = f"https://prod.snapster.bot/api/user/getUserByTelegramId?telegramId={self.user_id}"
        self.headers["telegram-data"] = self.query_id 
        
        # Ekstrak username dari query_id
        parsed_query = urllib.parse.parse_qs(self.query_id)
        user_data = parsed_query.get("user", [None])[0]
        telegram_username = None
        if user_data:
            user_info = json.loads(urllib.parse.unquote(user_data))
            telegram_username = user_info.get("username")
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers, proxy=proxy) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('result'):
                            user_data = data['data']
                            snapster_username = user_data.get('username', 'Unknown')
                            points_count = user_data.get('pointsCount', 0)
                            league = user_data.get('currentLeague', {}).get('title', 'Unknown')
                            log_message(hju + f"Telegram Username: {pth}{telegram_username}", hju)
                            log_message(hju + f"Snapster Username: {pth}{snapster_username}", hju)
                            log_message(hju + f"Total points: {pth}{points_count}", hju)
                            log_message(hju + f"Current league: {pth}{league}", hju)
                        else:
                            log_message(mrh + f"Failed to fetch user data. Message: {data.get('message', 'No error message')}", mrh)
                    else:
                        log_message(mrh + f"Error: {response.status}", mrh)
                        log_message(mrh + f"Response body: {await response.text()}", mrh)
            except Exception as e:
                log_message(mrh + f"An error occurred. Please check http.log", mrh)
                log_error(f"{str(e)}")

    async def claim_daily_bonus(self, session, proxy):
        if not self.user_id:
            log_message(mrh + f"User ID not found.", mrh)
            return
        
        url_daily_bonus = "https://prod.snapster.bot/api/dailyQuest/startDailyBonusQuest"
        payload = {
            "telegramId": str(self.user_id)
        }
        self.headers["telegram-data"] = self.query_id

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url_daily_bonus, json=payload, headers=self.headers, proxy=proxy) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('result'):
                            points_claimed = data['data']['pointsClaimed']
                            streak_count = data['data']['user']['dailyBonusStreakCount']
                            log_message(hju + f"Successfully claimed daily bonus {bru}| Points: {pth}{points_claimed} {hju}| Streak: {pth}{streak_count}", hju)
                        else:
                            error_message = data.get('message', 'Unknown error')
                            if 'Not possible to start' in error_message:
                                log_message(kng + f"You have already checked in today", kng)
                            else:
                                log_message(mrh + f"Failed to claim daily bonus!", mrh)
                                log_error(f"{error_message}")
                    else:
                        log_message(mrh + f"Error claiming daily bonus!", mrh)
                        log_error(f"{response.status}")
            except Exception as e:
                log_message(mrh +f"An error occurred. Please check http.log", mrh)
                log_error(f"{str(e)}")

    async def claim_league_bonus(self, session, proxy):
        if not self.user_id:
            log_message(mrh + f"User ID not found.", mrh)
            return
        
        url_leagues = f"https://prod.snapster.bot/api/user/getLeagues?telegramId={self.user_id}"
        self.headers["telegram-data"] = self.query_id

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url_leagues, headers=self.headers, proxy=proxy) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('result'):
                            leagues = data['data']
                            for league in leagues:
                                if league['status'] == 'UNCLAIMED':
                                    league_id = league['leagueId']
                                    league_title = league['title']
                                    bonus_points = league['bonusPoints']
                                    
                                    result, message = await self._claim_league_bonus(session, proxy, league_id)
                                    if result:
                                        log_message(hju + f"Successfully claimed {pth}{bonus_points} {hju}points for {pth}{league_title}.", hju)
                                    else:
                                        log_message(mrh + f"Failed to claim bonus for {pth}{league_title}: {mrh}{message}", mrh)
                                    return
                        else:
                            log_message(mrh + f"Failed to retrieve league information.", mrh)
                    else:
                        log_message(mrh + f"Error fetching leagues: {response.status}", mrh)
            except Exception as e:
                log_message(mrh +f"An error occurred. Please check http.log", mrh)
                log_error(f"{str(e)}")

    async def _claim_league_bonus(self, session, proxy, league_id):
        url_claim = "https://prod.snapster.bot/api/user/claimLeagueBonus"
        payload = {
            "telegramId": str(self.user_id),
            "leagueId": league_id
        }

        try:
            async with session.post(url_claim, json=payload, headers=self.headers, proxy=proxy) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('result'):
                        return True, hju + f"Successfully claimed {pth}{data['data']['pointsClaimed']} {hju}points"
                    else:
                        error_message = data.get('message', 'Unknown error')
                        return False, error_message
                else:
                    return False, f"Error: {response.status}"
        except Exception as e:
            log_message(mrh +f"An error occurred. Please check http.log", mrh)
            log_error(f"{str(e)}")
            return False

    async def claim_mining_bonus(self, session, proxy):
        if not self.user_id:
            log_message(mrh + f"User ID not found", mrh)
            return
        
        url = "https://prod.snapster.bot/api/user/claimMiningBonus"
        payload = {
            "telegramId": str(self.user_id)
        }
        self.headers["telegram-data"] = self.query_id

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=self.headers, json=payload, proxy=proxy) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('result'):
                            points_claimed = data['data']['pointsClaimed']
                            mining_speed = data['data']['user']['currentLeague']['miningSpeed']
                            log_message(hju + f"Successfully claimed Mining bonus | {bru}Points: {pth}{points_claimed} {hju}", hju)
                            log_message(hju + f"Mining speed: {pth}{mining_speed}x", hju)
                        else:
                            log_message(mrh + f"Failed! {data.get('message', 'Unknown error')}", mrh)
                    else:
                        log_message(mrh + f"Error: {response.status}", mrh)
            except Exception as e:
                log_message(mrh +f"An error occurred. Please check http.log", mrh)
                log_error(f"{str(e)}")

    async def get_tasks(self, session, proxy):
        if not self.user_id:
            log_message(mrh + f"User ID not found", mrh)
            return
        
        url = f"https://prod.snapster.bot/api/quest/getQuests?telegramId={self.user_id}"
        self.headers["telegram-data"] = self.query_id 

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers, proxy=proxy) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('result'):
                            tasks = data['data']
                            for task in tasks:
                                task_id = task['id']
                                task_name = task['title']
                                task_status = task['status']
                                if task_status == 'EARN':
                                    result, message = await self.start_quest(session, proxy, task_id)
                                elif task_status == 'UNCLAIMED':
                                    result, message = await self.claim_quest_bonus(session, proxy, task_id)
                                else:
                                    result, message = False, hju + f"COMPLETE"
                                
                                log_message(hju + f"Task: {pth}{task_name}", hju)
                                log_message(bru + f"Status: {hju}{task_status} - {kng}{'Started' if task_status == 'EARN' else 'CLAIMED'} {hju}| {pth}{message}", bru)
                        else:
                            log_message(mrh + "Failed to fetch tasks list", mrh)
                    else:
                        log_message(mrh + f"{response.status}", mrh)
            except Exception as e:
                log_message(mrh +f"An error occurred. Please check http.log", mrh)
                log_error(f"{str(e)}")

    async def start_quest(self, session, proxy, quest_id):
        url = "https://prod.snapster.bot/api/quest/startQuest"
        payload = {
            "telegramId": str(self.user_id),
            "questId": quest_id
        }

        try:
            async with session.post(url, json=payload, headers=self.headers, proxy=proxy) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('result'):
                        return True, hju + f"Success | {pth}{data['data']['status']}"
                    else:
                        error_message = data.get('message', 'Unknown error')
                        if 'Referral Count threshold' in error_message:
                            return False, mrh + f"Not achieved."
                        elif 'The wallet is not' in error_message:
                            return False, mrh + f"Wallet not connected."
                        elif 'Quest not found' in error_message:
                            return False, mrh + f"Failed! Quest not found."
                        else:
                            return False, mrh + f"{error_message}"
                else:
                    return False, mrh + f"Error starting quest: {htm}{response.status}"
        except Exception as e:
            log_message(mrh +f"An error occurred. Please check http.log", mrh)
            log_error(f"{str(e)}")
            return False

    async def claim_quest_bonus(self, session, proxy, quest_id):
        url = "https://prod.snapster.bot/api/quest/claimQuestBonus"
        payload = {
            "telegramId": str(self.user_id),
            "questId": quest_id
        }

        try:
            async with session.post(url, json=payload, headers=self.headers, proxy=proxy) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('result'):
                        return True, hju + f"CLAIMED | Points: {pth}{data['data']['pointsClaimed']}"
                    else:
                        error_message = data.get('message', 'Unknown error')
                        if 'already claimed' in error_message.lower():
                            return False, mrh + f"Failed! Bonus already claimed."
                        elif 'Quest not found' in error_message:
                            return False, mrh + f"Failed! Quest not found."
                        else:
                            return False, mrh + f"{error_message}"
                else:
                    return False, mrh + f"Error : {response.status}"
        except Exception as e:
            log_message(mrh +f"An error occurred. Please check http.log", mrh)
            log_error(f"{str(e)}")
            return False
        
    async def claim_referral_points(self, session, proxy):
        if not self.user_id:
            log_message(mrh + f"User ID not found.", mrh)
            return
        
        url = "https://prod.snapster.bot/api/referral/claimReferralPoints"
        payload = {
            "telegramId": str(self.user_id)
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, headers=self.headers, proxy=proxy) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('result'):
                            points_claimed = data['data'].get('pointsClaimed', 0)
                            log_message(hju + f"Referral reward point | {bru}Points: {pth}{points_claimed}", hju)
                        else:
                            log_message(mrh + f"Failed to claim referral points.", mrh)
                    else:
                        log_message(f"Error: Failed to claim referral : status {response.status}", mrh)
            except Exception as e:
                log_message(mrh +f"an error occurred check http.log", mrh)
                log_error(f"{str(e)}")

    def log_header(self, title):
        log_message(htm + f"{'═' * 10} {title} {'═' * 10}", htm)

    def log_footer(self):
        log_message(htm + "═" * 27, htm)

    async def run(self):
        tasks_enabled = self.config.get("auto_complete_tasks", False)
        delay = self.config.get("account_delay", 5)
        loop_duration = self.config.get("loop_countdown", 3800)

        query_ids = []
        try:
            with open(self.query_file, 'r') as file: 
                query_ids = [line.strip() for line in file]
        except FileNotFoundError:
            log_message(f"File {self.query_file} not found!", mrh)
            return

        account_number = 0
        total = len(query_ids)

        while True:
            try:
                for query_id in query_ids:
                    self.query_id = query_id
                    proxy = await self.get_proxy_for_account(account_number)
                    if proxy:
                        host = proxy.split("@")[-1].split(":")[0]
                    else:
                        host = "No Proxy"
                    
                    connector = aiohttp.TCPConnector(ssl=False)
                    async with aiohttp.ClientSession(connector=connector) as session:
                        self.log_header(f"Account {account_number + 1}/{total}")
                        log_message(f"{kng}╔{'═' * 27}╗", kng)
                        log_message(f"{kng}║ {pth}Processing account {account_number + 1} of {total} {kng}║", kng)  
                        log_message(f"{kng}╚{'═' * 27}╝", kng)
                        log_message(hju + f"Using proxy: {host}", hju)
                        await self.extract_user_id()
                        await self.get_user_data(session, proxy)
                        await self.claim_daily_bonus(session, proxy)
                        await self.claim_league_bonus(session, proxy)
                        await self.claim_mining_bonus(session, proxy)

                        if tasks_enabled:
                            await self.get_tasks(session, proxy)
                        else:
                            log_message(kng + f'Auto complete tasks is not activated!', kng)
                        
                        await self.claim_referral_points(session, proxy)
                        self.log_footer()
                        
                        account_number += 1
                        await countdown_timer(delay)

                await countdown_timer(loop_duration)
            except Exception as e:
                log_message(kng + f"Error: {e}", kng)

async def main():
    bot = SnapsterBot() 
    await bot.run()

if __name__ == "__main__":
    _clear()
    _banner()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log(mrh + f"Bot interrupted by user.")
        sys.exit()

