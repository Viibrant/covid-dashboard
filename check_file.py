from datetime import date, datetime
from requests import get
from requests.exceptions import RequestException
from os.path import isfile
from os import stat
import time
import json
import logging
import pandas as pd
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

def retrieve_data(endpoint):
    response = get(endpoint, allow_redirects=True, timeout=10, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size, unit="iB", unit_scale=True)
    with open("statistics.json", "wb") as json_file:
        for i in response.iter_content(block_size):
            progress_bar.update(len(i))
            json_file.write(i)

def read_file():
    with open("statistics.json") as f:
        data = json.load(f)
    return data

def get_dataset(endpoint):
    file_exists = isfile("statistics.json")
    empty = not (file_exists and stat("statistics.json").st_size != 0)
    retries = 1

    if file_exists:
        created = datetime.fromtimestamp(stat("statistics.json").st_mtime)
        old = created == date.today()

    if not file_exists or empty or old:
        try:
            data = retrieve_data(endpoint)
        except RequestException as e:
            wait = retries * 2
            print("Error! Waiting %s secs and re-trying..." % wait)
            time.sleep(wait)
            retries += 1
            if retries == 5:
                raise e        
    data = read_file()["body"]
    return pd.DataFrame(data)

    # Check whether file was created today





if __name__ == "__main__":
    metrics = ["newCasesBySpecimenDate", "newPeopleVaccinatedCompleteByVaccinationDate"]
    endpoint = "https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric={metrics}&format=json".format(
        metrics="&metric=".join(metrics)
    )
    get_dataset(endpoint)
