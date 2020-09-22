
"""
Download all specified links on a given webpage

Usage:
    python main.py --url <url/or/path/to/directory> --tag a --prefix http --suffix .zip

Requires: 
    requests >= 1.0.4
    beautifulsoup >= 4.0.0
"""

__author__= 'Jixin Jia <jixin.jia@outlook.com>'
__license__= 'MIT'
__version__= '1.0.0'

import requests
import os
import sys
import time
import re
from bs4 import BeautifulSoup
import argparse
import urllib.parse


def get_links(base_url, tag, prefix, suffix):
    # use requests.get if URL starts with http
    if base_url.startswith('http'):
        req = requests.get(base_url)
        if req.status_code == 200:
            encoding = req.encoding if req.encoding != 'ISO-8859-1' else None
            soup = BeautifulSoup(req.text, 'lxml', from_encoding=encoding)
    # read as local file
    else:
        soup = BeautifulSoup(open(base_url, encoding='utf-8'), 'lxml')
    
    # find all <tag>
    links = soup.find_all(tag)
    
    # retrieve <tag>'s link values if they satisfy specified prefix and suffix
    attr = 'href' if tag == 'a' else 'src'

    # get link path
    link_paths = [i.get(attr) for i in links]
    
    # separate absolute links and relative links
    absolute_links = [i for i in link_paths if '://' in i and bool(urllib.parse.urlparse(i).netloc)]
    relative_links = list(set(link_paths).difference(absolute_links))

    http_links = []
    
    # process absolute path links
    for i in absolute_links:
        if i.startswith(prefix) and i.endswith(suffix):
            http_links.append(i)
    
    # process relative path links
    protocol = urllib.parse.urlparse(base_url).scheme
    domain = urllib.parse.urlparse(base_url).netloc
        
    for i in relative_links:
        complete_link = urllib.parse.urljoin(protocol+'://'+domain, i)
        if complete_link.startswith(prefix) and complete_link.endswith(suffix):
            http_links.append(complete_link)
    
    return http_links


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, required=True, help='input url or file path')
    parser.add_argument('-t', '--tag', type=str, required=True, help='input tag (e.g. a, img)')
    parser.add_argument('-p', '--prefix', type=str, default='http', help='link prefix (e.g. http)')
    parser.add_argument('-s', '--suffix', type=str, default='', help='link suffix (e.g. .png, .jpg, .pdf, .zip)')
    
    args = parser.parse_args()
    count = 0
    try:
        # parse URL and get downloadable links
        download_links = get_links(args.url, args.tag, args.prefix, args.suffix)
        
        if len(download_links) == 0:
            raise Exception('No links found on the webpage')
        else:
            # list all downloadable links
            for i in download_links:
                print(i)
            
            print(f'\n[INFO] Found {len(download_links)} downloadable links')
            
            # ask whether to download or not
            ans = input('Do you want to download ? (y/n): ').lower()
            
            # termiante program if 'n'
            if ans != 'y':
                sys.exit()

            # proceed to download all downloadable links
            t0 = time.time()
            for i in download_links:
                # get download content name from original link
                origFileName = os.path.basename(i)
                try:
                    # download and save content
                    r = requests.get(i, allow_redirects=True)
                    
                    # get download content name (including redirected ones)
                    fileName = os.path.basename(r.url)

                    # save o disk
                    open(fileName, 'wb').write(r.content)
                    print(f'Downloaded: {fileName}')   
                    count += 1         
                except:
                    print(f'[ERROR] Unable to download: {origFileName}')
            
            t1 = time.time()

            print(f'\n[INFO] Successfully downloaded {count} files ({count/len(download_links)*100:.0f} % success rate) (Elapsed: {(t1-t0)//60:.1f} min)')
            

    except Exception as e:
        print('[ERROR]', e)
        exit(-1)