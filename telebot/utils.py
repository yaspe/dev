import re
import urllib2


def page_title(url):
    doc = urllib2.urlopen(url).read().lower().replace('\n', '')
    pattern = r'.+<title>(.+)</title>.+'
    title = re.search(pattern, doc).group(1).decode('utf-8')
    if len(title) > 64:
        title = title[:64] + '...'
    return title


def is_admin(uid):
    return uid in (1, 2, 3)
