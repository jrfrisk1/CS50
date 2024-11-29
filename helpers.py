from datetime import datetime


def userToDbDate(date_str):
    date_obj = datetime.strptime(date_str, "%m-%d-%Y")
    return date_obj.strftime("%Y-%m-%d")

def userToDbTime(time_str):
    time_obj = datetime.strptime(time_str, "%I:%M %p")
    return time_obj.strftime("%H:%M")

def convert_to_ampm(time_str):
    return datetime.strptime(time_str, "%H:%M").strftime("%I:%M %p")

def dbToUserDate(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%m/%d/%y")