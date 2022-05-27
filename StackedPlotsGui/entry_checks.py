def station_code_entry_check(self):

    if len(self.station_edit.get_entry()) <= 1:
        print("Failed statio code entry check")
        self.warning_message_dialog("Error invalid station code, needs to be 2 uppercase characters")

    # If it passed check return True
    return True

def year_day_entry_check(self):

    if (len(self.year_day_edit.get_entry()) == 0):
        self.warning_message_dialog("There was no input for the year day entry box")

    # If it passed check return True
    return True

def hour_entry_check(self, hour_entry, end_or_start):

    hour = int(hour_entry)

    if hour > 24 or hour < 0:
        self.warning_message_dialog(
            "Hour Entry Error. Valid input (0 - 23)")

    else:
        return hour

    if end_or_start:
        self.start_hour_edit.set_entry(0)
        return 0
    else:
        self.end_hour_edit.set_entry(24)
        return 24

def minute_entry_check(self, minute_entry, end_or_start):

    minute = int(minute_entry)

    if minute > 59 or minute < 0:
        self.warning_message_dialog(
            "Minute Entry Error. Valid input (0 - 59)")
    else:
        return minute

    if end_or_start:
        self.start_minute_edit.set_entry(0)
        return 0
    else:
        self.end_minute_edit.set_entry(59)
        return 59

def second_entry_check(self, second_entry, end_or_start):

    second = int(second_entry)

    if second > 59 or second < 0:
        self.warning_message_dialog(
            "Second Entry Error. Valid input (0- 59)")

    else:
        return second

    if end_or_start:
        self.start_second_edit.set_entry(0)
        return 0
    else:
        self.end_second_edit.set_entry(59)
        return 59

