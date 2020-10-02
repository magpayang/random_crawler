
from requests_html import HTML, HTMLSession
import time
import random
import csv

session = HTMLSession()


def func_0(input_url):
    """  """
    r = session.get(input_url)
    all_links = list(r.html.absolute_links)
    my_random = random.randint(0, len(all_links))
    new_url = all_links[my_random]

    return r, new_url


def func_1(input_response):
    """ extract information of this url """
    return input_response.apparent_encoding, input_response.headers['date']


def write_to_file(output_file, data, return_func=None, header=None, mode="a", write_header=False, encoding="utf-8"):
    """ pass """
    with open(output_file, mode, encoding=encoding, newline="") as file:
        csv_writer = csv.writer(file)
        if write_header:
            csv_writer.writerow(header)
        csv_writer.writerow(data)
        if return_func:
            return return_func


# settings
starting_url = "https://wikipedia.org"
output_file_0 = "crawl_0.csv"
header_0 = ["count", "date today", "url", "apparent_encoding", "r.headers['date']"]

delay = 6
count = 0

response, new_url = func_0(starting_url)

# run
trap = 0
while True:
    if trap == 0:
        first_time = True
        trap = 1
    else:
        first_time = False

    date_today = time.asctime()

    response_apparent_encoding, response_header_date = func_1(response)
    data_to_write = [count, date_today, new_url, response_apparent_encoding, response_header_date]

    try:
        response, new_url = write_to_file(output_file=output_file_0, data=data_to_write, return_func=func_0(new_url),
                                          header=header_0, mode="a", write_header=first_time, encoding="utf-8")
    except:
        print(Exception)
        print(count, date_today, new_url)

    time.sleep(delay)
    count += 1
