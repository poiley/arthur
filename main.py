import arthur
import plugin
import gq
import speech

from datetime import datetime

def main():
	a = arthur.Arthur()

	gq_plugin = plugin.plugin("GQ OOTD", 
						  gq.ootd, 
						  "What does GQ think I should wear today?",
						  params=(datetime.now().month, datetime.now().year) )
	
	a.add_plugin(gq_plugin)

	_in = ""
	while _in != "quit":
		_in = a.input(input("'quit' to quit.\n~> "))
		if _in:
			speech.say(_in)
		else:
			speech.say("__INVALID__")


if __name__ == "__main__":
    main()