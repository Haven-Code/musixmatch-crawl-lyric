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

    search_url = "https://www.musixmatch.com/search/%s" % (song.replace(' ', '-'))
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
                album = soup.find(class_="mxm-track-footer__album")

                if lyrics.strip():
                    return lyrics


if __name__ == '__main__':
    l = _musixmatch('egswthrth')
    print(l)
