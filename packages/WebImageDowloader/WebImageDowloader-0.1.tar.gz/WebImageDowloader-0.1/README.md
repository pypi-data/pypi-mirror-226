# WebImageDowloader

WebImageDowloader is a Python library that allows you to easily download all images from a given URL. It can be used to quickly fetch and save images from web pages for various purposes.

## Installation

You can install WebImageDowloader using pip:
```bash
pip install WebImageDowloader
```
## Usage

WebImageDowloader provides a simple method called download_images that allows you to download images from a URL and specify the output directory. To use it, follow the example below:

```bash

from WebImageDowloader import download_images

url = "https://example.com/images"
download_directory = "./downloaded_images"

download_images(url, download_directory)
```

Replace url with the URL of the web page containing the images you want to download, and download_directory with the directory where you want to save the downloaded images.

## Features

    Fetch and download all images from a given URL.
    Specify the output directory to save the images.
