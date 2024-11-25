# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 17:04:29 2024

@author: timcr
"""
import pynput as pnp
import time
import sys
import pandas as pd

def on_press(key):
    '''
    key:
        for function keys: enum 'Key'
        for letter keys: pynput.keyboard._win32.KeyCode
    '''
    global key_log, keys_to_wait_for_release
    if hasattr(key, 'name'):
        name = key.name
    else:
        name = key.char
    if name == 'esc':
        df = pd.DataFrame(key_log)
        first_recorded_timestamp = key_log[0]['key_down_timestamp']
        df['key_down_timestamp'] = df['key_down_timestamp'] - first_recorded_timestamp
        df['key_up_timestamp'] = df['key_up_timestamp'] - first_recorded_timestamp
        df['key'] = df['key'].str.lower()
        df.to_csv('recorded_keystrokes.csv', index=False)
        sys.exit()
    if name not in keys_to_wait_for_release:
        keys_to_wait_for_release.add(name)
        key_log.append({'key': name, 'key_down_timestamp': time.perf_counter()})

def on_release(key):
    '''
    key:
        for function keys: enum 'Key'
        for letter keys: pynput.keyboard._win32.KeyCode
    '''
    global key_log, keys_to_wait_for_release
    if hasattr(key, 'name'):
        name = key.name
    else:
        name = key.char
    if name not in keys_to_wait_for_release:
        #error
        print('key:', name, 'got up before down', 'len(key_log)', len(key_log))
        return
    keys_to_wait_for_release.remove(name)
    for i in list(range(len(key_log)))[::-1]:
        if key_log[i]['key'] == name and 'key_up_timestamp' not in key_log[i]:
            key_log[i]['key_up_timestamp'] = time.perf_counter()
            break
    

# listen for a hotkey
key_log = []
keys_to_wait_for_release = set()
with pnp.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()