import datetime
import pytz
import requests


def load_attempts(url):
    page = 1
    params = {"page": page}
    response = requests.get(url, params=params)
    while page != (response.json()["number_of_pages"] + 1):
        params = {"page": page}
        response = requests.get(url, params=params)
        for attempt in response.json()["records"]:
            yield {
                "username": attempt["username"],
                "timestamp": attempt["timestamp"],
                "timezone": attempt["timezone"],
            }
        page+=1


def get_midnighters(users_attempts):
    midnighters = []
    for attempt in users_attempts:
        attempt_timezone = attempt["timezone"]
        attempt_timestamp = attempt["timestamp"]
        user_timezone = pytz.timezone(attempt_timezone)
        users_date = datetime.datetime.fromtimestamp(attempt_timestamp,
            tz=user_timezone)
        if (users_date.hour <= 7 and users_date.hour >= 0 and
                attempt["username"] not in midnighters):
            midnighters.append(attempt["username"])
    return midnighters

if __name__ == "__main__":
    request_url = "https://devman.org/api/challenges/solution_attempts/"
    response = requests.get(request_url)
    users_attempts = load_attempts(request_url)
    midnighters = get_midnighters(users_attempts)
    print("Send their attempts after 12pm:")
    for user in midnighters:
        print(user)
