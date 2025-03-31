# Trigger Bot (Auto Fire Assistant)
This script is a Trigger Bot that scans a small zone at the center of your screen and automatically presses a key (e.g. "k") when it detects a target color. It is intended for educational and experimental purposes only.

* ⚠️ Do not use this software to violate the terms of service of any application or game. Use responsibly.
## Dependencies
* Python 3.7+

* mss

* numpy

* keyboard

* pywin32
  ``` bash
  pip install mss numpy keyboard pywin32
## How It Works
* The script monitors a small region at the center of the screen.

* If it detects a pixel that matches the target RGB color (with tolerance), it presses the "k" key.

* There are two modes:

  * Always Enabled: toggle on/off with F10

  * Hold Mode: only active while holding the trigger_hotkey

* Press Ctrl + Shift + X to safely exit the script at any time.
## Disclaimer
* Do not use this with any software or game that prohibits automation

* The developer is not responsible for any misuse

* Use for learning, testing, or local automation purposes only
## Getting Started
1. Create your config.json with the settings you want.

2. Run the script:
   ``` bash
   python main.py
3. Use it according to your selected mode (always_enabled or hold)
## License
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

For more information, please refer to: https://unlicense.org
