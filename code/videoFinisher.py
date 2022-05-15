import argparse
import os.path
import os
import subprocess

def emptyFolder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    try:
        os.rmdir(folder)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (folder, e))


parser = argparse.ArgumentParser(description='blah')
parser.add_argument('--input_file', type=str,  help='the script')
parser.add_argument('--keep_frames', type=str,  help='do you want to keep the thousands of frame still images, or delete them?')
args = parser.parse_args()
INPUT_FILE = args.input_file
KEEP_FRAMES = args.keep_frames



command = "ffmpeg -r 30 -f image2 -s 1920x1080 -i "+INPUT_FILE+"_frames/f%06d.png -i "+INPUT_FILE+".wav -vcodec libx264 -b 4M -c:a aac -strict -2 "+INPUT_FILE+"_final.mp4 "
subprocess.call(command, shell=True)

if KEEP_FRAMES == "F":
    emptyFolder(INPUT_FILE+"_frames")
