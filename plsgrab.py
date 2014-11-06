#!/usr/bin/python3 -tt

# Read in a .pls file from the Internet, and print out the URL of the stream for mpd

import sys
import os

import urllib.request, urllib.error, urllib.parse
from re import sub, search, findall


# Get the value of an external DEBUG shell variable to determine if we should print debug info
try:
    DEBUG_MODE = int(os.environ["DEBUG"])
except:
    DEBUG_MODE = 0

URLTIMEOUT = 2

def D(level, string, object):
    """Print debug information if the debug level is set
    """
    
    if DEBUG_MODE >= level:
        sys.stderr.write(string)
        sys.stderr.write(': ')
        sys.stderr.write(str(object))
        sys.stderr.write('\n')
    return


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
    try:
        response = urllib.request.urlopen(url, timeout = URLTIMEOUT)
        html = response.read().decode('utf8')
        stream_url = extract_pls(html)
        return stream_url
    except urllib.error.URLError as e:
        sys.stderr.write(str(e.reason))
        sys.stderr.write('\n')
    return


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
        try:
            response = urllib.request.urlopen(url, timeout = URLTIMEOUT)
            html = response.read().decode('utf8')
            pls_urls = findall(r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.pls)', html)
            D(2, 'get_stream_urls found:', pls_urls)
            for pls_url in pls_urls:
                D(1, 'get_stream_urls looking for', pls_url)
                streamurl = get_one_stream_url(pls_url)
                if streamurl:
                    response_list.append(streamurl)
            return response_list
        except urllib.error.URLError as e:
            sys.stderr.write(str(e.reason))
            sys.stderr.write('\n')
    return
    

def main():
    global VERBOSE_MODE
    global DEBUG_MODE

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
