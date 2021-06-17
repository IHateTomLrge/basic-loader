from playwright.sync_api import sync_playwright
import requests
from faker import Faker
import time

class C:
    ok = '\033[92m'
    error = '\033[91m'

def get_cookies(url, user_agent, max_retry=10):
    with sync_playwright() as p:
        print("Creating client...")
        browser = p.webkit.launch()
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()
        print("Getting page...")
        page.goto(url)
        max_retry = max_retry / 3
        retry = 0
        try:
            while page.title() == "Just a moment...":
                time.sleep(3)
                if retry > max_retry:
                    for c in context.cookies():
                        if c.get("name") == "__cf_bm":
                            print(C.ok + "[GOOD] Cookies loaded" + '\033[0m')
                            return context.cookies()
                    print(C.error + "[ERROR LOADING COOKIES] Max retry exceeded" + '\033[0m')
                    return False
                retry += 1
        except Exception:
            for c in context.cookies():
                if c.get("name") == "__cf_bm":
                    print(C.ok + "[GOOD] Cookies loaded" + '\033[0m')
                    return context.cookies()
            print(C.error + "[ERROR LOADING COOKIES] Failed to solve cloudflare" + '\033[0m')
            return False
        cookies = context.cookies()
        browser.close()
    print(C.ok + "[GOOD] Cookies loaded" + '\033[0m')
    return cookies


def create_clients():
    faker = Faker()
    user_agent = faker.user_agent()
    client = requests.Session()
    client.headers.update({
        "User-Agent": user_agent,
        "Accept": "*/*"
    })
    return client, user_agent
