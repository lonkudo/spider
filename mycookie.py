import json
from os import path

def loadcookie(driver,cookie_file):
    # Step 2: Inject cookies
    cookie_file_path = path.join(path.dirname(__file__), "cookies", cookie_file)
    with open(cookie_file_path, "r", encoding="utf-8") as f:
        cookies = json.load(f)
        for c in cookies:
            for key in ["sameSite", "storeId", "hostOnly", "session", "expirationDate"]:
                c.pop(key, None)
            driver.add_cookie(c)
