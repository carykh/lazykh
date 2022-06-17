import scipy.io.wavfile
import math
import numpy as np

AUDIO_FILE_LOCATION = "your_file"
MUSIC_FILE_LOCATION = "your_file"
OUTPUT_FILE_LOCATION = "your_file"
musicMulti = 0.044  # What percentage of the voice audio should the music audio be? Here, the music is 4.4% as loud as the speaker.

rate, voiceDataPre = scipy.io.wavfile.read(AUDIO_FILE_LOCATION)
rate, musicDataPre = scipy.io.wavfile.read(MUSIC_FILE_LOCATION)

voiceData = np.array(voiceDataPre)
musicData = np.array(musicDataPre)[:,0]

VOICE_LEN = voiceData.shape[0]
MUSIC_LEN = musicData.shape[0]
addedMusicData = np.zeros(voiceData.shape)
for ind in range(0,VOICE_LEN,MUSIC_LEN):
    if ind+MUSIC_LEN >= VOICE_LEN:
        addedMusicData[ind:VOICE_LEN] = voiceData[ind:VOICE_LEN]+musicData[0:VOICE_LEN-ind]*musicMulti
    else:
        addedMusicData[ind:ind+MUSIC_LEN] = voiceData[ind:ind+MUSIC_LEN]+musicData*musicMulti

addedMusicData = 32768*addedMusicData/np.amax(addedMusicData) # multiply by 2^32 because audio files just are that way sometimes
finishedData = np.asarray(addedMusicData, dtype=np.int16)
scipy.io.wavfile.write(OUTPUT_FILE_LOCATION,rate,finishedData)
