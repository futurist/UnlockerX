#!/usr/local/bin/python3
import os
import sys
import time
import json
import http.client
from urllib.parse import urlparse

from_json = lambda x: json.loads(x)
time_now = lambda: time.strftime('%Y_%m_%d_%H_%M_%S')
feishuBotUrl = ''

def notifyUrl(url: str, data: dict):
    parts = urlparse(url)
    conn = http.client.HTTPSConnection(parts.netloc)
    conn.request('POST', parts.path, json.dumps(data), {'Content-type': 'application/json'})
    response = conn.getresponse()
    print(response.status, response.reason)

def event_weak_signal(status: bool, status_prev: bool = None, **env):
    # TODO: something you want to do.
    print(time_now(), 'from "%s" to "%s"' % (status_prev, status))


def event_connect_status_changed(status: bool, status_prev: bool = None, **env):
    # TODO: something you want to do.
    print(time_now(), 'from "%s" to "%s"' % (status_prev, status))


def event_lock_status_changed(status: bool, status_prev: bool = None, **env):
    # TODO: something you want to do.
    print(time_now(), 'from "%s" to "%s"' % (status_prev, status))
    if feishuBotUrl:
        data = {'msg_type': 'text', 'content': {'text': 'computer locked:%s' % (status)}}
        notifyUrl(feishuBotUrl, data)
        # os.system("curl -sSf -X POST %s -H 'Content-Type: application/json' -d '%s'" % (feishuBotUrl, json.dumps(data)))


if __name__ == '__main__':
    env = os.environ
    params = from_json(env.pop('UNLOCKERX_ENV'))
    event = params['event']

    if len(sys.argv) >= 2:
        feishuBotUrl = sys.argv[1]

    events = {
        'weak_signal': event_weak_signal,
        'connect_status_changed': event_connect_status_changed,
        'lock_status_changed': event_lock_status_changed,
    }

    if event in events:
        events[event](**params, **env)
    else:
        print("Can't execute valid function: %s" % event)
