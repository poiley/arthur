from datetime import datetime
import sys
sys.path.insert(0, "./plugins")

import plugin
import speech
import arthur

import gq

def main():
	a = arthur.Arthur()

	gq_plugin = plugin.plugin("GQ OOTD", 
							  gq.ootd, 
							  "What does GQ think I should wear today?",
							  params=(datetime.now().month, datetime.now().year))
	
	a.add_plugin(gq_plugin)

	speech.say("Hello, there I'm {}".format(a.name))

	_in = speech.listen()
	while _in != "quit":
		print("Arthur heard you say '{}'".format(_in))
		_in = a.input(_in)
	
		if _in:
			speech.say(_in)
		else:
			speech.say("__INVALID__")

		_in = speech.listen()


if __name__ == "__main__":
    main()