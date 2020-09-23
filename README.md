This Repo provides various python tools for videos.

framer.py - Takes a Movie file, and splits it into frames.

motion_detector.py - Takes a Movie file, and detects motion, removing out all frames that do not have any significant change.

Install Steps:
1. Python3
2. pip3 install scikit-build
3. pip3 install cmake
4. pip3 install opencv-python
5. Any issues with opencv-python, upgrade pip first (pip3 install --upgrade pip)
6. pip3 install imutils
7. pip3 install imageio

Todo for future updates:
1. Encoding Features for motion_detector.py
2. GUI options for all utilities
3. Better usage of shared libraries - remove redundancies
4. Useage for Threading, allowing better performance for folders
5. Unit tests, and added tests