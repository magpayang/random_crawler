from requests_html import HTMLSession
import csv
import py_notes
import time

# import requests

starting_url = "https://en.wikipedia.org/wiki/"
starting_url_filter = starting_url
picture_filter = ".jpg"
true_image_link_filter = "https://upload.wikimedia.org/wikipedia/commons/"

image_folder_name = "./pics/"
log_file_name = image_folder_name + "main_page.csv"

delay = 6

session = HTMLSession()


def func_0(url, filter_string):
    """ given url, produce all absolute links, then return links that match the filter string """
    try:
        resp = session.get(url)
    except:
        resp.close()  # attempt to fix
        resp = session.get(url)  # retry
    finally:
        all_links = resp.html.absolute_links
        filtered_links = list(filter(lambda entry: filter_string in entry, all_links))
        return filtered_links


def filter_array(input_array, filter_string):
    """ given an input_array, sort between items that contains the filter string and those that don't """
    array_rej = []
    array_bin1 = []
    for entry in input_array:
        if filter_string in entry:
            array_bin1.append(entry)
        else:
            array_rej.append(entry)
    return array_bin1, array_rej


def func_1(input_link, filter_0, filter_1, enable_debug=False):
    """ given an input_link, returns valid_links minus image_links, and image_links """
    valid_links = func_0(input_link, filter_0)
    image_links, non_image_links = filter_array(valid_links, filter_1)  # filters if link contains ".jpg"

    return image_links, non_image_links


def func_2(input_link, folder_name, count=None, enable_debug=False):
    """ given image link, get the bytes response, produce the image name, then save the file """
    try:
        resp = session.get(input_link)
    except:
        resp.close()
        resp = session.get(input_link)
    finally:
        image_name = folder_name+input_link.split("/")[-1]

        if "%28" in image_name and "%29" in image_name:
            image_name = image_name.replace("%28", "(")
            image_name = image_name.replace("%29", ")")

        if "%2C" in image_name:
            image_name = image_name.replace("%2C", ",")

        with open(image_name, 'wb') as file:
            file.write(resp.content)
            if enable_debug:
                print(count, image_name)


def func_3(input_url, filter):
    """ two stage filter aimed at extracting the link that contains the highest resolution """
    tempo_array_0 = []
    tempo_array_1 = []

    name = input_url.split(":")[-1]
    if "(" in name and ")" in name:
        name = name.replace("(", "%28")
        name = name.replace(")", "%29")

    if "," in name:
        name = name.replace(",", "%2C")

    try:
        resp = session.get(input_url)
    except:
        resp.close()
        resp = session.get(input_url)
    finally:
        all_links = resp.html.absolute_links

        for entry in all_links:
            if name == entry.split("/")[-1]:
                tempo_array_0.append(entry)
            else:
                pass  # rejects

        for entry in tempo_array_0:
            if filter in entry:
                tempo_array_1.append(entry)

    return tempo_array_1


def catalogue_links(input_links, output_file):
    """ pass """
    with open(output_file, 'a', encoding="UTF-8", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["count", "image name", "url", "date", "delay used"])
        count = 0
        for entry in input_links:
            name = entry.split(":")[-1]
            csv_writer.writerow([count, name, entry, time.asctime(), delay])
            count += 1


def main():
    """ read my lips """
    starting_url_image_links, starting_url_non_image_links = func_1(starting_url, starting_url_filter, picture_filter,
                                                                    enable_debug=True)

    catalogue_links(starting_url_image_links, log_file_name)

    # this is a debug line, listed here must match the output of func_2
    # not matching indicates a skip
    print("urls found")
    py_notes.enu(starting_url_image_links)
    print("downloading...")

    counter = 0
    for entry in starting_url_image_links:
        time.sleep(delay)

        true_link = func_3(entry, true_image_link_filter)

        if len(true_link) == 1:  # assumed we have only one entry here
            func_2(true_link[0], image_folder_name, counter, enable_debug=True)
        else:
            print("Failed to save file: ")
            print(counter, entry, true_link)
        counter += 1

    print("Done")
    print()

    return starting_url_non_image_links


if __name__ == "__main__":
    main()
