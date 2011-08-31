#! /usr/bin/python
# groupon.py 

"""
	Small script to fetch groupon data and display the current offers in a neat GUI.
	11/8/31, Jan
"""

import urllib2
import os
from Tkinter import *

# global data store
grouponDataList = []

#
# classes
#

class GrouponDataItem:
    """data structure to store relevant data"""
	
    def __init__(self, city, url, cookieCode, content = "unknown"):
        self.city = city
        self.url = url
        self.cookieCode = cookieCode
        self.content = content
    def __repr__(self):
        return "city: %s, content: %s \n" % (self.city, self.content)

class GrouponGui:
    """tkinter-gui to display data"""
	
    def __init__(self, master):
        frame = Frame(master)
        frame.grid(padx=10, pady=10)
        
        #frame.grid_rowconfigure(0, weight=1)
        #frame.grid_columnconfigure(0, weight=1)
        #yscrollbar = Scrollbar(frame)
        #yscrollbar.grid(row=0, column=1, sticky=N+S)
        
        # scrollbar = Scrollbar(frame)
        # scrollbar.grid()
        # frame.config(yscrollcommand=scrollbar.set)
        # scrollbar.config(command=frame.yview)
        self.fill_table(frame)
        
    def fill_table(self, frame):
            for index, item in enumerate(grouponDataList):
                print index, item.city, item.content
                separator = Frame(frame, width=600, height=50, bd=1, relief=SUNKEN, padx=5, pady=5)
                separator.grid(columnspan=4)
                Label(separator, text = item.city, font="bold", width=15 ).grid(row = index, column=0)
                Label(separator, text = item.content, wraplength=400, width=50, anchor=W, justify=LEFT ).grid(row = index, column=1)
                Label(separator, text = "click", width=10).grid(row = index, column=2)
            			
def get_h1_from_html(html):
    """Extract headline from provided HTML string."""
    headline = 'cannot determine'
    if html.count("h1") == 2:
        headline = html[html.find("h1") + 3:html.rfind("h1") - 6]
        headline = headline.split(">")[1]
        headline = headline.replace("\n", " ")
        headline = headline.replace("\r", " ")
        headline = headline.replace("  ", " ")
    return headline

def get_content_from_url(url, cookieCode):
    """Fetches groupon data from provided URL, sends provided cookie."""
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    opener.addheaders.append(('Cookie', "__utma=151662447.1565834492.1313527685.1313988918.1314130979.5; __utmz=151662447.1313527685.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); user_locale=de_CH; city=" + cookieCode + "; _vis_opt_s=4%7C; CID=CH_DTI_0_0_0_0; BIGipServerwww.citydeal.ch_http=3592415242.33280.0000; _vis_opt_test_cookie=1; __utmb=151662447.6.10.1314130979; __utmc=15166244"))
    infile = opener.open(url)
    return get_h1_from_html(infile.read())

def fetch_data():
    """initalize global datastore"""
    global grouponDataList
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
                  "St.Gallen": ["http://www.groupon.ch/deals/stgallen", "st-gallen"], 
                  "Zuerich" : ["http://www.groupon.ch/deals/zuerich", "zuerich"]}
    for city,dataList in swissData.iteritems():
        grouponDataList.append(GrouponDataItem(city, dataList[0], dataList[1], get_content_from_url(dataList[0], dataList[1])))
    grouponDataList.sort(key=lambda item: item.city) 

def build_gui():
    """builds tkinter GUI."""
    root = Tk()
    app = GrouponGui(root)
    root.mainloop()

def main():
    """ Fetch data from various groupon cities, merge into data structure, display in GUI."""
    fetch_data()
    build_gui()
        
if __name__ == "__main__":
    main()