import os
import time
import urllib.request
from multiprocessing.pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor, wait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image
from chromedriver_py import binary_path
import urllib.request
import logging
import requests
from fake_useragent import UserAgent
from selenium.common.exceptions import TimeoutException
import base64
from io import BytesIO
from tqdm import tqdm
from urllib.request import HTTPError
from selenium.webdriver.common.action_chains import ActionChains

DEFAULT_DESTINATION = "downloads"
DEFAULT_LIMIT = 50
DEFAULT_RESIZE = None
DEFAULT_QUIET = False
DEFAULT_DEBUG = False

IMAGE_HEIGHT = 180

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

user_agent = UserAgent().chrome
headers = {'User-Agent': str(user_agent)}


class GoogleImagesDownloader:
    def __init__(self):
        self.quiet = DEFAULT_QUIET

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(options=options, service=webdriver.ChromeService(executable_path=binary_path))

        self.__consent()

    def init_arguments(self, arguments):
        if arguments.debug:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.DEBUG)
            stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

            logger.addHandler(stream_handler)

        if arguments.quiet:
            self.quiet = True

    def download(self, query, destination=DEFAULT_DESTINATION, limit=DEFAULT_LIMIT,
                 resize=DEFAULT_RESIZE):
        query_destination_folder = os.path.join(destination, query)
        os.makedirs(query_destination_folder, exist_ok=True)

        self.driver.get(f"https://www.google.com/search?q={query}&tbm=isch")

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='list']"))
        )

        self.__disable_safeui()

        list_items = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='list']"))
        )

        self.__scroll(limit)

        image_items = list_items.find_elements(By.CSS_SELECTOR, "div[role='listitem']")

        if not self.quiet:
            print("Downloads...")

        downloads_count = len(image_items) if limit > len(image_items) else limit

        if self.quiet:
            self.__download_items(query, destination, image_items, resize, limit)
        else:
            with tqdm(total=downloads_count) as pbar:
                self.__download_items(query, destination, image_items, resize, limit, pbar=pbar)

    def __download_items(self, query, destination, image_items, resize, limit, pbar=None):
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_list = list()

            for index, image_item in enumerate(image_items):
                logger.debug(f"index : {index}")

                image_url, preview_src = self.__get_image_values(image_item)

                complete_file_name = os.path.join(destination, query,
                                                  query.replace(" ", "_") + "_" + str(index) + ".jpg")

                future_list.append(
                    executor.submit(download_image, complete_file_name, image_url, preview_src,
                                    resize, pbar=pbar))

                if index + 1 == limit:
                    break

            wait(future_list)

    def __get_image_values(self, image_item):
        actions = ActionChains(self.driver)
        actions.move_to_element(image_item).perform()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(image_item)).click()

        preview_src = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[jsname='CGzTgf'] div[jsname='figiqf'] img"))
        ).get_attribute("src")

        image_url = None

        try:
            image_url = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img[jsname='kn3ccd']"))
            ).get_attribute("src")
        except TimeoutException:  # No image available
            pass

        logger.debug(f"image_url : {image_url}")

        return image_url, preview_src

    def __disable_safeui(self):
        href = self.driver.find_element(By.CSS_SELECTOR, 'div.cj2HCb div[jsname="ibnC6b"] a').get_attribute("href")

        href = href.replace("safeui=on", "safeui=off")

        self.driver.get(href)

    def __consent(self):
        self.driver.get("https://www.google.com/")

        self.driver.add_cookie(
            {'domain': '.google.com', 'expiry': 1726576871, 'httpOnly': False, 'name': 'SOCS', 'path': '/',
             'sameSite': 'Lax', 'secure': False, 'value': 'CAESHAgBEhJnd3NfMjAyMzA4MTUtMF9SQzQaAmZyIAEaBgiAjICnBg'})

        self.driver.add_cookie(
            {'domain': 'www.google.com', 'expiry': 1695040872, 'httpOnly': False, 'name': 'OTZ', 'path': '/',
             'sameSite': 'Lax', 'secure': True, 'value': '7169081_48_52_123900_48_436380'})

    def __scroll(self, limit):
        if not self.quiet:
            print("Scrolling...")

        count = 0

        display_more = self.driver.find_element(By.CSS_SELECTOR, 'input[jsaction="Pmjnye"]')
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        scroll_try = 0

        loaded_images = 0

        while True:
            count += IMAGE_HEIGHT * 3
            self.driver.execute_script(f"window.scrollTo(0, {count});")
            loaded_images += 6

            time.sleep(1)

            if loaded_images >= limit:
                return

            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if display_more.is_displayed() and display_more.is_enabled():
                display_more.click()

            if last_height == new_height:
                scroll_try += 1
            else:
                scroll_try = 0

            if last_height == new_height and scroll_try > 10:
                break

            last_height = new_height


def download_image(complete_file_name, image_url, preview_src, resize, pbar=None):
    image_bytes = None

    download_success = False

    if image_url:
        download_image_aux(complete_file_name, image_url)  ## Try to download image_url

    if not download_success:  # Download failed, download the preview image
        if preview_src.startswith("http"):
            logger.debug("preview_src startswith http")
            download_image_aux(complete_file_name, preview_src)  ## Download preview image
        else:
            logger.debug("preview_src data")
            image_bytes = base64.b64decode(
                preview_src.replace("data:image/png;base64,", "").replace("data:image/jpeg;base64,", ""))

    image = Image.open(complete_file_name) if image_bytes is None else Image.open(BytesIO(image_bytes))

    if image.mode != 'RGB':
        image = image.convert('RGB')

    if resize is not None:
        image = image.resize(resize)

    image.save(complete_file_name, "jpeg")

    if pbar:
        pbar.update(1)


def download_image_aux(complete_file_name, image_url):
    download_success = True

    with open(complete_file_name, 'wb') as handler:
        try:
            request = requests.get(image_url, headers=headers)

            if request.status_code == 200:
                handler.write(request.content)
            else:
                download_success = False

            logger.debug(f"requests get")
        except requests.exceptions.SSLError:
            try:
                request = urllib.request.Request(image_url, headers=headers)
                handler.write(urllib.request.urlopen(request).read())
                logger.debug(f"urllib retrieve")
            except HTTPError:
                logger.debug(f"download failed")
                download_success = False

    return download_success
