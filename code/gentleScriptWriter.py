import argparse
import os.path
from utils import removeTags

parser = argparse.ArgumentParser(description='blah')
parser.add_argument('--input_file', type=str,  help='the script')
args = parser.parse_args()
INPUT_FILE = args.input_file

with open(INPUT_FILE+".txt","r+") as f:
  script = f.read()

with open(INPUT_FILE+"_g.txt","w+") as f:
  f.write(removeTags(script))  # This will automatically flush anyway

print("Done creating the gentle-friendly script!")
