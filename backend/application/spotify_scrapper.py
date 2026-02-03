from typing import List, Union
from playwright.sync_api import sync_playwright
import time

class SpotifyScraper:
    def __init__(self, headless: bool = True, wait_seconds: float = 1.0):

        self.headless = headless
        self.wait_seconds = wait_seconds

    def get_playlist_track_names(self, playlist_url: str, count: Union[int, str] = "all") -> List[str]:

        if not (isinstance(count, int) or (isinstance(count, str) and count == "all")):
            raise ValueError("count deve ser int ou 'all'")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            page.goto(playlist_url, timeout=30000)

            # Espera os links de músicas aparecerem
            try:
                page.wait_for_selector('a[href*="/track/"]', timeout=15000)
            except:
                time.sleep(self.wait_seconds)

            tracks = []
            seen = set()
            previous_count = 0
            max_scrolls = 50  # Limite de scrolls para evitar loop infinito

            for scroll_attempt in range(max_scrolls):
                # Coleta todos os links de tracks atuais
                anchors = page.query_selector_all('a[href*="/track/"]')
                
                for a in anchors:
                    href = a.get_attribute('href')
                    if not href or '/track/' not in href or href in seen:
                        continue

                    name = a.inner_text().strip()
                    if not name:
                        continue
                    if '\n' in name:
                        name = name.splitlines()[0].strip()

                    tracks.append(name)
                    seen.add(href)

                    if isinstance(count, int) and len(tracks) >= count:
                        break

                if isinstance(count, int) and len(tracks) >= count:
                    break

                if len(tracks) == previous_count:
                    break

                previous_count = len(tracks)
                
                self.scroll_to_down(page)

            browser.close()

        return tracks if count == "all" else tracks[:count]

    def scroll_to_down(self, page):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(self.wait_seconds)


