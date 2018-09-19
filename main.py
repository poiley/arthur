import arthur
import plugin
import gq

def main():
	# import pdb; pdb.set_trace()
	a = arthur.Arthur()

	gq_plugin = plugin.plugin("GQ OOTD", 
							  gq.ootd, 
							  "What does GQ think I should wear today?",
							  params=(int(9), int(2018)) )
	print(gq_plugin.run())


if __name__ == "__main__":
    main()