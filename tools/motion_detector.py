# USAGE
# python motion_detector.py
# python motion_detector.py --video videos/example_01.mp4

# import the necessary packages
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import os
import imageio
import glob
from PIL import Image

#============================= DEFINE VARIABLES =============================
#set and initialize variables used throughout the rest of the program
debugger = False
quieter = True
vfile = ''
vfolder = ''
output_folder = 'output'
default_video_output_name = 'out.avi'
duration = 1
makemovie = False
remove_pictures_at_end = False

RED = (0, 0, 255)
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
TEXT_COLOR = GREEN

frame_picture_extension_default = ".png"

#============================= DEFINE ARGPARSE =============================
# contrust the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="Path to the video file - Program will quit if video file or folder not specified. Video option only works for a single file. Video file must exist.")
ap.add_argument("-f", "--folder", help="Path to the folder - Program will quit if video file or folder not specified. Folder option only works for a single folder. Folder must exist. If both video and folder arguments are given, folder will be chosen and video will be ignored.")
ap.add_argument("-o", "--output", help="Path to the output directory - Program will create a directory 'output' if none is given. Program will remove any files that exist in that directory. Be cautious.")
ap.add_argument("-d", "--duration", help="Duration of time in seconds where the motion detector keeps saving frames after initial detection. Default is 1 second.")
ap.add_argument("-m", "--movie", action="store_true", help="Turns on gif generation from files. Off by default.")
ap.add_argument("-c", "--color", default='o', choices=["r", "red", "g", "green", "b", "blue", "o", "off"], help="Indicates color of motion detecting frame /{r/red, g/green, b/blue, o/off/}")
ap.add_argument("-n", "--no_picture_output", action="store_true", help="")
ap.add_argument("-a", "--min-area", type=int, default=400, help="minimum area size")
args = vars(ap.parse_args())

#============================= DEFINE FUNCTIONS =============================
def parseAllArgs(args):
    #parse the arguments when program is used
    tfile, tfolder = parseVideoAndFolder(args)
    toutput_folder = parseOutputFolder(args)
    tcolor = parseColor(args)
    tduration = parseDuration(args)
    tmovie = parseMovie(args)
    t_no_picture_output = parsePictureOutput(args)
    return tfile, tfolder, toutput_folder, tcolor, tduration, tmovie, t_no_picture_output

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

def parseMovie(args):
    #output argument
    return args["movie"] 

def parsePictureOutput(args):
    #output argument
    return args["no_picture_output"]

def parseColor(args):
    #output argument
    tcolor = TEXT_COLOR
    if args["color"] is not None:
        tcolor = args["color"][0]
        if(tcolor == 'r'):
            return RED
        elif(tcolor == 'b'):
            return BLUE
        elif(tcolor == 'g'):
            return GREEN
        elif(tcolor == 'o'):
            return False
        else:
            print(f"Error: option {tcolor} color is not a valid option apparently - Please verify argument")

    return tcolor

