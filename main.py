import arthur
import plugin
import gq
import speech

from datetime import datetime

def main():
	a = arthur.Arthur()

	a.input("good morning, arthur")	
	# speech.say(a.greet())

	# gq_plugin = plugin.plugin("GQ OOTD", 
	# 						  gq.ootd, 
	# 						  "What does GQ think I should wear today?",
	# 						  params=(datetime.now().month, datetime.now().year) )
	
	# a.add_plugin(gq_plugin)

	# speech.say(a.get_plugin("GQ OOTD").run())

if __name__ == "__main__":
    main()