import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def create_directory(directory):
    os.makedirs(directory, exist_ok=True)

def download_images(url, directory):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'lxml')
    img_tags = soup.find_all('img', src=True)

    create_directory(directory)

    for img in img_tags:
        img_url = urljoin(url, img['src'])
        img_filename = os.path.basename(urlparse(img_url).path)
        img_path = os.path.join(directory, img_filename)

        try:
            with requests.get(img_url, stream=True) as img_response:
                img_response.raise_for_status()
                with open(img_path, 'wb') as img_file:
                    for chunk in img_response.iter_content(chunk_size=8192):
                        img_file.write(chunk)
                print(f"Downloaded: {img_filename}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {img_filename}: {e}")