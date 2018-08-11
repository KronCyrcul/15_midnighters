import datetime
import pytz
import requests


def load_attempts(url):
    page = 1
    while True:
        params = {"page": page}
        response = requests.get(url, params=params)
        for attempt in response.json()["records"]:
            yield {
                "username": attempt["username"],
                "timestamp": attempt["timestamp"],
                "timezone": attempt["timezone"],
            }
        page+=1
        if page == (response.json()["number_of_pages"] + 1):
            break


def get_midnighters(users_attempts):
    midnighters = []
    for attempt in users_attempts:
        attempt_timezone = attempt["timezone"]
        attempt_timestamp = attempt["timestamp"]
        user_timezone = pytz.timezone(attempt_timezone)
        users_date = datetime.datetime.fromtimestamp(attempt_timestamp,
            tz=user_timezone)
        if 0 <= users_date.hour <= 7:
            midnighters.append(attempt["username"])
    return set(midnighters)


if __name__ == "__main__":
    request_url = "https://devman.org/api/challenges/solution_attempts/"
    users_attempts = load_attempts(request_url)
    midnighters = get_midnighters(users_attempts)
    print("Send their attempts after 12pm:")
    for user in midnighters:
        print(user)
