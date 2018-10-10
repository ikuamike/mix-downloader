# ========== Imports ==========

from bs4 import BeautifulSoup
import pprint
import requests
import sys

# ========== Main variables ==========

site_url = "http://www.deejayjoemfalme.com"
mix_page = "http://www.deejayjoemfalme.com/index.php/mixes"

# ========== Functions ==========


def download_mix(url, filename):
    with open(filename, 'wb') as f:
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')
        dl = 0
        total_length = int(total_length)
        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            f.write(data)
            done = int(50 * dl / total_length)
            sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
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
    mixes = {}
    mix_page_urls = extract_urls(requests.get(mix_page).text, 'mixes-')
    for url in mix_page_urls:
        year = url[-4:]
        url = site_url + url
        mixes[year] = extract_urls(requests.get(url).text, 'Double')
    return mixes

def list_urls():
    for key, value in collect_urls().items():
        for index, url in enumerate(value):
            filename = url.split('/')[-1].replace('%20', " ")
            print("{}.  {}.".format(str(index), filename[:-4]))


# ========== Main ==========

def main():
    list_urls()
    # pprint.pprint(collect_urls())


main()
# print('[*] Downloading ' + filename)


