#! /usr/bin/python
# groupon.py 

"""
	Small script to fetch groupon data and display the current offers in a neat GUI.
	11/8/31, Jan
"""

import urllib2
import cookielib
import os
import webbrowser
from Tkinter import *
from time import localtime, strftime

# global data lists
grouponDataList = []
swissData = { "Basel": ["http://www.groupon.ch/deals/basel", "basel"], 
			  "Bern" : ["http://www.groupon.ch/deals/bern", "bern"], 
			  "Biel" : ["http://www.groupon.ch/deals/biel", "biel"],
			  "Chur" : ["http://www.groupon.ch/deals/chur", "chur"],
			  "Freiburg" : ["http://www.groupon.ch/deals/freiburg", "freiburg"],
			  "Genf" : ["http://www.groupon.ch/deals/genf", "genf"],
			  "Groupon Travel" : ["http://www.groupon.ch/deals/groupon-travel", "groupon-travel"],
			  "Interlaken" : ["http://www.groupon.ch/deals/interlaken", "interlaken"],
			  "Koenitz" : ["http://www.groupon.ch/deals/koenitz", "koenitz"],
			  "La-Chaux-de-Fonds" : ["http://www.groupon.ch/deals/la-chaux-de-fonds", "la-chaux-de-fonds"],
			  "Lausanne" : ["http://www.groupon.ch/deals/lausanne", "lausanne"],
			  "Luzern" : ["http://www.groupon.ch/deals/luzern", "luzern"],
			  "Neuenburg" : ["http://www.groupon.ch/deals/neuenburg", "neuenburg"],
			  "Schaffhausen" : ["http://www.groupon.ch/deals/schaffhausen", "schaffhausen"],
			  "Sitten" : ["http://www.groupon.ch/deals/sitten", "sitten"],
			  "St.Gallen": ["http://www.groupon.ch/deals/stgallen", "st-gallen"], 
			  "Thun": ["http://www.groupon.ch/deals/thun", "thun"], 
			  "Uster": ["http://www.groupon.ch/deals/uster", "uster"], 
			  "Winterthur": ["http://www.groupon.ch/deals/winterthur", "winterthur"], 
			  "Vernier": ["http://www.groupon.ch/deals/vernier", "vernier"], 
			  "Zug": ["http://www.groupon.ch/deals/zug", "zug"], 
			  "Zuerich" : ["http://www.groupon.ch/deals/zuerich", "zuerich"],
			  "Zuerich Spezial" : ["http://www.groupon.ch/deals/zurich-spezial", "zurich-spezial"],
			  "National Deal" : ["http://www.groupon.ch/deals/zurich-spezial", "online-deal"]
			  }

#
# classes
#

class GrouponDataItem:
    """data structure to store relevant data"""
	
    def __init__(self, content, cities, urls):
        self.content = content
        self.cities = cities
        self.urls = urls
    def __repr__(self):
        return "cities: %s content: %s, \n" % (self.cities, self.content)

class GrouponGui:
    """tkinter-gui to display data"""

    def __init__(self, master):
        frame = Frame(master, width = 300)
        frame.pack(padx=10, pady=10, fill=BOTH, expand=YES)
        self.fill_table(frame)
        self.master = master

    def fill_table(self, frame):
		for index, item in enumerate(grouponDataList):
			separator = Frame(frame, bd=1, relief=SUNKEN, padx=5, pady=5)
			w = Text( separator, wrap='word', height=2, width=1 )
			w.insert( 1.0, item.content )
			w.configure( bg=separator.cget('bg'), relief='flat', state='disabled' )
			w.pack(fill=BOTH, expand=1)
			for index, city in enumerate(item.cities):
				Button(separator, text=city, command=lambda url = item.urls[index]: self.open_url(url)).pack(side=LEFT)
			separator.pack(fill=BOTH, expand=True)
		finish = Frame(frame, bd=1, padx=15, pady=15)
		Label(finish, text="fetch time: " + strftime("%a, %d %b %Y %H:%M:%S", localtime())).pack(side=LEFT)
		Button(finish, text="update now", command=self.refresh_gui).pack(side=RIGHT)
		finish.pack(fill=BOTH, expand=True)
            			
    def open_url(self, url):
    	webbrowser.open_new_tab(url)

    def refresh_gui(self):
		self.master.destroy()
		main()
        
def get_content_from_url(url, cookieCode, cookies):
    """Fetches groupon data from provided URL, sends provided cookie."""
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    opener.addheaders.append(('Cookie', cookies + "; city=" + cookieCode))
    infile = opener.open(url)
    html = infile.read()
    headline = 'cannot determine'
    if html.count("h1") == 2:
    	headline = html[html.find("h1") + 3:html.rfind("h1") - 6]
    	if headline.find(">") != -1: # if nested link
    	 	headline = headline.split(">")[1] 
    	headline = headline.replace("\n", " ")
    	headline = headline.replace("\r", " ")
    	headline = headline.replace("  ", " ")
    return headline

def append_or_merge_to_list(content, city, url):
	""" adds or merges content to existing dictonary"""
	global grouponDataList
	for item in grouponDataList:
		if item.content == content:
			item.cities.append(city)
			item.urls.append(url)
			break
	else:
		grouponDataList.append(GrouponDataItem(content, [city], [url]))

def fetch_data():
    """initalize global datastore"""
    global grouponDataList 
    grouponDataList = [] # needed for refresh
    cookies = read_cookies()
    for city,dataList in swissData.iteritems():
    	print "fetching %s ..." % city,
        append_or_merge_to_list(get_content_from_url(dataList[0], dataList[1], cookies), city, dataList[0])
        print " ok"
    grouponDataList.sort(key = lambda item: len(item.cities))

def build_gui():
    """builds tkinter GUI."""
    root = Tk()
    root.title("GDF - groupon data fetcher")
    app = GrouponGui(root)
    root.mainloop()

def read_cookies():
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	resp = opener.open('http://www.groupon.ch')
	result = ""
	for cookie in cj:
		result += cookie.name + "=" + cookie.value +"; "
	return result;

def main():
    """ Fetch data from various groupon cities, merge into data structure, display in GUI."""
    read_cookies()
    fetch_data()
    print grouponDataList
    # build_gui()
        
if __name__ == "__main__":
    main()