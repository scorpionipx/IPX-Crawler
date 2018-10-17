from gtts import gTTS
import subprocess
from time import sleep, strftime, gmtime
import platform
import logging
from pygame import mixer

LANGUAGE_LITERAL = 'ipx_lang:'

logger = logging.getLogger("ipx_logger")

mixer.init()


def speak(speech, language):
    audio_file = "crawler_voice_{}.mp3".format(strftime("%Y_%m_%d_%H_%M_%S", gmtime()))
    text_to_speech = gTTS(text=speech, lang=language)
    text_to_speech.save(audio_file)
    if platform.system() == 'Windows':
        os_cmd = audio_file
        os_cmd = os_cmd.split()
        cmd_output = (subprocess.run(os_cmd, stdout=subprocess.PIPE)).stdout.decode('utf-8)')
    elif platform.system() == 'Linux':
        # os_cmd = 'mpg321 ' + audio_file
        mixer.music.load(audio_file)
        mixer.music.play()
    else:
        os_cmd = audio_file




def speak_obsolete(speech, language):
    audio_file = "crawler_voice_{}.mp3".format(strftime("%Y_%m_%d_%H_%M_%S", gmtime()))
    if platform.system() == 'Windows':
        text_to_speech = gTTS(text=speech, lang=language)
        text_to_speech.save(audio_file)
        os_cmd = audio_file
    elif platform.system() == 'Linux':
        os_cmd = 'espeak ' + "\"" + speech + "\""

    # os_cmd = os_cmd.split()
    subprocess.call(os_cmd, shell=True)