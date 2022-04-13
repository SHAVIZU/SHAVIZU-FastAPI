from selenium import webdriver

import boto3

import time

import ssl
from urllib.request import urlopen
from io import BytesIO

from src import Settings


async def crawl_image_by_style_code(style_code: str, settings: Settings):
        chrome_driver = settings.CHROME_DRIVER_PATH
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        driver = webdriver.Chrome(chrome_driver, options=options)
        driver.get(f"https://www.google.com/search?q={style_code}&tbm=isch")
        data_id = driver.find_element_by_xpath(
            "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]"
        ).get_attribute('data-id')
        driver.get(f"https://www.google.com/search?q={style_code}&tbm=isch#imgrc={data_id}")

        time.sleep(1)

        img_url = driver.find_element_by_xpath(
            "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img"
        ).get_attribute("src")
        context = ssl._create_unverified_context()
        res = urlopen(img_url, context=context).read()
        img = BytesIO(res)

        s3_client = boto3.client(
                service_name="s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY,
                aws_secret_access_key=settings.AWS_SECRET_KEY
        )
        s3_client.upload_fileobj(img, "shavizu", f"item/{style_code}.png", ExtraArgs={"ACL": "public-read", "ContentType": "png"})

        return f"https://shavizu.s3.ap-northeast-2.amazonaws.com/item/{style_code}.png"
