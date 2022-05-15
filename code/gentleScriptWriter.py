import argparse
import os.path
from utils import removeTags

parser = argparse.ArgumentParser(description='blah')
parser.add_argument('--input_file', type=str,  help='the script')
args = parser.parse_args()
INPUT_FILE = args.input_file

f = open(INPUT_FILE+".txt","r+")
script = f.read()
f.close()

f = open(INPUT_FILE+"_g.txt","w+")
f.write(removeTags(script))
f.flush()
f.close()
print("Done creating the gentle-friendly script!")
