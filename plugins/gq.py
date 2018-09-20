import requests, json
from lxml import html
from datetime import datetime

DATA_PATH = "plugins/ootd.json"
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

"""
	Return what GQ reccomends wearing today.
	For reference, see https://www.gq.com/gallery/what-to-wear-september
"""
def ootd(month, year):
	date_formatted = str(month) + "/" + str(year)[2:]
	now = datetime.now()
	
	if month < now.month or year < now.year:
		return ""

	with open(DATA_PATH, "r") as f:
		file_data = json.load(f)
	
	if date_formatted in file_data.keys():
		ootd_data = file_data[date_formatted]
	else:
		ootd_data = _write_data(date_formatted, _get_gq_ootd_data(month, year))
	
	return "GQ suggests " + ootd_data[str(now.day)]

"""
	If data isn't already scraped from GQ, write the scraped data to 
	file for future reference.
"""
def _write_data(date_formatted, ootd_data):
	formatted_data = {}
	for i in range(0, len(ootd_data)):
		formatted_data[str(i+1)] = ootd_data[i]

	with open(DATA_PATH) as f:
		data = json.load(f)
		data[date_formatted] = formatted_data

	with open(DATA_PATH, "w") as f:
		json.dump(data, f)

	return data[date_formatted]

"""
	Scrape GQ site for the months worth of style tips.
"""
def _get_gq_ootd_data(month, year):
	url = _get_ootd_url(month, year)
	
	if not url: # If invalid URL for current month, break
		return [""]

	site = requests.get(url)
	html_data = html.fromstring(site.content)

	return html_data.xpath('//div[@class="vertical-gallery-item__dek"]/text()')

"""
	Get the URL of the GQ style reccomendations.
	Certain dates have different URLs, so there's a series of checks invovled.
"""
def _get_ootd_url(month, year):
	url = "https://www.gq.com/gallery/what-to-wear-today-{}".format(MONTHS[month-1])
	
	if _check_status_code(url) or _check_status_code("{}-{}".format(url, year)):
		return url
	
	return ""

"""
	Ensure given URL is accessible
"""
def _check_status_code(url):
	page = requests.get(url)

	if page.status_code == 200:
		return True

	return False