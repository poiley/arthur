import arthur
import plugin
import gq

from datetime import datetime

def main():
	a = arthur.Arthur()

	gq_plugin = plugin.plugin("GQ OOTD", 
							  gq.ootd, 
							  "What does GQ think I should wear today?",
							  params=(datetime.now().month, datetime.now().year) )
	
	a.add_plugin(gq_plugin)

	print("GQ recommends {}".format(a.get_plugin("GQ OOTD").run()))


if __name__ == "__main__":
    main()