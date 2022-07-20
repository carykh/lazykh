# lazykh
This Github repo has the source code for the automatic lip-syncing project described in these videos:

2020: https://www.youtube.com/watch?v=y3B8YqeLCpY 

2022 (includes walkthrough tutorial): https://www.youtube.com/watch?v=ItVnKlwyWwA

Creating a video using this lazykh code is a 5-step-process! (That sounds intimidating, but some steps take under 5 seconds.) 

2022-07-20 UPDATE: I added frame-caching to Step 4 (frame drawing), which speeds up the frame-drawing by about 5 times! (Now, if it detects that the current frame has the exact same parameters as a previously-rendered frame, it will just copy-paste that frame, which is much faster.) So, to render a 5-minute video, it only takes around 10-12 minutes on my machine, instead of one hour.

## Things to know before starting
For Step 2, "Gentle" (the phoneme detection library I'm using) will only work on Mac OS. However, Steps 1, 3, 4, and 5 can be done on any computer. The source code for "gentle" comes from here: https://github.com/lowerquality/gentle. However, I've found the only way to get gentle to work is to run this command, ideally from within the lazykh folder:
```
sudo pip install Twisted==16.4.1
git clone https://github.com/lowerquality/gentle.git
cd gentle
./install.sh
```

Put the "gentle-final" folder in the "lazykh" folder. (This is around 3 GB, so be prepared for the large size.) Estimated runtimes are based on my 2015 MacBook Pro, so your results may vary. (Hopefully, they are faster!)

If you're a cool person, please provide credit to me (Cary Huang) when you use this! All it needs to be is a quick mention that you're using software written by carykh spoken in the video, and we're good. I'm making this code open source because I'm just excited to see how other content creators can innovate with this tool, so I don't care too much about clout, financial gain, or legal ownership. I just want to see people being creative with their videos! But yeah, I'd still appreciate being acknowledged. :)

Also, aside from easy-to-fix bugs, I won't be maintaining this repo or providing assistance to others. Think of this repo as an archive of how my personal passion project worked. It's not like Adobe's constantly-maintained software, it's just one guy spewing random hobby projects onto the internet! (I go into a more detailed discussion of this in my "lazykh goodbye" video: https://www.youtube.com/watch?v=hkOGbehVeQs)

## The script
The script is a .txt file that tells Gentle what words you're actually saying, and it should match your spoken audio as close as possible, if not perfectly. Read through example/ev.txt for an example.

You'll notice that occasionally, the text in ev.txt are synonym words to what I actually say. For example, instead of "Cary-ness" (which is what I say), ev.txt contains the words "caring es". Simiarly, instead of "Minecraft", it has "Mine craft". This is because Gentle's dictionary only contains common words. If you include a word in the script that Gentle doesn't know, the stick figure will just not lip-sync that word at all, which isn't ideal. The janky solution is to type common words that produce the same mouth shapes as the uncommon word, to get the same desired effect. For example, I might say the word "Amogus" in the audio, but since that word is so recent, Gentle doesn't know it. I might type "Um hoe cuss" as a substitute, and hope Gentle can connect the dots. To find better substitutes, it's helpful to know which phonemes use the same letters (F/V,  B/P/M,  K/D/G/J/N/S/T/Z,  L/Y/H,  etc.).

Anything in triangle brackets is an emotion that is not verbally said. There are only 6 permitted emotions:
```
explain,happy,sad,angry,confused,rq

Example:

<happy> It would be really cool, to see other Minecraft players
playing around with my giant Earth.
<angry> I just hope they don't destroy it like my brother did last time!
```
Most of these are pretty self-explanatory. "Explain" is a generally positive emotion where the stick figure is giving the audience information, but not in an over-the-top happy way. "rq" stands for "rhetorical question", and will give the stick figure a shrug-like pose for questions like "But what is gnocchi anyway?" that are answered directly afterward. When you denote an emotion, the stick figure will become that emotion at that part of the script, and will retain that emotion until the next emotion marker (whether that's 1 line away or 100 lines away).

Square brackets denote the "topic" of a line. These are integrated into spoken lines, so they should be spoken in the audio file, too. If a line doesn't have any square brackets, this program will assume the entire line is the "topic". In the below example, "tarantula" is spoken and it's the topic. "Explain" is not spoken.
```
<explain> Despite bring over 3 inches in length, the [tarantula] is not large enough to have a measurable gravitational pull on the Sun.
```
Square brackets are not necessary, and including them or not doesn't affect the timing of the video at all. The only purpose they have is for drawing billboards. When you draw the billboard for the above line, it will be called "tarantula.png", and there will be a subtitle under the image that says "Tarantula". This is useful because if there is a another line 5 minutes later that also uses the word "tarantula", you can indicate that [tarantula] is again the topic, so you can reuse the same billboard image. If you don't care too much about the billboards, you can ignore including any square brackets at all.

Single line breaks indicate a change in pose without the emotion changing. There are 5 poses within each emotion category (e.g., 5 angry poses), so it's posibble to see the stick figure move his limbs around while still saying the same emotion. If you enable billboards, single line breaks also indiciate a billboard change.

Double line breaks change the background image and flip the entire screen (so if the stick figure was on the left side of the screen, now he's on the right). This is to make the video feel like it's distinctly in a "new section" of discussion. However, double line breaks are never necessary.

## Creating an actual lazykh video
I've provided one example project in this repo for you to test: it's called "exampleVideo". For this example project, the audio file is "exampleVideo/ev.wav", and the annotated script file is "exampleVideo/ev.txt". These should be placed in lazykh folder, so the addresses are "lazykh/exampleVideo/ev.wav" and "lazykh/exampleVideo/ev.txt"

### Step 1 - Remove the annotations from the script to make it "gentle-friendly" (Runtime: instant)
Open a command prompt, go to the lazykh folder, and run this command. This will create ev_g.txt
```
python3 code/gentleScriptWriter.py --input_file exampleVideo/ev
```

### Step 2 - Calculate phoneme timestamps with 'gentle'. (Runtime: 2 minutes for a 5-min video)
Run this command, which will create ev.json.
```
python3 gentle-final/align.py exampleVideo/ev.wav exampleVideo/ev_g.txt -o exampleVideo/ev.json
```

### Step 3 - Create a simplified timetable (Runtime: 2 seconds for a 5-min video)
Run this command, which will create ev_schedule.json. (This is not my code, it's solely Gentle.)
```
python3 code/scheduler.py --input_file exampleVideo/ev
```

### Step 4 - Render the frames (Runtime: 12 minutes for a 5-min video)
Run this command, which will create thousands of image files. (30 images per second of final video)
```
python3 code/videoDrawer.py --input_file exampleVideo/ev --use_billboards F --jiggly_transitions F
```

### Step 5 - Convert the image sequence to a video and add audio (Runtime: 8 minutes for a 5-min video)
Run this command, which will create the video file and delete all the image files.
```
python3 code/videoFinisher.py --input_file exampleVideo/ev --keep_frames F
```

If you want to start working on more video projects with different filepaaths, replace "exampleVideo/ev" with the new video's filepath in all the commands above before running them. It should work for your new videos.


## Alternate settings (adding billboards)
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
