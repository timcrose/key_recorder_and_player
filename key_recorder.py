# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 17:04:29 2024

@author: timcr
"""
import pynput as pnp
import time
import pandas as pd
import string

def get_key_name(key, lowercase_only=True):
    '''
    convert a pynput key into a str representing the key.
    
    Parameters
    ----------
    key:
        for function keys: enum 'Key'
        for letter keys: pynput.keyboard._win32.KeyCode
        
    lowercase_only: bool
        True: only worry about lowercase letters
        False: attempt to keep track of uppercase letters too as different from
            lowercase letters.
            
    Returns
    -------
    name: str
        String code for the key as recognized by pynput.
    '''
    name = str(key).replace('Key.','')
    if lowercase_only:
        name = name.lower()
    return name


def on_press(key):
    '''
    Record when the key is pressed unless the termination key is pressed, in which case,
    write all recorded data to a file and exit the program.
    
    Parameters
    ----------
    key:
        for function keys: enum 'Key'
        for letter keys: pynput.keyboard._win32.KeyCode
        
    Returns
    -------
    continue_operation: None or bool
        If None, continue. If False, abort the program.
        
    Notes
    -----
    1. The timestamp will become relative to the timestamp of the first key press
        in the recording.
    '''
    global key_log, key_is_pressed
    name = get_key_name(key, lowercase_only=True)
    if name == 'esc':
        df = pd.DataFrame(key_log)
        first_recorded_timestamp = key_log[0]['key_down_timestamp']
        df['key_down_timestamp'] = df['key_down_timestamp'] - first_recorded_timestamp
        df['key_up_timestamp'] = df['key_up_timestamp'] - first_recorded_timestamp
        df['key'] = df['key'].str.lower()
        df.to_csv('recorded_keystrokes.csv', index=False)
        return False
    # Holding down a key causes that key to register as many on_press events, but
    # we only want to record the first one.
    if not key_is_pressed[name]:
        key_log.append({'key': name, 'key_down_timestamp': time.perf_counter()})
        key_is_pressed[name] = True
        

def on_release(key):
    '''
    Record when the key is released unless it had not yet been pressed (which usually
    signals an issue).
    
    Parameters
    ----------
    key:
        for function keys: enum 'Key'
        for letter keys: pynput.keyboard._win32.KeyCode
        
    Returns
    -------
    None
    '''
    global key_log, key_is_pressed
    name = get_key_name(key, lowercase_only=True)
    if not key_is_pressed[name]:
        if not key_is_pressed[name.lower()]:
            #error
            print('key:', name, 'got up before down', 'len(key_log)', len(key_log))
            return
        else:
            name = name.lower()
    key_is_pressed[name] = False
    for i in list(range(len(key_log)))[::-1]:
        if key_log[i]['key'] == name and 'key_up_timestamp' not in key_log[i]:
            key_log[i]['key_up_timestamp'] = time.perf_counter()
            break
    

def record_keys(start_delay=0):
    '''
    Record all keystrokes by recording each key's press and release times. Store
    that data to a file.

    Parameters
    ----------
    start_delay: number
        The amount of time to sleep before starting the recording.

    Returns
    -------
    None
    '''
    global key_log, key_is_pressed
    key_log = []
    key_is_pressed = dict()
    for name in string.ascii_letters + string.digits + string.punctuation:
        key_is_pressed[name] = False
    for key in pnp.keyboard.Key:
        key_is_pressed[get_key_name(key, lowercase_only=True)] = False
    # This sleep is in case the user pressses a button such as enter or F5 to start the program.
    time.sleep(start_delay)
    # Start listening for key presses. Esc ends the listening and records data.
    with pnp.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
        
        
def main():
    record_keys(start_delay=0.15)
    

if __name__ == '__main__':
    main()
