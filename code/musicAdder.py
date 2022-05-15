import scipy.io.wavfile
import math
import numpy as np

musicMulti = 0.044

rate, voiceDataPre = scipy.io.wavfile.read("tc/tcv.wav")
rate, musicDataPre = scipy.io.wavfile.read("tc/BODYSURFER.wav")
print("Rate: "+str(rate))

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


addedMusicData = 32768*addedMusicData/np.amax(addedMusicData)

finishedData = np.asarray(addedMusicData, dtype=np.int16)
scipy.io.wavfile.write("tc/tcv_m.wav",rate,finishedData)


"""musicMulti = 0.05

rate, voiceDataPre = scipy.io.wavfile.read("slazykh/slazykh.wav")
rate, musicDataPre = scipy.io.wavfile.read("slazykh/Fig Leaf Times Two.wav")
print("Rate: "+str(rate))

voiceData = np.array(voiceDataPre)
musicData = np.array(musicDataPre)[:,0]

VOICE_LEN = voiceData.shape[0]
MUSIC_LEN = musicData.shape[0]
addedMusicData = np.zeros(voiceData.shape)
for ind in range(0,VOICE_LEN,MUSIC_LEN):
    if ind+MUSIC_LEN >= VOICE_LEN:
        addedMusicData[ind:VOICE_LEN] = voiceData[ind:VOICE_LEN]+musicData[0:VOICE_LEN-ind]*musicMulti
    else:
        mask = np.zeros(musicData.shape)
        for indy in range(0,MUSIC_LEN):
            v = abs(indy-44100*60*2)/44100
            truncatedV = min(max(v-7,0),1)
            mask[indy] = truncatedV
        addedMusicData[ind:ind+MUSIC_LEN] = voiceData[ind:ind+MUSIC_LEN]+musicData*musicMulti*mask


addedMusicData = 32768*addedMusicData/np.amax(addedMusicData)

finishedData = np.asarray(addedMusicData, dtype=np.int16)
scipy.io.wavfile.write("slazykh/slazykh_m.wav",rate,finishedData)"""
