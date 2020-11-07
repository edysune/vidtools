#audior.py
import argparse
import subprocess
import speech_recognition as sr

#============================= DEFINE VARIABLES =============================
#set and initialize variables used throughout the rest of the program


#============================= DEFINE ARGPARSE =============================
# contrust the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", help="input file")
ap.add_argument("-o", "--output", help="output file.")
ap.add_argument("-a", "--audio_extract", help="extracts the audio of a movie.", action='store_true')
ap.add_argument("-s", "--subtitle_extract", help="extracts the subtitles of a movie.", action='store_true')
ap.add_argument("-t", "--create_transcript", help="creates a transcript of the movie or audio file.", action='store_true')

args = vars(ap.parse_args())


def startAudior():
    print(args)
    if args["audio_extract"]:
        extractAudioFromMovie()
    elif args["subtitle_extract"]:
        extractAudioFromMovie()
    elif args["create_transcript"]:
        createTranscriptFromAudio()
    else:
        print("Error - no operation specified")
        return
    

def ValidateInputAndOutput():
    if args["input"] is None or args["output"] is None:
        print("Error - no input and output specified")
        return False
    return True

#Feature 1 - Extract Audio
#   Requirements: ffmpeg must be installed
def extractAudioFromMovie():
    if not ValidateInputAndOutput():
        return
    command = f"ffmpeg -i \"{args['input']}\" -vn \"{args['output']}\""
    subprocess.call(command, shell=True)

#Feature 2 - Extract Subtitles
def extractSubtitlesFromMovie():
    if not ValidateInputAndOutput():
        return
    command = f"ffmpeg -i \"{args['input']}\" \"{args['output']}\""
    subprocess.call(command, shell=True)

#Feature 3 - Generate Transcriptions
def createTranscriptFromAudio():
    #if not ValidateInputAndOutput():
    #    return

    af = sr.AudioFile('howls.wav')
    with af as source:
        audio = r.record(source, duration=4)

    r = sr.Recognizer()
    r.recognize_sphinx(audio)

    #recognize_bing(): Microsoft Bing Speech
    #recognize_google(): Google Web Speech API
    #recognize_google_cloud(): Google Cloud Speech - requires installation of the google-cloud-speech package
    #recognize_houndify(): Houndify by SoundHound
    #recognize_ibm(): IBM Speech to Text
    #recognize_sphinx(): CMU Sphinx - requires installing PocketSphinx
    #recognize_wit(): Wit.ai



#Feature 4 - Create SRT From Audio
#Feature 5 - Upload SRT
#Feature 6 - Convert To SRT
#Feature 7 - Remove All Subtitles
#Feature 8 - Time Shift Subtitles for X Starting at time Y

#============================= RUN PROGRAM =============================

startAudior()