import aiohttp
import urllib.parse
import json
from colorama import *
from src.headers import headers
from src.lock import (
    countdown_timer, 
    read_config, log_error,
    log_pesan, mrh, pth, hju, kng, bru, htm, log_line, loading_animation
    )

init(autoreset=True)
config = read_config()

class SnapsterBot:
    def __init__(self, query_file="data.txt"):
        self.query_file = query_file
        self.headers = headers
        self.query_id = None
        self.user_id = None
        self.proxies = self.load_proxies()
        loading_animation("Loading configuration...", 3)

    def load_proxies(self):
        try:
            with open("proxies.txt", "r") as f:
                return [line.strip() for line in f]
        except FileNotFoundError:
            log_pesan("Proxies file not found.", mrh)
            return []

    async def get_proxy_for_account(self, account_number):
        if self.proxies and config.get("use_proxy", False):
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
                log_pesan(mrh + f"User ID not found.", mrh)
                return None
        except Exception as e:
            log_pesan(f"An error occurred. Please check http.log", mrh)
            log_error(f"{e}")
            return None
        
    async def get_user_data(self, session, proxy):
        if not self.user_id:
            log_pesan(mrh + f"User ID not found.", mrh)
            return
        
        url = f"https://prod.snapster.bot/api/user/getUserByTelegramId?telegramId={self.user_id}"
        self.headers["telegram-data"] = self.query_id 
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers, proxy=proxy) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('result'):
                            user_data = data['data']
                            username = user_data.get('username', 'Unknown')
                            points_count = user_data.get('pointsCount', 0)
                            league = user_data.get('currentLeague').get('title')
                            log_pesan(hju + f"Username: {pth}{username}", hju)
                            log_pesan(hju + f"Total points: {pth}{points_count}", hju)
                            log_pesan(hju + f"Current league: {pth}{league}", hju)
                        else:
                            log_pesan(mrh + f"Failed to fetch user data.", mrh)
                    else:
                        log_pesan(mrh + f"Error: {response.status}", mrh)
            except Exception as e:
                log_pesan(mrh +f"An error occurred. Please check http.log", mrh)
                log_error(f"{str(e)}")

    async def claim_daily_bonus(self, session, proxy):
        if not self.user_id:
            log_pesan(mrh + f"User ID not found.", mrh)
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
                            log_pesan(hju + f"Successfully claimed daily bonus {bru}| Points: {pth}{points_claimed} {hju}| Streak: {pth}{streak_count}", hju)
                        else:
                            error_message = data.get('message', 'Unknown error')
                            if 'Not possible to start' in error_message:
                                log_pesan(kng + f"You have already checked in today", kng)
                            else:
                                log_pesan(mrh + f"Failed to claim daily bonus!", mrh)
                                log_error(f"{error_message}")
                    else:
                        log_pesan(mrh + f"Error claiming daily bonus!", mrh)
                        log_error(f"{response.status}")
            except Exception as e:
                log_pesan(mrh +f"An error occurred. Please check http.log", mrh)
                log_error(f"{str(e)}")

    async def claim_league_bonus(self, session, proxy):
        if not self.user_id:
            log_pesan(mrh + f"User ID not found.", mrh)
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
                                        log_pesan(hju + f"Successfully claimed {pth}{bonus_points} {hju}points for {pth}{league_title}.", hju)
                                    else:
                                        log_pesan(mrh + f"Failed to claim bonus for {pth}{league_title}: {mrh}{message}", mrh)
                                    return
                        else:
                            log_pesan(mrh + f"Failed to retrieve league information.", mrh)
                    else:
                        log_pesan(mrh + f"Error fetching leagues: {response.status}", mrh)
            except Exception as e:
                log_pesan(mrh +f"An error occurred. Please check http.log", mrh)
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
            log_pesan(mrh +f"An error occurred. Please check http.log", mrh)
            log_error(f"{str(e)}")
            return False

    async def claim_mining_bonus(self, session, proxy):
        if not self.user_id:
            log_pesan(mrh + f"User ID not found", mrh)
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
                            log_pesan(hju + f"Successfully claimed Mining bonus | {bru}Points: {pth}{points_claimed} {hju}", hju)
                            log_pesan(hju + f"Mining speed: {pth}{mining_speed}x", hju)
                        else:
                            log_pesan(mrh + f"Failed! {data.get('message', 'Unknown error')}", mrh)
                    else:
                        log_pesan(mrh + f"Error: {response.status}", mrh)
            except Exception as e:
                log_pesan(mrh +f"An error occurred. Please check http.log", mrh)
                log_error(f"{str(e)}")

    async def get_tasks(self, session, proxy):
        if not self.user_id:
            log_pesan(mrh + f"User ID not found", mrh)
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
                                
                                log_pesan(hju + f"Tasks {pth}{task_name}", hju)
                                log_pesan(bru + f"Status: {hju}{task_status} - {kng}{'Started' if task_status == 'EARN' else 'CLAIMED'} {hju}| {pth}{message}", bru)
                        else:
                            log_pesan(mrh + "Failed to fetch tasks list", mrh)
                    else:
                        log_pesan(mrh + f"{response.status}", mrh)
            except Exception as e:
                log_pesan(mrh +f"An error occurred. Please check http.log", mrh)
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
            log_pesan(mrh +f"An error occurred. Please check http.log", mrh)
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
            log_pesan(mrh +f"An error occurred. Please check http.log", mrh)
            log_error(f"{str(e)}")
            return False
        
    async def claim_referral_points(self, session, proxy):
        if not self.user_id:
            log_pesan(mrh + f"User ID not found.", mrh)
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
                            log_pesan(hju + f"Referral reward point | {bru}Points: {pth}{points_claimed}", hju)
                        else:
                            log_pesan(mrh + f"Failed to claim referral points.", mrh)
                    else:
                        log_pesan(f"Error: Failed to claim referral : status {response.status}", mrh)
            except Exception as e:
                log_pesan(mrh +f"an error occurred check http.log", mrh)
                log_error(f"{str(e)}")

    # Menambahkan fungsi untuk memformat header
    def log_header(self, title):
        log_pesan(htm + f"{'═' * 10} {title} {'═' * 10}", htm)

    # Menambahkan fungsi untuk memformat footer
    def log_footer(self):
        log_pesan(htm + "═" * 27, htm)

    async def run(self):
        tasks_enabled = config.get("auto_complete_tasks", False)
        delay = config.get("account_delay", 5)
        loop_duration = config.get("loop_countdown", 3800)

        query_ids = []
        try:
            with open(self.query_file, 'r') as file: 
                query_ids = [line.strip() for line in file]
        except FileNotFoundError:
            log_pesan(f"File {self.query_file} not found!", mrh)
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
                        log_pesan(f"{kng}╔{'═' * 27}╗", kng)
                        log_pesan(f"{kng}║ {pth}Processing account {account_number + 1} of {total} {kng}║", kng)  
                        log_pesan(f"{kng}╚{'═' * 27}╝", kng)
                        log_pesan(hju + f"Using proxy: {host}", hju)
                        await self.extract_user_id()
                        await self.get_user_data(session, proxy)
                        await self.claim_daily_bonus(session, proxy)
                        await self.claim_league_bonus(session, proxy)
                        await self.claim_mining_bonus(session, proxy)

                        if tasks_enabled:
                            await self.get_tasks(session, proxy)
                        else:
                            log_pesan(kng + f'Auto complete tasks is not activated!', kng)
                        
                        await self.claim_referral_points(session, proxy)
                        self.log_footer()
                        
                        account_number += 1
                        await countdown_timer(delay)

                await countdown_timer(loop_duration)
            except Exception as e:
                log_pesan(kng + f"Error: {e}", kng)

async def main():
    bot = SnapsterBot() 
    await bot.run()