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

	_in = input("'quit' to quit.\n~> ")
	while _in != "quit":
		_in = a.input(_in)
	
		if _in:
			speech.say(_in)
		else:
			speech.say("__INVALID__")

		_in = input("'quit' to quit.\n~> ")


if __name__ == "__main__":
    main()