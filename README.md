# key_recorder_and_player
Record a series of keystrokes and play them back with the same timings as when recorded.

Run 
```
python key_recorder.py
```
or execute
```
key_recorder.record_keys()
```
to begin recording. Press esc when done. Run
```
python recorded_keystrokes_player.py
```
or execute
```
recorded_keystrokes_player.play_recorded_keystrokes(recorded_keystrokes_fpath)
```
to have the computer play back the keystrokes. (Running it has a start delay you can change).

## Installation

```
python setup.py develop
```
