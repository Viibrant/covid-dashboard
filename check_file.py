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

path = "data/statistics.json"

def retrieve_data(endpoint):
    response = get(endpoint, allow_redirects=True, timeout=10, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size, unit="iB", unit_scale=True)
    logging.info("Attempting to retrieve data")
    with open(path, "wb") as json_file:
        for i in response.iter_content(block_size):
            progress_bar.update(len(i))
            json_file.write(i)
    logging.info("Successfully retrieved data")
def read_file():
    logging.info("Reading data...")
    with open(path) as f:
        data = json.load(f)
    logging.info("Parsed as JSON")
    return data

def get_dataset(endpoint):
    file_exists = isfile(path)
    empty = not (file_exists and stat(path).st_size != 0)
    retries = 1

    if file_exists:
        logging.info("Existing file detected")
        created = datetime.fromtimestamp(stat(path).st_mtime)
        old = created == date.today()

    if not file_exists or empty or old:
        try:
            data = retrieve_data(endpoint)
        except RequestException as e:
            wait = retries * 2
            logging.warning("Error! Waiting %s secs and re-trying..." % wait)
            time.sleep(wait)
            retries += 1
            if retries == 5:
                raise e        
    data = read_file()["body"]
    return pd.DataFrame(data)


if __name__ == "__main__":
    metrics = ["newCasesBySpecimenDate", "newPeopleVaccinatedCompleteByVaccinationDate"]
    endpoint = "https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric={metrics}&format=json".format(
        metrics="&metric=".join(metrics)
    )
    get_dataset(endpoint)
