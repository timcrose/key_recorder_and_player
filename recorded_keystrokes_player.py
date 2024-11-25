# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 17:39:09 2024

@author: timcr
"""

import pandas as pd
import time
import pydirectinput_tmr as pdi
pdi.FAILSAFE = False


def press(key, start_delay=0, return_delay=0, key_down_delay=0):
    '''
    press a key for a specified length of time.
    
    Parameters
    ----------
    key: str
        pynput string representation of a key.
        
    start_delay: number
        How long in seconds to delay starting the presses.
        
    return_delay: number
        How long in seconds to delay returning after the presses.
        
    key_down_delay: number
        How long in seconds to hold down each press.

    Returns
    -------
    None
    
    Notes
    -----
    1. start_delay and return_delay should normally be 0 as having them be > 0 
        will mess with the timings in a record. But, in case they are needed, 
        they are available.
    '''
    time.sleep(start_delay)
    pdi.keyDown_fast(key)
    time.sleep(key_down_delay)
    pdi.keyUp_fast(key)
    time.sleep(return_delay)
    
    
def create_event_dataframe(df):
    '''
    Creates a new DataFrame with columns 'key', 'action', and 'timestamp' by combining key_down and key_up events.
    
    Parameters
    ----------
    df: pandas.DataFrame
        The original DataFrame with columns 'key', 'key_down_timestamp', and 'key_up_timestamp'.
    
    Returns
    -------
    df_events: pandas.DataFrame
        A new DataFrame with columns 'key', 'action', and 'timestamp'.
    '''
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


def play_recorded_keystrokes(recorded_keystrokes_fpath, verbosity=0, start_delay=0, return_delay=0):
    '''
    Read a .csv dataframe file that stores each key's key, key_down_timestamp, and key_up_timestamp columns
    and transform it into a form such that then this function will use to replay the events as sequential
    keystrokes according to the timing as they were pressed during the recording.

    Parameters
    ----------
    recorded_keystrokes_fpath: str or path
        File path to .csv file that contains columns 'key', 'key_down_timestamp', and 'key_up_timestamp'.
        This is the recorded keystrokes you want to replay.
        
    verbosity: int
        0: no prints
        1: final dataframe head
        2: final and original dataframe heads
        3: Print full final dataframe and original head.
        4: Print full final dataframe and full orignal dataframe
        
    start_delay: number
        How long in seconds to delay starting the presses.
        
    return_delay: number
        How long in seconds to delay returning after the presses.

    Returns
    -------
    None
    
    Notes
    -----
    1. key_recorder.py is a script that writes the recording to the recorded_keystrokes_fpath
        in the correct input format.
    '''
    df = pd.read_csv(recorded_keystrokes_fpath)
    df_events = create_event_dataframe(df)
    if verbosity == 1 or verbosity == 2:
        print('df_events.head()')
        print(df_events.head())
    elif verbosity >= 3:
        print('df_events')
        print(df_events)
    if verbosity == 2 or verbosity == 3:
        print('df.head()')
        print(df.head())
    elif verbosity >= 4:
        print('df')
        print(df)
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
    play_recorded_keystrokes('recorded_keystrokes.csv')