def parseDuration(args):
    #output argument
    tduration = duration
    if args["duration"] is not None:
        try:
            temp_val = args["duration"]
            tduration = int(temp_val)
            if(tduration < 0):
                print(f"Error: duration argument {tduration} not a positive int - defaulting to 1")
                tduration = 1
        except Exception as err:
            print(f"Error: duration argument {temp_val} not a valid int - defaulting to 1")
            tduration = 1
    return tduration


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
#   folder          
#   file            
#Returns:
#   None
def detectMotionOnFile(folder, file):
    if debugger:
        print(f"STARTING FILE:", file)
    #create video capture object
    video_capture_obj = cv2.VideoCapture(file)
    #read initial another image
    is_success, current_image = video_capture_obj.read()
    #count frames starts at 0
    count = 0
    count_written = 0

    fps = int(video_capture_obj.get(cv2.CAP_PROP_FPS))
    total_expected_frames = int(video_capture_obj.get(cv2.CAP_PROP_FRAME_COUNT))
    framesLeftToPrint = 0

    previous_image = None

    while is_success:
        text = "Unoccupied"

        image_before_resize = current_image
        current_image = imutils.resize(current_image, width=500)

        #make the image Grey
        grey_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
        #blur the image
        grey_image = cv2.GaussianBlur(grey_image, (21, 21), 0)

        if previous_image is None:
            previous_image = grey_image
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(previous_image, grey_image)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < args["min_area"]:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            if TEXT_COLOR != False:
                cv2.rectangle(current_image, (x, y), (x + w, y + h), TEXT_COLOR, 2)
            text = "Occupied"

        # draw the text and timestamp on the frame
        if TEXT_COLOR != False:
            cv2.putText(current_image, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, TEXT_COLOR, 2)
            cv2.putText(current_image, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, current_image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, TEXT_COLOR, 1)

        outfilename = f"{folder}/frame{str(count)}{frame_picture_extension_default}"

        #write an image out
        #cv2.imwrite(outfilename, image)
        if text == "Occupied" or framesLeftToPrint > 0:
            count_written += 1
            if TEXT_COLOR == False:
                #frames.append(image_before_resize)
                cv2.imwrite(outfilename, image_before_resize)
            else:
                cv2.imwrite(outfilename, current_image)
                #frames.append(current_image)
            if text == "Occupied":
                framesLeftToPrint = fps * duration
            else:
                framesLeftToPrint -= 1

        #Get next Frame
        is_success, current_image = video_capture_obj.read()

        count += 1

        printProgressBar(count + 1, total_expected_frames, prefix = f'Progress On {file}:\t', suffix = 'Complete', length = 50)

        previous_image = grey_image

    printProgressBar(total_expected_frames, total_expected_frames, prefix = f'Progress On {file}:\t', suffix = 'Complete', length = 50)
    printStats(fps, total_expected_frames, folder, count_written)

    if makemovie:
        writeVideo(folder, fps)
    if remove_pictures_at_end:
        clearImages(folder)

def printStats(fps, total_expected_frames, folder, count_written):
    if not quieter:
        print(f"Expected FPS:\t\t{fps}")
        print(f"Expected Total Frames:\t{total_expected_frames}")
        try:
            print(f"Expected Duration:\t{ int(total_expected_frames / fps)} seconds")
        except Exception as err:
            print(f"Error in determining Duration Probaly due to 0 Frames Found")
        print(f"Actual Frames Written to {folder}:\t{count_written}/{count}")


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def clearImages(folder):
    images = [img for img in os.listdir(folder) if img.endswith(".png") or  img.endswith(".jpg") or  img.endswith(".jpeg")]
    for image in images:
        os.remove(os.path.join(folder, image))

def writeGif(folder, fps):
    all_images = [img for img in os.listdir(folder) if img.endswith(frame_picture_extension_default)]

    fp_in = folder + f"/*{frame_picture_extension_default}"
    fp_out = folder + "/out.gif"

    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
        save_all=True, duration=int(len(all_images)/fps), loop=0)
    '''
    with imageio.get_writer(folder + "/" + "out.gif", mode='I') as writer:
        for img in all_images:
            image = imageio.imread(folder + "/" + img)
            writer.append_data(image)
    '''

def writeVideo(folder, frame_rate):
    image_folder = f'{folder}'
    video_name = os.path.join(image_folder, default_video_output_name)

    images = [img for img in os.listdir(image_folder) if img.endswith(".png") or  img.endswith(".jpg") or  img.endswith(".jpeg")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, frame_rate, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

#Preconditions: None
#Postconditions: None
#Arguments:
#   out_folder      The folder that the frames will eventually go into. Sub-folders have to be created first for each file.
#   folder          The folder that possibly multiple video files are in now. Program must go through each of these individually
#Returns:
#   None
def detectMotionOnFolder(out_folder, folder):
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
        detectMotionOnFile(next_output_with_path, next_video_with_path)


    #print(f"Actual Frames Written to {folder}:\t{count_written}/{count}")

#============================= DRIVER START =============================

#parse all arguments into pre-defined variables
vfile, vfolder, output_folder, TEXT_COLOR, duration, makemovie, remove_pictures_at_end = parseAllArgs(args)
#always clear output_folder contents and sub-directories. This is a potentially dangerous operation
clearOutputFolder(output_folder)
#if video file has been passed in as an argument, then call detectMotionOnFile Function
if vfile != '':
    detectMotionOnFile(output_folder, vfile)
elif vfolder != '':
    detectMotionOnFolder(output_folder, vfolder)
exit()