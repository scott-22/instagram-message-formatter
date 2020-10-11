#Sicheng Hao

from json import load
from io import *
from EMOJI_REPLACE import EMOJI_REPLACE

#USERNAME AND TARGET USERS
USERNAME = "filler1"
TARGET = set([USERNAME, "filler2"])

#MONTHS
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

#NUMBER OF DAYS IN EACH MONTHS
MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
MONTH_DAYS_LEAP = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

#TIME ZONE EXPRESSED AS DIFFERENCE FROM UTC
TIME_ZONE = -4

def process(message, outStream, last):

    if message["sender"] != last:
        outStream.write("</div>\n<div class=\""+ str(message["sender"] == USERNAME) + "\">\n<h2>" + message["sender"] + ":</h2>\n")

    for i in ["media", "media_share_url"]:
        if i in message:
            outStream.write("<img src=\"" + message[i] + "\" width=\"200\" /><br />\n")

    for i in ["text", "story_share"]:
        if i in message and message[i]:
            outStream.write("<p class=\"text\">")
            out = message[i]
            for j in EMOJI_REPLACE:
                if j in out:
                    out = out.replace(j, EMOJI_REPLACE[j])
            outStream.write(out + "</p>")

    outStream.write("<p class=\"date\">")
    if "created_at" in message:
        outStream.write(formatDate(message["created_at"]))
    else:
        outStream.write(formatDate(message["date"]))
    outStream.write("</p>\n")

    return message["sender"]

def formatDate(date):
    global MONTHS, TIME_ZONE
    out = ""
    dayChange = 0

    hour = int(date[11:13]) + TIME_ZONE
    if hour < 0:
        hour += 24
        dayChange = -1
    elif hour >= 24:
        hour -= 24
        dayChange = 1
    if hour % 12 == 0:
        out += "12"
    else:
        out += str(hour % 12)
    out += date[13:16]
    if hour // 12 == 1:
        out += " PM"
    else:
        out += " AM"

    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10]) + dayChange
    year, month, day = changeDate(year, month, day)
    out = str(year) + "-" + str(MONTHS[month-1]) + "-" + str(day) + ", " + out

    return out

def changeDate(y, m, d):
    if d > monthDay(y, m):
        y, m = changeMonth(y, m+1)
        d = 1
    elif d < 1:
        y, m = changeMonth(y, m-1)
        d = monthDay(y, m)
    return y, m, d

def changeMonth(y, m):
    if m > 12:
        m = 1
        y += 1
    elif m < 1:
        m = 12
        y -= 1
    return y, m

def monthDay(y, m):
    global MONTH_DAYS, MONTH_DAYS_LEAP
    if m != 2:
        return MONTH_DAYS[m-1]
    if (y % 400 == 0) or (y % 100 != 0 and y % 4 == 0):
        return MONTH_DAYS_LEAP[1]
    else:
        return MONTH_DAYS[1]

with open("messages.json") as readChats, open("messages.html", 'w') as writeChats:
    chats = load(readChats)

    writeChats.write("<!DOCTYPE html>\n<html>\n<head><title>Instagram Chats</title>\n")
    writeChats.write("<link href=\"messages.css\" type=\"text/css\" rel=\"stylesheet\" /></head>")
    writeChats.write("<body>\n<div>\n<h1>Messages between " + ", ".join(TARGET) + "</h1>\n")

    last = ""
    for chat in reversed(chats):
        if not set(chat["participants"]) == TARGET:
            continue
        for message in reversed(chat["conversation"]):
            last = process(message, writeChats, last)

    writeChats.write("</div>\n</body>\n</html>\n")
