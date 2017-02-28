import requests
import cStringIO
from bs4 import BeautifulSoup
import datetime
import re
from urlparse import urljoin
import json
from censorcheck.models import OONIRecord
from dateutil.parser import parse

OONI_MEASUREMENTS_URL = "https://measurements.ooni.torproject.org/"
PATTERN = re.compile("^\d{8}T\d{6}Z\-MY\-AS\d+\-web_connectivity")

def main():
    date_str = fetch_latest_directory()
    print(date_str)
    if date_str:
        urls = read_directory(date_str)
        print(urls)
        for url in urls:
            fetch_and_save_data(url)

def fetch_and_save_data(url):
    r = requests.get(url)
    content = cStringIO.StringIO(r.content)
    for line in content:
        data = json.loads(line)
        failure = is_failure(data)
        if failure:
            status = "BLOCKED"
        else:
            status = "OPEN"
        record = OONIRecord(
                report_id = data["report_id"],
                test_start_time = parse(data["test_start_time"]),
                input_url = data["input"],
                software_name = data["software_name"],
                test_name = data["test_name"],
                probe_asn = data["probe_asn"],
                probe_cc = data["probe_cc"],
                status = status
                )
        record.save()
    
def fetch_latest_directory():
    url = OONI_MEASUREMENTS_URL
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    a = soup.find_all("a")
    date_str = a[-1].text[:-1] # Remove trailing / in dir name, name is in yyyy-mm-dd/
    if to_process(date_str):
        return date_str
    return ''

def read_directory(date_dir):
    url = urljoin(OONI_MEASUREMENTS_URL, date_dir+"/")
    print(url)
    r = requests.get(url)
    print(r.status_code)
    soup = BeautifulSoup(r.content)
    a = soup.find_all("a")
    temp = []
    print(a)
    for i in a:
        print(i.text)
        if i.text == "../":
            continue
        print(i.text)
        if PATTERN.match(i.text):
            target_url = "%s/%s/%s" % (OONI_MEASUREMENTS_URL, date_dir, i["href"])
            temp.append(target_url)

    return temp

def to_process(date_str):
    check = OONIRecord.objects.all()
    # empty_result put anything
    if not check:
        return True
    latest_record = OONIRecord.objects.latest("test_start_time")
    latest_date = latest_record.test_start_time.date
    test_date = parse(date_str)
    return today <= latest_date

def is_failure(data):
    test_keys = data["test_keys"]
    if test_keys["accessible"]:
        return False
    return True

if __name__ == "__main__":
    main()
