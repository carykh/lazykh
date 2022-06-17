# lazykh
This Github repo has the source code for the automatic lip-syncing project described in these videos:

2020: https://www.youtube.com/watch?v=y3B8YqeLCpY 

2022 (includes walkthrough tutorial): https://www.youtube.com/watch?v=ItVnKlwyWwA

Creating a video using this lazykh code is a 1-step-process! (YES REALLY!!!) 

## Things to know before starting
For Step 2, "Gentle" (the phoneme detection library I'm using) will only work on Mac OS. However, Steps 1, 3, 4, and 5 can be done on any computer. The source code for "gentle" comes from here: https://github.com/lowerquality/gentle. However, I've found the only way to get gentle to work is to run this command, ideally from within the lazykh folder:
```
sudo pip install Twisted==16.4.1
git clone https://github.com/lowerquality/gentle.git
cd gentle
./install.sh
```

Put the "gentle-final" folder in the "lazykh" folder. (This is around 400MB-3GB, so be prepared for the large size.) Estimated runtimes are based on my 2015 MacBook Pro, so your results may vary. (Hopefully, they are faster!)

If you're a cool person, please provide credit to Cary Huang when you use this! All I did, is made it more user friendly... The project itself is by carykh

I'm assuming you already know how to make a lazykh video...

## Creating an actual lazykh video
HAH CARY i made it 1 FILE ONLY! MWHAHHH

### Step 1
open a terminal and run:
```
sh LAZYKH.sh (drag and drop the file
```

### Step 2
do what the thingy says. EVERYTHINg. When it says: "Where is this? blablabla", drag the folder/file to the terminal window. there are alot of prompts to fill in but it's fineeee

### Step 3
there is no step 3. thats all. LOL


## Alternate settings (adding billboards)
oh yeah if u want billboards just fill in the prompt when it asks you.
