import vlc, time, json
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1

with open("keys.json") as f:
	data = json.loads(f.read())

USERNAME=data['username']
PASSWORD=data['password']
VOICE = data['voice']

service = TextToSpeechV1(username=USERNAME, password=PASSWORD)

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
	