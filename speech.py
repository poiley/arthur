import vlc, time, json, re
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1
import speech_recognition as sr

with open("keys.json") as f:
	data = json.loads(f.read())

stt_USERNAME=data["stt_username"]
stt_PASSWORD=data["stt_password"]

tts_USERNAME=data["tts_username"]
tts_PASSWORD=data["tts_password"]
VOICE = data['voice']

service = TextToSpeechV1(username=tts_USERNAME, password=tts_PASSWORD)

def say(message):
	print(message)
	
	if message == "__REPEAT__":
		play("./voice/response.mp3")
		return
	elif message == "__INVALID__":
		play("./voice/invalid_input.mp3")
		return

	with open(join(dirname(__file__), "voice/response.mp3"), "wb") as f:
		response = service.synthesize(message, accept="audio/mp3", voice=VOICE).get_result()
		f.write(response.content)

	play("./voice/response.mp3")

def play(file_path):
	p = vlc.MediaPlayer(file_path)
	p.play()
	
	while p.get_state() != vlc.State.Ended:
		time.sleep(1)

def listen():
	r = sr.Recognizer()

	mic = sr.Microphone()
	with mic as src:
		print("Say something! ")
		audio = r.listen(src)

	return re.sub(r"[^\w\s]", "", r.recognize_ibm(audio, stt_USERNAME, stt_PASSWORD).strip().lower())
