import arthur
import plugin

def main():
	# import pdb; pdb.set_trace()
	a = arthur.Arthur()

	gq_plugin = plugin.plugin("GQ OOTD", 
							  gq_ootd, 
							  "What does GQ think I should wear today?",
							  params=(int(9), int(2018)) )
	gq_plugin.run()

#will scrape from sites like this: https://www.gq.com/gallery/what-to-wear-today-september
#break it down into a json file, reference the file each day of the month.
def gq_ootd(month, year):
	print("Hello world")
	#pseudocode
	# if month < current month
	# 	return error
	# if year < 2017
	# 	return error

if __name__ == "__main__":
    main()