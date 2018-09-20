import json
import time
from threading import Thread
from datetime import datetime
from weather import Weather, Unit
import feedparser
import plugin
import speech
import re

class Arthur():
    def __init__(self):
        self.name, self.WOEID, self.todo, temp_name, temp_title, temp_url = self.read_traits_from_file()
        self.owner = User(temp_name, temp_title, news_url=temp_url)
        self.plugins = []

    """
        Receive user input, parse it and run as function.
        Returns function return if function run was a success, "" if failure.
    """
    def input(self, input_str):
        if " arthur" in input_str:
            input_str = input_str.replace(" arthur", "")
        elif  "arthur " in input_str:
            input_str = input_str.replace("arthur ", "")
        
        input_str = re.sub(r"[^\w\s]", "", input_str)

        with open("functions.json") as f:
            data = json.loads(f.read())

        func = {""}
        if input_str in data.keys():
            l = list(data.keys())
            for i in range(0, len(l)):
                if input_str == l[i]:
                    func = data[l[i]]
                    break

        if func != {""}:
            return eval("self."+func)

        return ""


    def standard_response(self, response):
        return response

    """
        Repeat what was just said
    """
    def repeat(self):
        return "__REPEAT__"

    """
    	A simple greeting that changes depending on the time of day.
    """
    def greet(self, full=False):
        now = datetime.now()
        if now.hour < 5 or now.hour >= 21:
            time_of_day = "night"
        elif now.hour < 12:
            time_of_day = "morning"
        elif now.hour < 17:
            time_of_day = "afternoon"
        else:
            time_of_day = "evening"

        if not full and not self.is_first_greeting_of_day():
            return "Good {day}, {fullname}.".format(day=time_of_day, fullname=self.owner.get_full_name())
        else:
            return self.greet_first_of_day("Good {}, {}.".format(time_of_day, self.owner.get_full_name()),
                    self.get_suggestions_based_off_weather(),
                    self.get_headlines(3) )
    
    """
        Wrapper function for speech input case. Forces full greeting.
    """
    def greet_full(self):
        return self.greet(full=True)

    """
    	Boolean function to check if user has been greeted with first message of the day.
    """
    def is_first_greeting_of_day(self):
    	data = ""
    	with open("static.json") as f:
    		data = json.loads(f.read())

    	if data:
    		d = datetime.strptime(data["Morning_Greeting"], "%m/%d/%y")

    		if datetime.now().day != d.day:
    			return True

    	return False

    """
    	More intricate greeting, combining information from multiple other functions
    	to compile a small daily report for user.
    """
    def greet_first_of_day(self, greeting, weather_suggestions, headlines):
        with open("static.json", "r+") as f:
            data = json.load(f)
            data["Morning_Greeting"] = datetime.now().strftime("%D")
            f.seek(0)
            json.dump(data, f)
            f.truncate()

        schedule = "Todays schedule calls for "
        if datetime.now().weekday() == 0:
            greeting += "It's Monday, which means a new Discover Weekly."
            schedule += "Discrete, CS 223, CS 260."
        elif datetime.now().weekday() == 2:
            schedule += "Discrete, CS 223, CS 260."
        elif datetime.now().weekday() == 1 or datetime.now().weekday() == 3:
            schedule += "a Physics and Linear Algebra lecture."
        elif datetime.now().weekday() == 4:
            s = greeting.split("Good")
            s[0] = "Happy Friday"
            greeting = "".join(s)

            greeting += "You have a refreshed Release Radar playlist ready for you Spotify."
            schedule += "Discrete, CS 223, CS 260."

        return greeting + " " + schedule + " " + weather_suggestions[1:] + " " + self.get_news_formatted()


    """
		Input is WOEID (Yahoo Weather API equiv. of Zip Code)
		It can be found/configured in `static.json`.
    """
    def get_weather(self):
    	lookup = Weather(unit=Unit.FAHRENHEIT).lookup(self.WOEID)
    	return "It is {} degrees and {} in {}, {}".format(lookup.condition.temp, lookup.condition.text, lookup.location.city, lookup.location.region)

    """
        Return some semi-casual conversation and advice based on weather.
    """
    def get_suggestions_based_off_weather(self):
    	lookup = Weather(unit=Unit.FAHRENHEIT).lookup(self.WOEID)

    	suggestion_temp = ""
    	if int(lookup.condition.temp) > 75:
    		suggestion_temp = "It looks like it's hot out. May I suggest some shorts and a tee?"
    	elif int(lookup.condition.temp) > 40:
    		suggestion_temp = "Seems to be a pretty normal day out. How about some regular jeans or a hoodie?"
    	elif int(lookup.condition.temp) > 32:
    		suggestion_temp = "It's a cold one out there! Layer up. Grab a coffee on your way out to warm you up."
    	else:
    		suggestion_temp = "My records are indicating below freezing temperatures. Cancel your plans, Winter is coming."

    	suggestion_weather = ""
    	if suggestion_temp != "":
    		if lookup.condition.code in range(26, 30):
    			suggestion_weather = "Reports are coming in that it's going to a be a bit cloudy."
    		elif lookup.condition.code in range(5,7) or lookup.condition.code in range(13, 16) or lookup.condition.code in range(41, 43) or lookup.condition.code == 46:
    			suggestion_weather = "Log into MyWazzu and check if classes are in session because it's going to be snowing soon!"
    		elif lookup.condition.code in range(8, 12) or lookup.condition.code in range(17, 18) or lookup.condition.code == 35 or lookup.condition.code in range(37, 40) or lookup.condition.code == 45 or lookup.condition.code == 47:
    			suggestion_weather = "Surprise, surprise! It's raining."
    		elif lookup.condition.code == 32 or lookup.condition.code == 36:
    			suggestion_weather = "Good morning sunshine! The Earth says hello!"
    	
    	return suggestion_weather + " " + suggestion_temp


    def get_news_formatted(self):
        headlines = self.get_headlines(3)
        headlines_listed = ""
        for i in range(0, len(headlines)):
            if i == (len(headlines) - 1):
                headlines_listed += " and \"" + headlines[i] + "\".."
            else:
                headlines_listed += "\"" + headlines[i] + "\","

        return "Today's headlines include " + headlines_listed[:-1] + "."
    
    """
    	Import RSS feed, return `number` headlines from top
    	Ex.: self.get_headlines("https://reddit.com/r/worldnews.rss", 3)
    """
    def get_headlines(self, number):
    	headlines = []
    	rss_data = feedparser.parse(self.owner.news_url)

   
    	for i in range(0, number):
    		try:
    			headlines.append(rss_data.entries[i]["title"])
    		except KeyError:
    			break
    	
    	return headlines

    """
    	File `static.json` must exist and contain such key values
    """
    def read_traits_from_file(self):
    	with open("static.json") as f:
    		data = json.loads(f.read())
    		return data["Traits"]["Name"], data["Traits"]["WOEID"], data["Todo"], data["Traits"]["Owner"], data["Traits"]["Owner_Title"], data["Traits"]["News_RSS_URL"]

    """
    	Times are formatted as "HH:MM:SS DD/MM/YY"
    	Ex.: self.set_alarm("04:10:00 09/18/18")
    """
    def set_alarm(self, alarm_time):
        d = datetime.strptime(alarm_time, "%H:%M:%S %m/%d/%y")
        alarm_epoch = float(time.mktime(d.timetuple()))
        current_epoch = float(time.mktime(datetime.now().timetuple()))
        
        a = Alarm(alarm_epoch - current_epoch)

        speech.play("voice/alarm.mp3")

    """
    	Add item to Todo list and write to disk
    """
    def add_todo(self, new):
        self.todo.append(new)
        self._update_todo_file()
        return "Added to to-do list." 

    """
    	Remove item from Todo list and write to disk
    """
    def remove_todo(self, rm):
        if rm in self.todo:
            self.todo.remove(rm)
            self._update_todo_file()
            return "Removed from to-do list." 
        return "Item not in list."

    """
    	Clear the Todo list and write to disk
    """
    def clear_todo(self):
        self.todo = []
        self._update_todo_file()
        return "To-do list cleared."

    """
    	Private function for accessing and writing to the todo file when changes
    	are made.
    """
    def _update_todo_file(self):
    	with open("static.json", "r+") as f:
    		data = json.load(f)
    		data["Todo"] = self.todo
    		f.seek(0)
    		json.dump(data, f)
    		f.truncate()

    """
        Return Todo list
    """
    def get_todo(self):
    	return self.todo

    """
        Add plugin object to Arthur
    """
    def add_plugin(self, plugin):
        self.plugins.append(plugin)

    """
        Return all plugins
    """
    def get_all_plugins(self):
        return self.plugins

    """
        Returns plugin, given plugin title matches query parameter
    """
    def get_plugin(self, plugin_title):
        for p in self.plugins:
            if p.get_title() == plugin_title:
                return p

    """
        Lists all plugins as text
    """
    def list_plugins(self):
        for p in self.plugins:
            print(p.get_title())

"""
	Alarm clock class, child of threading.Thread
"""
class Alarm(Thread):
	def __init__(self, alarm_duration):
		time.sleep(alarm_duration)
		
"""
	User class
	Stores data about the user
"""
class User():
    def __init__(self, name, title, news_url=None):
        self.name = name
        self.title = title
        if not news_url:
            news_url = "http://feeds.bbci.co.uk/news/world/rss.xml"
        self.news_url = news_url
        

    def get_name(self):
        return self.name

    def get_title(self):
        return self.title

    def get_full_name(self):
        return self.title + " " + self.name 

    def get_news_url(self):
        return self.news_url

    def set_name(self, new):
        self.name = new

    def set_title(self, new):
        self.title = new

    def set_url(self, new):
        self.news_url = new