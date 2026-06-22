ECG from a Polar H10
====================

A tiny, hackable Python toolkit for streaming raw ECG straight off a Polar H10
chest strap over Bluetooth LE — no app, no cloud, no account. Just your heart,
a CSV file, and a graph.

Why this exists
---------------

The Polar H10 is one of the few consumer chest straps that exposes a real ECG
waveform (130 Hz, 14-bit) through its Measurement Data service. Most apps hide
that signal behind heart-rate numbers and lock the data inside their ecosystem.
This project skips the middlemen: connect, stream, save, plot. About 100 lines
of code, end to end.

What you get
------------

  scan.py   Discover nearby BLE devices and find your strap's address.
  main.py   Connect to the H10, stream 30 seconds of ECG, write ecg.csv.
  plot.py   Read the CSV and render the waveform with matplotlib.

The output is a two-column CSV (time_s, ecg_uv) — friendly to pandas, NumPy,
SciPy, R, a spreadsheet, or whatever you want to throw at it. Roll your own
QRS detector, compute HRV, train a model, or just stare at your own heartbeat
on a Tuesday evening. It's surprisingly meditative.

Quick start
-----------

  uv sync
  uv run python scan.py     # copy your H10's address into main.py
  uv run python main.py     # wear the strap, record 30 seconds
  uv run python plot.py     # see your heart

Requirements: Python 3.13+, a Polar H10, and a machine with Bluetooth LE.
Tested on macOS; Linux and Windows should work via bleak.

Hack it
-------

The recording length, sample handling, and plotting are all a few lines each.
Change the sleep in main.py to record longer. Pipe ecg.csv into your own
analysis. Add a real-time plot. Detect arrhythmias. Make art out of your
pulse. The point is that the signal is yours — do something with it.

License
-------

Public repo, take what's useful. No warranty: this is a hobby tool, not a
medical device. If something on the graph worries you, talk to a doctor, not
a Python script.
