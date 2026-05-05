This repository contains:
- The latest version of the Python LED controller.
  - This cannot be used without the physical prototype.
  - Technically, it will run if connected to any device that uses serial port: `COM3` on Windows or `/dev/tty/ACM0` on Linux devices.
- The Arduino firmware, in C++.
- A version of the Python LED controller for an examiner to run on their computer if they wish.
  - This version will work without the physical prototype because all serial communication has been disabled.
---

In an IDE, run `main.py`.

To run in the program in a terminal:
1) Navigate to directory containing `main.py`. 
```cd [path-to-directory]/main.py ```
2) Run the command:
```python main.py```
