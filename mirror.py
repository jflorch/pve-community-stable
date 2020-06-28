#!/usr/bin/python3

import urllib.request as req
from datetime import datetime as dt
import re
import os

sources = [
    '/pve/dists/buster/pve-no-subscription/binary-amd64/',
    '/pve/dists/buster/pve-no-subscription'
]
download_dir = 'C:\\Users\\jordan.florchinger\\Desktop\\repo\\'
minimum_age = 60
data_page_url = 'http://download.proxmox.com/debian/'
file_reg = '<a href="(.+)">.+([0-9]{2}-[a-zA-Z]{3}-[0-9]{4}) [0-9]{2}:[0-9]{2}\s+([0-9]+)'
dir_reg = '<a href="(.+)">.+([0-9]{2}-[a-zA-Z]{3}-[0-9]{4}) [0-9]{2}:[0-9]{2}\s+-'
file_pat = re.compile(file_reg)
dir_pat = re.compile(dir_reg)

# Setup Directory
os.makedirs(download_dir, exist_ok=True)


def process_link(current_link):
    tmp_link = data_page_url + current_link
    print(tmp_link)
    link_data = req.urlopen(tmp_link)
    for line in link_data:
        line = line.decode("utf-8")
        file_match = file_pat.match(line)
        dir_match = dir_pat.match(line)
        if file_match is not None:
            name = file_match.group(1)
            if 'index.' in name:
                continue
            dl_link = tmp_link + name
            dir_path = download_dir + current_link
            file_path = download_dir + current_link + name
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                remote_file_size = file_match.group(3)
                if file_size == int(remote_file_size):
                    print('Skipping', file_path)
                    continue
            print('Downloading', file_path)
            os.makedirs(dir_path, exist_ok=True)
            req.urlretrieve(dl_link, file_path)
        elif dir_match is not None:
            name = dir_match.group(1)
            if '../' in name or not name.endswith('/'):
                continue
            print('Exploring', tmp_link + name)
            process_link(current_link + name)

process_link('')

#data = data_resp.read().decode('utf-8')

#lines = data.split('\n')
#for line in lines:
#    groups = re.findall(regex_pattern, line)
#    if len(groups) <= 0:
#        continue
#    groups = groups[0]

#    name = groups[0]
#    type = groups[1]
#    date = dt.strptime(groups[2], '%d-%b-%Y')
#    age_in_days = (dt.now() - date).days

#    if age_in_days < minimum_age:
#        continue;