#framer.py

import cv2
import os
import argparse

#============================= DEFINE VARIABLES =============================
#set and initialize variables used throughout the rest of the program
debugger = False
quieter = False
output_folder = 'output'
pic_ext_type = "jpg"
vfile = ''
vfolder = ''
mod_value = 1

#============================= DEFINE ARGPARSE =============================
# contrust the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="Path to the video file - Program will quit if video file or folder not specified. Video option only works for a single file. Video file must exist.")
ap.add_argument("-f", "--folder", help="Path to the folder - Program will quit if video file or folder not specified. Folder option only works for a single folder. Folder must exist. If both video and folder arguments are given, folder will be chosen and video will be ignored.")
ap.add_argument("-o", "--output", help="Path to the output directory - Program will create a directory 'output' if none is given. Program will remove any files that exist in that directory. Be cautious.")
ap.add_argument("-e", "--extension", help="Extension Type of the files that will be created. By default, .jpg will be used. .png will also be supported")
ap.add_argument("-m", "--mod", help="Mod value that will used be filtered out frames, instead of every writing every single frame. If '5' is given as an argument for this flag, then 1 out of every 5 frames will be saved, the others filtered")
ap.add_argument("-q", "--quiet", help="true/false or t/f supported. This argument quiets video ")
ap.add_argument("-d", "--debug", help="true/false or t/f supported. This argument turns debugging prints on/off so you can see more information about current operations during video framing")
args = vars(ap.parse_args())

#============================= DEFINE FUNCTIONS =============================
#Preconditions: a dictionary containing keys video, folder, output, extension, quiet, and debug must be set
#Postconditions: None
#Arguments:
#   args        a dictionary containing all the keys for argument parsing
#Returns:
#   tfile, tfolder, toutput_folder, tpic_ext_type, tquieter, tdebugger      The values that are parsed out, given that validation has checked to make sure files exist, and values are possible
def parseAllArgs(args):
    #parse the arguments when program is used
    tfile, tfolder = parseVideoAndFolder(args)
    toutput_folder = parseOutputFolder(args)
    tpic_ext_type = parseExtension(args)
    tquieter = parseQuiet(args)
    tdebugger = parseDebug(args)
    tmod_value = parseMod(args)
    return tfile, tfolder, toutput_folder, tpic_ext_type, tquieter, tdebugger, tmod_value

#Preconditions: None
#Postconditions: None
#Arguments:
#   args        a dictionary containing video or folder keys. At least 1 must be something other than None
#Returns:
#   tfile, tfolder      A file or folder value in which actually exists. Program exits if it doesn't exist.
def parseVideoAndFolder(args):
    tfile = vfile
    tfolder = vfolder
    #neither video or folder argument used -> should quit program
    if args["video"] is None and args["folder"] is None:
        print("-v <VIDEO FILE PATH> or -f <FOLDER PATH> not defined\nPlease see HELP screen for more information about how to use this program")
        exit()
    #both video and folder argument
    elif args["video"] is not None and args["folder"] is not None:
        tfolder = args["folder"]
        if not os.path.exists(tfolder):
            print(f"Error: folder {tfolder} does not exist - Please verify path")
            exit()
    #video argument only
    elif args["video"] is not None:
        tfile = args["video"]
        if not os.path.exists(tfile):
            print(f"Error: file {tfile} does not exist - Please verify path")
            exit()
    #folder argument only
    elif args["folder"] is not None:
        tfolder = args["folder"]
        if not os.path.exists(tfolder):
            print(f"Error: folder {tfolder} does not exist - Please verify path")
            exit()
    return tfile, tfolder

#Preconditions: None
#Postconditions: None
#Arguments:
#   args        a dictionary containing output key that contains a possible but valid path
#Returns:
#   toutput_folder      a file path that may or may not exist already where frames will be outputed to
def parseOutputFolder(args):
    #output argument
    toutput_folder = output_folder
    if args["output"] is not None:
        toutput_folder = args["output"]
    return toutput_folder

#Preconditions: None
#Postconditions: None
#Arguments:
#   args        a dictionary containing extension key that contains either jpg or png. Other extensions may be supported, but not now.
#Returns:
#   tpic_ext_type       a valid extension of either png or jpg. If an incorrect value for the key is passed in, it's reverted to jpg
def parseExtension(args):
    #extension argument
    tpic_ext_type = pic_ext_type
    if args["extension"] is not None:
        tpic_ext_type = args["extension"]
        if tpic_ext_type != "jpg" and tpic_ext_type != "png":
            print(f"Error: extension {tpic_ext_type} not jpg or png - defaulting to jpg")
            tpic_ext_type = pic_ext_type
    return tpic_ext_type

#Preconditions: None
#Postconditions: None
#Arguments:
#   args        a dictionary containing quiet key that contains either true/t or false/f.
#Returns:
#   tquieter        a valid boolean value either True/False. If anything else is given, the value is reverted back to False
def parseQuiet(args):
    #quiet argument
    tquieter = quieter
    if args["quiet"] is not None:
        tquieter = args["quiet"].lower()
        if tquieter == "true" or tquieter == "t":
            tquieter = True
        elif tquieter == "false" or tquieter == "f":
            tquieter = False
        else:
            print(f"Error: quieter argument {tquieter} not true/false or t/f - defaulting to false")
            tquieter = quieter
    return tquieter

