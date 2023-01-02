# !/usr/bin/env python3
import os
import re
import glob
import json
import requests
from os import environ as env
from dotenv import load_dotenv


def card_link(url):
    """Custom html card link"""

    with open('custom/card_link.html', 'r') as reader:
        content = reader.read()

    return content.replace("url", url)


def list_files(root_dir, ext):
    """list files by extension"""

    path = f'{root_dir}/**/*.{ext}'
    files = glob.glob(path, recursive=True)
    return files


def convert_shortcodes(string):
    """convert backslash quotes to regular quotes"""

    pattern = r'{{\s*richlink\s*(.+)\s*}}'

    if re.search(pattern, string):
        for match in re.finditer(pattern, string):
            link, shortcode = match.group(1), match.group(0)
            string = string.replace(shortcode, richlink(link))
        return string
    else:
        print("nada")
        return string


def richlink(url):
    """return richlink html from iframely.com"""

    url_api = f"https://iframe.ly/api/oembed?url={url}&api_key={api_key}&card=small"
    response = requests.get(url_api)
    if response.status_code == 200:
        try:
            data = response.json()
            return (data['html'])
        except:
            print("200 Error al obtener el HTML de la página")
            print(url)
            return card_link(url)
    else:
        print("Error al obtener el HTML de la página")
        print(url)
        return card_link(url)


def render(root_dir, ext):
    """Render files by extension"""

    files = list_files(root_dir, ext)

    for file in files:
        print(file)
        with open(file, 'r') as reader:
            content = reader.read()

        content = convert_shortcodes(content)

        with open(file, 'w') as writer:
            writer.write(content)


if __name__ == "__main__":

    load_dotenv()
    api_key = env['IFRAMELY_API_KEY']
    render(root_dir="_site", ext="html")
