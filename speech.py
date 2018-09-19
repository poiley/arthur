import vlc, time
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1

USERNAME=""
PASSWORD=""
VOICE = "en-US_AllisonVoice" # "en-GB_KateVoice", "en-US_MichaelVoice", "en-US_AllisonVoice"

service = TextToSpeechV1(username=USERNAME, password=PASSWORD)

def say(message):
	print(message)
	with open(join(dirname(__file__), "voice/response.mp3"), "wb") as f:
		response = service.synthesize(message, accept="audio/mp3", voice=VOICE).get_result()
		f.write(response.content)

	play("./voice/response.mp3")

def play(file_path):
	p = vlc.MediaPlayer(file_path)
	p.play()
	
	while p.get_state() != vlc.State.Ended:
		time.sleep(1)
	