#Preconditions: None
#Postconditions: None
#Arguments:
#   args        a dictionary containing debug key that contains either true/t or false/f.
#Returns:
#   tquieter        a valid boolean value either True/False. If anything else is given, the value is reverted back to False
def parseDebug(args):
    #debug argument
    tdebugger = debugger
    if args["debug"] is not None:
        tdebugger = args["debug"].lower()
        if tdebugger == "true" or tdebugger == "t":
            tdebugger = True
        elif tdebugger == "false" or tdebugger == "f":
            tdebugger = False
        else:
            print(f"Error: debugger argument {tdebugger} not true/false or t/f - defaulting to false")
            tdebugger = debugger
    return tdebugger

#Preconditions: None
#Postconditions: None
#Arguments:
#   args        a dictionary containing mod key that contains an integar.
#Returns:
#   tquieter        a valid integar value for a mod operation during framing. If anything invalid is given, 0 is returned back which frames everything
def parseMod(args):
    #debug argument
    tmod_value = mod_value
    if args["mod"] is not None:
        try:
            temp_val = args["mod"]
            tmod_value = int(temp_val)
        except Exception as err:
            print(f"Error: mod argument {temp_val} not a valid int - defaulting to 0")
            tmod_value = mod_value
    return tmod_value

#Preconditions: None
#Postconditions: None
#Arguments:
#   folder          The folder that we are removing all files and sub-folders from. This doesn't have to exist prior.
#Returns:
#   None
def clearOutputFolder(folder):
    #if folder doesn't exist, then just create it. 
    if not os.path.exists(folder):
        os.mkdir(folder)
        if debugger:
            print(f"Directory {folder} Created")
    #else folder must already exist, so remove all files and directories
    else:
        filelist = os.listdir(folder)
        #go through each file/folder
        for f in filelist:
            #if is a directory, remove all sub-files and then remove the directory
            if os.path.isdir(os.path.join(folder, f)):
                clearOutputFolder(os.path.join(folder, f))
                os.rmdir(os.path.join(folder, f))
            #else it must be a file, which can just be removed
            else:
                os.remove(os.path.join(folder, f))
        if debugger:
            print(f"Directory {folder} Should Be Empty Now...")

#Preconditions: None
#Postconditions: None
#Arguments:
#   folder          The folder that the frames will be stripped into
#   file            The file that the frames will be stripped from
#Returns:
#   None
def frameFile(folder, file):
    if debugger:
        print(f"STARTING FILE:", file)
    #create video capture object
    video_capture_obj = cv2.VideoCapture(file)
    #read initial another image
    is_success, image = video_capture_obj.read()
    #count frames starts at 0
    count = 0
    count_written = 0
    while is_success:
        #create output file name
        outfilename = f"{folder}/frame{str(count)}.{pic_ext_type}"
        # write/save frame as a file unless it should be filtered out. Always write the first frame.
        if count % mod_value == 0 or count == 0:
            cv2.imwrite(outfilename, image)
            count_written += 1
        #read another image
        is_success, image = video_capture_obj.read()
        count += 1
    if not quieter:
        print(f"Expected FPS:\t\t{int(video_capture_obj.get(cv2.CAP_PROP_FPS))}")
        print(f"Expected Total Frames:\t{int(video_capture_obj.get(cv2.CAP_PROP_FRAME_COUNT))}")
        try:
            print(f"Expected Duration:\t{int(float(video_capture_obj.get(cv2.CAP_PROP_FRAME_COUNT)) / float(video_capture_obj.get(cv2.CAP_PROP_FPS)))} seconds")
        except Exception as err:
            print(f"Error in determining Duration Probaly due to 0 Frames Found")
    print(f"Actual Frames Written to {folder}:\t{count_written}/{count}")

#Preconditions: None
#Postconditions: None
#Arguments:
#   out_folder      The folder that the frames will eventually go into. Sub-folders have to be created first for each file.
#   folder          The folder that possibly multiple video files are in now. Program must go through each of these individually
#Returns:
#   None
def frameFolder(out_folder, folder):
    if debugger:
        print(f"STARTING FOLDER:", folder)
    #list of all video files that are .avi, .mp4, .mkv. Others could be supported easily too.
    all_video_files = [f for f in os.listdir(folder) if f.lower().endswith('.avi') or f.lower().endswith('.mkv') or f.lower().endswith('.mp4')]
    if debugger:
        print(all_video_files)
    #go through each video
    for next_video in all_video_files:
        #get the path of the video included with the file name
        next_video_with_path = os.path.join(folder, next_video)
        #get the output path, that will now be in the output folder's subdirectory of the file's name
        next_output_with_path = os.path.join(output_folder, next_video)
        #make the output's sub-folder, as it doesn't exist yet
        os.mkdir(next_output_with_path)
        #frame the file like normally
        frameFile(next_output_with_path, next_video_with_path)

#============================= DRIVER START =============================

#parse all arguments into pre-defined variables
vfile, vfolder, output_folder, pic_ext_type, quieter, debugger, mod_value = parseAllArgs(args)
#always clear output_folder contents and sub-directories. This is a potentially dangerous operation
clearOutputFolder(output_folder)
#if video file has been passed in as an argument, then call frameFile Function
if vfile != '':
    frameFile(output_folder, vfile)
#else it's probably a folder, otherwise program would have exited before this point
elif vfolder != '':
    frameFolder(output_folder, vfolder)
exit()