from datetime import date, datetime, timedelta
from requests import get
from os.path import isfile, getctime
import time
import json
import pandas as pd

def get_dataset(endpoint):
    file_exists = isfile("statistics.json")
    retries = 1
    latest = True

    if file_exists:
        with open("statistics.json") as json_file:
            data = json.load(json_file)

            # Read latest date from statistics.json and convert to Date object
            latest_date = datetime.strptime(
                data[0]['date'], "%Y-%m-%d").date()

            # Get exact creation time then parse only date
            creation_date = getctime("statistics.json")
            creation_date = datetime.fromtimestamp(creation_date).date()
            # Data is always retrieved a day behind
            #   therefore if statistics.json is up to date then
            #       current_date == latest_date + 1 day
            if date.today() == latest_date + timedelta(days=1):
                print("**** Dataset is up to date")
                # Convert dictionary to a Pandas DataFrame, far more efficient
                return pd.DataFrame(data)
            # Otherwise dataset itself may be outdated but retrieved today
            else:
                if date.today() == creation_date:
                    print("**** Created today but outdated data")
                    return pd.DataFrame(data)
                else:
                    print("**** Dataset is outdated, downloading...")
                    latest = False

    while not latest or not file_exists:
        print("File exists:%s\nLatest version:%s" % (file_exists, latest))
        # Attempt to retrieve COVID Statistics from NHS, waiting time grows incrementally
        try:
            response = get(endpoint, allow_redirects=True, timeout=10)
            data = json.loads(response.text)['body']
            with open("statistics.json", "w") as json_file:
                json.dump(data, json_file)
            return pd.DataFrame(data)

        except Exception as e:
            wait = retries * 2
            print('Error! Waiting %s secs and re-trying...' % wait)
            time.sleep(wait)
            retries += 1
            if retries == 5:
                raise e 