import datetime
import pytz
import requests


def load_attempts(url, number_of_pages):
    pages = number_of_pages
    for page in range(1, pages+1):
        params = {"page": page}
        response = requests.get(url, params=params)
        for attemp in response.json()["records"]:
            yield {
                "username": attemp["username"],
                "timestamp": attemp["timestamp"],
                "timezone": attemp["timezone"],
            }


def get_midnighters(users_attempts):
    for attemp in users_attempts:
        attemp_timezone = attemp["timezone"]
        attemp_timestamp = attemp["timestamp"]
        utc_date = datetime.datetime.utcfromtimestamp(attemp_timestamp)
        au_timezone = pytz.timezone(attemp_timezone)
        au_date = au_timezone.normalize(utc_date.astimezone(au_timezone))
        if au_date.hour <= 7 and au_date.hour >= 0:
            yield attemp["username"]

if __name__ == "__main__":
    request_url = "https://devman.org/api/challenges/solution_attempts/"
    response = requests.get(request_url)
    number_of_pages = response.json()["number_of_pages"]
    users_attempts = load_attempts(request_url, number_of_pages)
    midnighters = get_midnighters(users_attempts)
    for user in midnighters:
        print(user)
