import argparse
import os.path
from os import path
import subprocess
import shutil
import os, random
import time
import requests
import json
from pathlib import Path
import imageio

def getSearchTermFromLine(line):
    BAD_ENDINGS = ['.',',',' ','?',';','!','-',':']
    searchTerm = line
    if '[' in line:
        s = line.index('[')+1
        e = line.index(']')
        searchTerm = line[s:e]
    while "  " in searchTerm:
        searchTerm = searchTerm.replace("  "," ")
    if len(searchTerm) == 0:
        return ""
    while searchTerm[0] in BAD_ENDINGS:
        searchTerm = searchTerm[1:]
    while searchTerm[-1] in BAD_ENDINGS:
        searchTerm = searchTerm[0:-1]
    return searchTerm.lower()

"""def downloadImageForTerm(term):
    command = 'python google-images-download-master/bing_scraper.py --search "'+term+'" --limit 3 --download --chromedriver "C:/Users/caryk/Documents/YouTube Videos/GoogleImager/chromedriver.exe"'
    subprocess.call(command, shell=True)
    underScoredTerm = term.replace(" ","_")
    source = "images/"+underScoredTerm+"/"+random.choice(os.listdir("images/"+underScoredTerm))
    destination = "lookup/"+term+".jpg"
    shutil.copyfile(source, destination)
    time.sleep(5)"""

def downloadImageForTerm(term):

    Path("dict/"+term).mkdir(parents=True, exist_ok=True)

    r = requests.get('https://www.googleapis.com/customsearch/v1',
  params={
    'q': term,
    'cx': '008869571965829350955:lxfnn3lgylk',
    'searchType': 'image',
    'num': '5',
    'safe': 'active', # Safe search on
    'tbs':'sur', # only use images that you're allowed to 'reuse' (Usage Rights)
    'key': 'AIzaSyB4toPM9w-9yGz4HdajtSmOBStGzxoKen4'})

    count = 0
    rContentStr = r._content.decode("utf-8")
    content = json.loads(rContentStr)

    FILEPATH = 'dict/'+term

    # https://www.google.com/search?q=rabbit&tbm=isch&safe=active&safe=active&tbs=sur%3Afc&rlz=1C5CHFA_enUS696US709&hl=en&ved=0CAIQpwVqFwoTCPiCiuybn-oCFQAAAAAdAAAAABAC&biw=1157&bih=557
    # https://www.google.com/search?q=rabbit&tbm=isch&hl=en&hl=en&safe=active&safe=active&tbs&rlz=1C5CHFA_enUS696US709&ved=0CAEQpwVqFwoTCOiA3becn-oCFQAAAAAdAAAAABAC&biw=1157&bih=557
    # https://www.google.com/search?q=rabbit&tbm=isch&hl=en&hl=en&safe=active&safe=active&tbs=sur%3Afmc&rlz=1C5CHFA_enUS696US709&ved=0CAIQpwVqFwoTCJiLh7Kdn-oCFQAAAAAdAAAAABAC&biw=1157&bih=557
    # https://www.google.com/search?q=rabbit&tbm=isch&hl=en&hl=en&safe=active&safe=active&tbs=sur%3Afm&rlz=1C5CHFA_enUS696US709&ved=0CAMQpwVqFwoTCLD96rudn-oCFQAAAAAdAAAAABAC&biw=1157&bih=557

    for item in content["items"]:
        image_url = item["link"]
        img_data = requests.get(image_url).content
        with open(FILEPATH+'/'+term+"_"+str(count), 'wb') as handler:
            handler.write(img_data)
            count += 1

    fileList = os.listdir(FILEPATH)
    for fileP in fileList:
        try:
            img = imageio.imread(FILEPATH+"/"+fileP)
            imageio.imwrite(FILEPATH+"/"+fileP+".png", img)
        except:
            print("Weird. "+fileP+" failed.")
        os.remove(FILEPATH+"/"+fileP)



    fileList = os.listdir(FILEPATH)
    source = FILEPATH+"/"+random.choice(fileList)
    destination = "lookuptest/"+term+".png"
    shutil.copyfile(source, destination)
    print("********** Just got images for "+term+"! **********")
    time.sleep(5)


parser = argparse.ArgumentParser(description='blah')
parser.add_argument('--input_file', type=str,  help='the script')
args = parser.parse_args()
INPUT_FILE = args.input_file

f = open(INPUT_FILE+".txt","r+",encoding="utf-8")
script = f.read()
f.close()

scriptLines = script.replace("/","\n").split("\n")
for line in scriptLines:
    #print("LINE: "+line)
    searchTerm = getSearchTermFromLine(line)
    #print("SEARCH: "+str(searchTerm))
    if len(searchTerm) >= 1:
        filePath = "lookuptest/"+searchTerm+".png"
        if not path.exists(filePath):
            downloadImageForTerm(searchTerm)
