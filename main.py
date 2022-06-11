import urllib.parse

from bs4 import BeautifulSoup
import requests
import codecs
import re


def _musixmatch(song):
    def extract_mxm_props(soup_page):
        scripts = soup_page.find_all("script")
        for script in scripts:
            if script and script.contents and "__mxmProps" in script.contents[0]:
                return script.contents[0]

    search_url = "https://www.musixmatch.com/search/%s" % (urllib.parse.quote(song))

    header = {"User-Agent": "curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)"}
    search_results = requests.get(search_url, headers=header)

    soup = BeautifulSoup(search_results.text, 'html.parser')
    props = extract_mxm_props(soup)

    if props:
        page = re.findall('"track_share_url":"([^"]*)', props)

        if page:
            url = codecs.decode(page[0], 'unicode-escape')
            lyrics_page = requests.get(url, headers=header)
            soup = BeautifulSoup(lyrics_page.text, 'html.parser')
            props = extract_mxm_props(soup)

            if '"body":"' in props:
                lyrics = props.split('"body":"')[1].split('","language"')[0]
                lyrics = lyrics.replace("\\n", "\n")
                lyrics = lyrics.replace("\\", "")

                coverEl = soup.find(class_='banner-album-image-desktop').find('img')
                cover = 'https:' + coverEl['src'] if coverEl.has_attr('src') is not None else ''

                artisAr = soup.find_all(class_='mxm-track-title__artist-link')

                artises = []
                for artis in artisAr:
                    artises.append(artis.text)

                title = soup.find(class_='mxm-track-title__track').text[6:]

                if lyrics.strip():
                    return lyrics, cover, title, artises


if __name__ == '__main__':
    print(_musixmatch("thu cuoi"))
