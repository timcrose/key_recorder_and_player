# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 17:39:09 2024

@author: timcr
"""

import pandas as pd
import time
import sys, os
sys.path.append(os.path.join(r'C:\Users\timcr\Documents\python_packages\swg_code'))
import pydirectinput_tmr as pdi
pdi.FAILSAFE = False

def press_sequentially():
    pass

def press(keys, presses=1, start_delay=0.0, return_delay=0.0, key_down_delay=0):
    '''
    Parameters
    ----------
    keys: list of str or list of list of str or str
        List of keys.
        e.g.
        ['shift', 'a']
        list of list of keys: equivalent to press_sequentially
        e.g.
        [['shift', 'a'], ['ctrl', 'c']]
        str
        e.g.
        'esc' presses escape, '1', presses 1

    Returns
    -------
    None

    Purpose
    -------
    This function enables you to press any number of keys in combination. i.e. you can hold down alt, ctrl, shift and then press a key using this function.
    '''
    time.sleep(start_delay)
    for _ in range(presses):
        if keys is None or len(keys) == 0:
            break
        elif type(keys) is str:
            if key_down_delay > 0:
                pdi.keyDown_fast(keys)
                time.sleep(key_down_delay)
                pdi.keyUp_fast(keys)
            else:
                pdi.press_key_fast(keys)
        elif type(keys[0]) is list:
            press_sequentially(keys, key_down_delay=key_down_delay)
        elif type(keys[0]) is str or type(keys[0]) is int:
            if type(keys[0]) is int:
                keys = list(map(str,keys))
            for key in keys:
                pdi.keyDown_fast(key)
            time.sleep(key_down_delay)
            for key in keys[::-1]:
                pdi.keyUp_fast(key)
    time.sleep(return_delay)
    
    
def create_event_dataframe(df):
  """
  Creates a new DataFrame with columns 'key', 'action', and 'timestamp' by combining key_down and key_up events.

  Args:
    df: The original DataFrame with columns 'key', 'key_down_timestamp', and 'key_up_timestamp'.

  Returns:
    A new DataFrame with columns 'key', 'action', and 'timestamp'.
  """

  # Create two DataFrames, one for key_down and one for key_up events
  df_down = df[['key', 'key_down_timestamp']].rename(columns={'key_down_timestamp': 'timestamp'})
  df_down['action'] = 'down'

  df_up = df[['key', 'key_up_timestamp']].rename(columns={'key_up_timestamp': 'timestamp'})
  df_up['action'] = 'up'

  # Combine the DataFrames and sort by timestamp
  df_events = pd.concat([df_down, df_up], ignore_index=True)
  df_events = df_events.sort_values(by='timestamp')
  df_events['time_delta'] = df_events['timestamp'].diff().shift(-1).fillna(0.0)
  df_events = df_events.drop(columns=['timestamp'])
  return df_events


def play_recorded_keystrokes(recorded_keystrokes_fpath):
    df = pd.read_csv(recorded_keystrokes_fpath)
    #print(df.head())
    df_events = create_event_dataframe(df)
    print(df_events)
    for _, row in df_events.iterrows():
        key = row['key']
        action = row['action']
        delay = row['time_delta']
        if action == 'down':
            pdi.keyDown_fast(key)
        else:
            pdi.keyUp_fast(key)
        time.sleep(delay)

if __name__ == '__main__':   
    time.sleep(3)
    #play_recorded_keystrokes('stone_to_gate.csv')
    #play_recorded_keystrokes('gate_to_outside_cave.csv')
    #play_recorded_keystrokes('cave_to_top_of_hill.csv')
    #play_recorded_keystrokes('to_outside_httk.csv')
    #play_recorded_keystrokes('recorded_keystrokes_altered.csv')
    #play_recorded_keystrokes('1_end_to_cave.csv')
    play_recorded_keystrokes('recorded_keystrokes.csv')