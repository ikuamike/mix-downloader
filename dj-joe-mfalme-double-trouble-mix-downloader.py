##############################
# Author: Michael Ikua
# Github: ikuamike
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
    default_download_location = os.getenv('HOME') + '/Music'
    print('\n[*] Downloading ' + filename + ' to ' + default_download_location + '\n')
    filename = default_download_location + '/' + filename

    with open(filename, 'wb') as f:
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')
        dl = 0
        total_length = int(total_length)
        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            f.write(data)
            done = int(50 * dl / total_length)
            sys.stdout.write('\t\r[{}{}]'.format('█' * done, '.' * (50-done)))
            sys.stdout.flush()
    print('\n\n[*] Done!')


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
    download_choice = int(input("\nWhich mix would you like to Download?\n> ")) - 1
    mixes = collect_urls()
    download_mix(mixes[download_choice], filenames[download_choice])
    # pprint.pprint(collect_urls())


main()


