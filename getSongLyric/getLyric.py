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

    search_url = "https://www.musixmatch.com/search/%s/tracks" % (song.replace(' ', '-'))
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
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

                artists = []
                for artist in artisAr:
                    artists.append(artist.text)

                # title = soup.find(class_='mxm-track-title__track').text[6:]
                titleEl = soup.find(class_='lyrics-to').text if soup.find(class_='lyrics-to').text is not None else ''
                titleEl = titleEl.split('by')[0]

                if "The" in titleEl:
                    title = titleEl[14:]
                else:
                    title = titleEl[10:]

                title = title.strip()

                if lyrics.strip():
                    return lyrics, cover, title, artists
