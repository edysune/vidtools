This Repo provides various python tools for videos.

framer.py - Takes a Movie file, and splits it into frames.

motion_detector.py - Takes a Movie file, and detects motion, removing out all frames that do not have any significant change.

Install Steps (framer/motion_detector):
1. Python3
2. pip3 install scikit-build
3. pip3 install cmake
4. pip3 install opencv-python
5. Any issues with opencv-python, upgrade pip first (pip3 install --upgrade pip)
6. pip3 install imutils
7. pip3 install imageio

audior.py - Takes a Movie file, and performs various operations relating to audio and subtitles.

Install Steps (audior):
1. If using Windows, download VisualStudios C++ build tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. pip3 install SpeechRecognition
3. Install ffmpeg: https://ffmpeg.org/download.html
4. If using Windows, install swig: https://netix.dl.sourceforge.net/project/swig/swigwin/swigwin-3.0.12/swigwin-3.0.12.zip
5. pip3 install SpeechRecognition
6. pip install PocketSphinx




Todo for future updates:
1. Encoding Features for motion_detector.py
2. GUI options for all utilities
3. Better usage of shared libraries - remove redundancies
4. Useage for Threading, allowing better performance for folders
5. Unit tests, and added tests