# lazykh
This Github repo has the source code for the automatic lip-syncing project described in this video! https://www.youtube.com/watch?v=y3B8YqeLCpY

To create a video using this lazykh code, there are 5 commands you will need to run.

## Things to know before starting
For Step 2, "Gentle" (the phoneme detection library I'm using) will only work on Mac OS. However, Steps 1, 3, 4, and 5 can be done on any computer. Install "gentle", the phoneme detection library, from here: https://lowerquality.com/gentle/

Put the "gentle-final" folder in the "lazykh" folder. (This is around 3 GB, so be prepared for the large size.) Estimated runtimes are based on my 2015 MacBook Pro, so your results may vary. (Hopefully, they are faster!)

If you're a cool person, please provide credit to me (Cary Huang) when you use this! All it needs to be is a quick mention that you're using software written by carykh spoken in the video, and we're good. I'm making this code open source because I'm just excited to see how other content creators can innovate with this tool, so I don't care too much about clout, financial gain, or legal ownership. I just want to see people being clever/expressive/funny with their videos! But despite that, I'd still appreciate being acknowledged.

Also, aside from easy-to-fix bugs, I won't be maintaining this repo or providing assistance to others. Think of this repo as an archive of how my personal passion project worked. It's not like Adobe's constantly-maintained software, it's just one guy spewing random hobby projects onto the internet! (I go more into detail describing this in my "lazykh goodbye" video: https://www.youtube.com/watch?v=hkOGbehVeQs)

## Creating an actual lazykh video
For this example, suppose your video's audio file is "exampleVideo/ev.wav", and your annotated script file is "exampleVideo/ev.txt". These should be placed in lazykh folder, so the addresses are "lazykh/exampleVideo/ev.wav" and "lazykh/exampleVideo/ev.txt"

### Step 1 - Remove the annotations from the script to make it "gentle-friendly" (Runtime: instant)
Open a command prompt, go to the lazykh folder, and run this command. This will create ev_g.txt
```
python3 code/gentleScriptWriter.py --input_file exampleVideo/ev
```

### Step 2 - Calculate phoneme timestamps (Runtime: 2 minutes for a 5-min video)
Run this command, which will create ev.json.
```
python3 gentle-final/align.py exampleVideo/ev.wav exampleVideo/ev_g.txt -o exampleVideo/ev.json
```

### Step 3 - Create a simplified timetable (Runtime: 2 seconds for a 5-min video)
Run this command, which will create ev_schedule.json
```
python3 code/scheduler.py --input_file exampleVideo/ev
```

### Step 4 - Render the frames (Runtime: 1 hour for a 5-min video)
Run this command, which will create thousands of image files. (30 images per second of final video)
```
python3 code/videoDrawer.py --input_file exampleVideo/ev --use_billboards F --jiggly_transitions F
```

### Step 5 - Convert the image sequence to a video and add audio (Runtime: 8 minutes for a 5-min video)
Run this command, which will create the video file and delete all the frame files
```
python3 code/videoFinisher.py --input_file exampleVideo/ev --keep_frames F
```

If you want to start working on more video projects with different filepaaths, replace "exampleVideo/ev" with the new video's filepath in all the commands above before running them. It should work for your new videos.


## Alternate settings
Running the 5 standard commands listed above will give you a video with no synchronized billboards to the side of the avatar-speaker-talking-guy. If you want to include billboards drawings, do these steps between steps 3 and 4:

### Step 3.1
Run this command to launch a pygame applet that lets the user draw really crappy scribbles for each line of the script.
```
python3 code/humanImager.py --input_file exampleVideo/ev
```
When the applet gives you a line, you have 30 seconds to draw it in the given zone. You can hit SPACE to advance to the next line early. Also, you can hit ESCAPE to exit if you mess up, and then run the code again. (It will save all the billboards you've finished.)

### Step 3.2
There will be the folder lazykh/exampleVideo/ev_billboards that contains all the billboard files. Feel free to swap them out with any other image, like legitimate artwork, or something from the internet.

### Step 4-alt
Run the same command as Step 4, but be sure to change the "use-billboards" argument to "T" (true).
```
python3 code/videoDrawer.py --input_file exampleVideo/ev --use_billboards T --jiggly_transitions F
```
