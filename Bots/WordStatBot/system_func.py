import re
import subprocess

from config import admin_id

def is_admin(message):
    return admin_id == message.from_user.id


def get_ip():
    res = str(
        subprocess.Popen("echo $(ifconfig | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}')",
                         shell=True, stdout=subprocess.PIPE).communicate())
    res = re.sub('[^0-9.]', '', res)
    return res


def list_to_str(title, _list, index=[], reverse=False):
    _len = len(index)
    if _len > 0:
        if _list:
            title = '<strong>' + str(title) + ':</strong>'
            _str = ''
            for item in _list:
                if reverse:
                    if 1 == _len:
                        _str = str(item[index[0]]) + _str + '\n'
                    else:
                        _str = str(item[index[0]]) + ' - ' + str(item[index[1]]) + _str + '\n'
                else:
                    if 1 == _len:
                        _str += str(item[index[0]]) + '\n'
                    else:
                        _str += str(item[index[0]]) + ' - ' + str(item[index[1]]) + '\n'
            return str(title + '\n' + _str)
