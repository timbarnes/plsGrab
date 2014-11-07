#!/usr/bin/python3 -tt

# Read in a .pls file from the Internet,
# and print out the URL of the stream for mpd

import sys
import os

import urllib.request, urllib.error, urllib.parse
from re import sub, search, findall


# Get the value of an external DEBUG shell variable to see if we should print debug info
try:
    DEBUG_MODE = int(os.environ["DEBUG"])
except:
    DEBUG_MODE = 0

URLTIMEOUT = 2

def D(level, string, object):
    """Print debug information if the debug level is set
    """
    if DEBUG_MODE >= level:
        print(string, ':', str(object))
    return
              

def open_web_file(url):
    """Given a URL, attempt to open and download the content of the page.
    """
    try:
        response = urllib.request.urlopen(url, timeout = URLTIMEOUT)
        html = response.read().decode('utf8')
        return html
    except urllib.error.URLError as e:
        sys.stderr.write(str(e.reason))
        sys.stderr.write('\n')
        return ""

def extract_pls(html):
    """Scan the provided .pls html for the first stream.
    """
    D(2, 'plsStream HTML', html)
    # This regex finds a URL in the source of the page
    stream = search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', html)
    D(1, 'get_one_stream_url found', stream.group())
    if stream:
        stream = sub(r'(&|\?).*', '', stream.group())
        D(1, 'returning', stream)
        return stream
    else:
        D(1, 'get_one_stream_url', 'not found')
    return ""


def get_one_stream_url(url):
    """Extracts the first stream URL from the given .pls file
    """
    D(1, 'get_one_stream_url looking for', url)
    html = open_web_file(url)
    stream_url = extract_pls(html)
    return stream_url


def get_multiple_pls(html):
    """Given html text, return a list of the embedded stream .pls urls.
    """
    response_list = []
    pls_urls = findall(r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.pls)', html)
    D(2, 'get_stream_urls found:', pls_urls)
    return pls_urls


def get_stream_urls(url):
    """If given a .pls URL, use regex to extract the URL up to the ? or end, whichever happens first.
    If a non-pls file, search the file for .pls entries, and process each.
    """
    response_list = []
    if url[-4:] == '.pls':
        D(1, 'Single Pls', url)
        response_list.append(get_one_stream_url(url))
        D(1, 'get_stream_urls found', response_list)
        return response_list
    else:
        D(1, 'get_stream_urls looking for multiple in', url)
        html = open_web_file(url)
        if html:
            response_list = get_multiple_pls(html)
            return [get_one_stream_url(f) for f in response_list]
    

def main():

    args = sys.argv[1:]

    if not args:
        print('usage: URL')
        sys.exit(1)

    for arg in args:
        D(1, 'main', args)
        urls = get_stream_urls(arg)
        D(1, 'main result', urls)
        for url in urls:
            print(url)


if __name__ == '__main__':
    main()
