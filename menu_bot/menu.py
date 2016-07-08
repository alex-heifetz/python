#! /usr/bin/python
# -*- coding: utf-8 -*-

import re
import datetime
import sys



# if 1 == len(sys.argv):
#     exit()
# elif '250' == sys.argv[1]:
#     response = urllib2.urlopen('http://www.brandmeister.spb.ru/menu/biznes-lanch#content')
# elif '300' == sys.argv[1]:
#     response = urllib2.urlopen('http://www.brandmeister.spb.ru/menu/premium-lanchi-300-rub#content')
# else:
#     exit()

def pls_parse_this_shit(response):
    html = response.read()
    html = html[html.find(r'<table style="width: 100%;" border="0">'):html.find(r'</table>')]
    html = re.sub('style="text-align: .*?;"', '', html)
    html = re.sub('\s+colspan="2"', '', html)
    html = re.sub('&nbsp;', '', html)
    html = re.sub('</?(span|thead|tbody|br)>', '', html)
    html = re.sub(' >', '>', html)
    html = re.sub('<hr />', '', html)
    html = re.sub('\n+', "\n", html)
    html = re.sub('\s{3,}', '', html)
    html = re.sub('(</strong>)+', '</strong>', html)
    html = re.sub('(<strong>)+', '<strong>', html)
    html = re.sub('</strong><strong>', '', html)
    html = re.sub('<strong></strong>', '', html)
    html = re.sub('<(\w+) .*?>', '<\g<1>>', html)
    html = re.sub('<br>', '', html)
    html = re.sub('<tr>\n<td>(<strong></strong>)?</td>\n</tr>', '', html)

    months = ['ЯНВАРЯ', 'ФЕВРАЛЯ', 'МАРТА', 'АПРЕЛЯ', 'МАЯ', 'ИЮНЯ', 'ИЮЛЯ', 'АВГУСТА', 'СЕНТЯБРЯ', 'ОКТЯБРЯ', 'НОЯБРЯ',
              'ДЕКАБРЯ']
    day = str(datetime.date.today().day)
    month = months[int(datetime.date.today().month) - 1]
    reg = r'<tr>\n((?:.|\n)*?)\n</tr>'
    pos = []
    items = []
    head = False

    for item in re.compile(reg).findall(html):
        if not ':' in item and '<strong>' in item:
            pos.append(html.find(item))
            items.append(item)
            if month in item:
                if str(day) in item:
                    head = item
                    continue
                elif not head and str(int(day) + 1) in item:
                    head = item
                    continue

    if head:
        if pos[-1] > html.find(head):
            end = items[pos.index(html.find(head)) + 1]
            html = html[html.find(head) + len(head):html.find(end)]
        else:
            html = html[html.find(head) + len(head):]
    #
    html = re.sub(r'</?t[rd]>', '', html)
    html = re.sub('&laquo;', '«', html)
    html = re.sub('&raquo;', '»', html)
    html = re.sub('(\d)([мг])', '\g<1> \g<2>', html)
    html = re.sub('\n\s?(\d)', ' - \g<1>', html)
    html = re.sub('\n{2,}', '\n\n', html)

    text = "<strong>" + day + ' ' + month + "</strong>\n"
    text += html[1:]
    return text
