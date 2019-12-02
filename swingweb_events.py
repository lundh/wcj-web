import urllib.request
import xml.etree.ElementTree as ET
import json
import argparse

parser = argparse.ArgumentParser(description='Where to store the json')
parser.add_argument("-o")

args = parser.parse_args()

# url='https://dans.se/xml/?type=events&org=wcj&pw='
# event_response = urllib.request.urlopen(url)
# events = event_response.read()

#tree = ET.fromstring(events)
tree = ET.parse('../events.xml')
root = tree.getroot()

# print root.tag

# Build a yaml file with events

events = list()
for child in root:
    if child.tag == "events":
        for event in child: # loop through all public events
            event_data = {}
            for event_details in event: # extract details about the event
                if event_details.tag == "title":
                    event_data["title"] = event_details.text
                elif event_details.tag == "source":
                    event_data["source"] = event_details.text
                elif event_details.tag == "primaryEventGroup":
                    event_data["category"] = event_details.text
                    event_data["category_id"] = event_details.attrib['itemId']
                elif event_details.tag == "category":
                    event_data["kind"] = event_details.text

            if any(event_data):
                if "category_id" not in event_data:
                    event_data["category_id"] = 9999
                    event_data["category"] = "Övrigt"
                events.append(event_data)

events_json = json.dumps(events, sort_keys=True, indent=4)

f = open(args.o, "w")
f.write(events_json)
f.close()

