from selenium.webdriver.common.by import By

from urllib.parse import urlparse

from .exceptions import UnsupportedSourceError
from .exceptions import UnsupportedStructureError


class ScraperTemplate:
    def _fix_scheme(self, url: str) -> str:
        if urlparse(url).scheme == "":
            url = "https:" + url

        return url


class StreamtapeScraper(ScraperTemplate):
    def __init__(self, driver) -> None:
        self.driver = driver

    def get(self):
        video = self.driver.find_element(By.CSS_SELECTOR, "video#mainvideo")

        if not (url := video.get_attribute("src")):
            raise UnsupportedStructureError

        return self._fix_scheme(url)


class MixdropScraper(ScraperTemplate):
    def __init__(self, driver) -> None:
        self.driver = driver

    def get(self) -> str:
        url = self.driver.execute_script("return MDCore.wurl")

        if not url:
            raise UnsupportedStructureError

        return self._fix_scheme(url)

class FilemoonScraper(ScraperTemplate):
    def __init__(self, driver) -> None:
        self.driver = driver

    def get(self) -> str:
        url = self.driver.execute_script("return videop.hls.url")

        if not url:
            raise UnsupportedStructureError

        return self._fix_scheme(url)


class Scraper:
    SOURCES = {
        "tap": StreamtapeScraper,
        "mix": MixdropScraper,
        "mon": FilemoonScraper,
    }

    def __init__(self, driver) -> None:
        self.driver = driver

    def get(self, iframe, source):
        self.driver.switch_to.frame(iframe)
        
        scraper = self.SOURCES.get(source)
        if scraper is None: raise UnsupportedSourceError from None

        return scraper(self.driver).get()
    
    def attach(self, domain, scraper):
        if not hasattr(scraper, "get"):
            raise ValueError("scraper must have get method")

        self.SOURCES[domain] = scraper
    
    def detach(self, domain):
        if domain in self.SOURCES:
            del self.SOURCES[domain]
