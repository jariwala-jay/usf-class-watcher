import requests
from bs4 import BeautifulSoup
import time
import os

# --- CONFIG ---
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_USER_ID = os.getenv('TELEGRAM_USER_ID')

SEARCH_URL = "https://usfweb.usf.edu/DSS/StaffScheduleSearch/StaffSearch/Results"


# Course titles to watch for
WATCHLIST = ["Mobile Biometrics", "Human-Computer Interaction","Cryptographic Hardware","Cryptographic Hardware & Embedded Systems"]

# Form data (same as your payload)
FORM_DATA = {
    "P_SEMESTER": "202508",
    "P_SESSION": "1",
    "P_CAMPUS": "",
    "P_COL": "AI",
    "P_DEPT": "",
    "p_status": "O",
    "p_ssts_code": "A",
    "P_CRSE_LEVL": "GR",
    "P_REF": "",
    "P_SUBJ": "",
    "P_NUM": "",
    "P_TITLE": "",
    "P_CR": "",
    "p_insm_x_inad": "YAD",
    "p_insm_x_incl": "YCL",
    "p_insm_x_inhb": "YHB",
    "p_insm_x_inpd": "YPD",
    "p_insm_x_innl": "YNULL",
    "p_insm_x_inot": "YOT",
    "p_day_x": "no_val",
    "p_day": "no_val",
    "p_daym": "M",
    "p_dayt": "T",
    "p_dayw": "W",
    "p_dayr": "R",
    "p_dayf": "F",
    "P_TIME1": "",
    "P_INSTRUCTOR": "",
    "P_UGR": ""
}

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_USER_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print("Failed to send Telegram message:", response.text)

def check_courses():
    response = requests.post(SEARCH_URL, data=FORM_DATA)
    soup = BeautifulSoup(response.text, 'html.parser')

    found = []

    for course in WATCHLIST:
        if course.lower() in soup.text.lower():
            found.append(course)

    if found:
        message = "✅ Course(s) Available:\n" + "\n".join(found)
        send_telegram_message(message)
        print(message)
    else:
        print("No matching courses found.")

# Run every 10 minutes
if __name__ == "__main__":
    while True:
        print("Checking for course availability...")
        check_courses()
        time.sleep(60)  # 10 minutes
