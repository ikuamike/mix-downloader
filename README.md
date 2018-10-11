# Mix Downloader

Simple script to automate downloading mixes from [Deejay Joe Mfalme's website.](http://www.deejayjoemfalme.com/)

## How it works!

- It scrapes the website for links using [BeautifulSoup](#).
- Filters them to make sure they are mix only links and makes a list of them.
- Then downloads the mixes using [Requests](#) and saves them in ``` The Double Trouble Mixxtapes``` folder in the ```Music``` directory.

## Features

- Download Progress bar
- Interactive interface to pick mix of choice to download or download all of them at once.
