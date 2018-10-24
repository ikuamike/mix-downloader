#!/usr/bin/env python3
##############################
#
# Author: Michael Ikua
# Github: ikuamike
#
# ############################


# ========== Imports ==========

from bs4 import BeautifulSoup
import os
import pprint
import requests
import sys

# ========== Main variables ==========

site_url = "http://www.deejayjoemfalme.com"
mixes_page_url = "http://www.deejayjoemfalme.com/index.php/mixes"

# ========== Functions ==========


def download_mix(url, filename):
    home = os.getenv('HOME')
    if not os.path.exists(home + '/Music/The Double Trouble Mixxtapes'):
        os.mkdir(home + '/Music/The Double Trouble Mixxtapes')

    default_download_location = home + '/Music/The Double Trouble Mixxtapes'
    print('\n[*] Downloading ' + filename + ' to ' + default_download_location + '\n')
    filename = default_download_location + '/' + filename

    with open(filename, 'wb') as f:
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')
        dl = 0
        total_length = int(total_length)
        for data in response.iter_content(chunk_size=1024):
            dl += len(data)
            f.write(data)
            done = int(50 * dl / total_length)
            sys.stdout.write('\t\r[{}{}]'.format('█' * done, '.' * (50-done)))
            sys.stdout.flush()


def extract_urls(html, search_phrase):
    """
    Functions takes in html content and extracts urls
    """
    all_urls = []
    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.find_all('a'):
        # loop over all links and get only those for mix download
        url = link['href'].replace(' ', '%20')
        if search_phrase in url:
            all_urls.append(url)
    return sorted(list(set(all_urls))) # sort to get latest as top

def collect_urls():
    mixes = []
    mix_page_urls = extract_urls(requests.get(mixes_page_url).text, 'mixes-')
    for url in mix_page_urls:
        url = site_url + url
        for link in extract_urls(requests.get(url).text, 'Double'):
            mixes.append(link)

        # year = url[-4:]
        # url = site_url + url
        # mixes[year] = extract_urls(requests.get(url).text, 'Double')
    return mixes

def list_urls():
    urls_list = []
    for index, url in enumerate(collect_urls()):
        filename = url.split('/')[-1].replace('%20', " ")
        urls_list.append(filename)
        print("{}.  {}".format(str(index + 1), filename[:-4]))
    return urls_list


# ========== Main ==========

def main():
    filenames = list_urls()
    print("\nUse 'all' to download all mixes.")
    download_choice = input("\nWhich mix would you like to Download?\n> ")
    mixes = collect_urls()
    if download_choice == 'all':
        for mix, filename in zip(mixes, filenames):
            download_mix(mix, filename)
    else:
        download_choice = int(download_choice) - 1
        download_mix(mixes[download_choice], filenames[download_choice])
    print('\n\n[*] Done!')
    # pprint.pprint(collect_urls())


main()


