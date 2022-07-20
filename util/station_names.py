#
# station_names.py
#
# Contains functions for converting the various abbreviations and names
# of MACCS stations.

names = (
    # MACCS test locations
    ( "AU", "AUG", "AUGS", "Augsburg College",  "Augsburg College, Minnesota, USA"),
    ( "BU", "BOS", "BOST", "Boston University", "Boston University, Boston, USA"),
    # MACCS stations
    ( "CD", "CDR", "CDOR", "Cape Dorset",       "Cape Dorset, Nunavut, Canada"),
    ( "CH", "CHB", "CHAR", "Coral Harbour",     "Coral Harbour, Nunavut, Canada"),
    ( "CY", "CRV", "CYRV", "Clyde River",       "Clyde River, Nunavut, Canada"),
    ( "GH", "GJO", "GHAV", "Gjoa Haven",        "Gjoa Haven, Nunavut, Canada"),
    ( "IG", "IGL", "IGLK", "Igloolik",          "Igloolik, Nunavut, Canada"),
    ( "NA", "NAN", "NAIN", "Nain",              "Nain, Labrador, Canada"),
    ( "PB", "PEB", "PBAY", "Pelly Bay",         "Pelly Bay, Nunavut, Canada"),
    ( "PG", "PGG", "PGTG", "Pangnirtung",       "Pangnirtung, Nunavut, Canada"),
    ( "RB", "RBY", "RBAY", "Repulse Bay",       "Repulse Bay, Nunavut, Canada"),
    # Search Coil locations
    ( "MC", "MCM", "MCM-", "McMurdo",           "McMurdo Sound, Antarctica"),
    ( "SP", "SPA", "SPA-", "South Pole",        "South Pole, Antarctica"),
    ( "IQ", "IQA", "IQA-", "Iqaluit",           "Iqaluit, Nunavut, Canada"),
    ( "SS", "SDY", "SDY-", "Sondrestrom",       "Sondrestrom, Greenland"),
    ( "HB", "HAL", "HAL-", "Halley Bay",        "Halley Bay, Antarctica"))

def find_three_letter_name( a_name) :
    """
    Finds the three letter name of a station given a two to four letter name.

    Parameters
    ----------
    a_name :
        A two, three, or four letter station name.

    Returns
    -------
    string
        The three letter name of the given station or the empty string if not found.
    """

    a_name = a_name.upper() # change the input to all upper case
    column_index = 0        # assume the input is a two letter abbreviation
    if len( a_name) == 3 :
        column_index = 1    # the input string is a three letter abbreviation
    elif len( a_name) == 4 :
        column_index = 2
    row_index = -1          # start with an illegal row number
    for row in range(16) :  # 0 to 15, the row numbers of names array.
        if names[row][column_index] == a_name :
            row_index = row
            break
    if row_index < 0 :      # did not find a match
        return ""           # FIXME: return nil?
    else :
        return names[row_index][1]  # 1 is the column of the three letter abbr.

def find_full_name( a_name) :
    """
    Finds the full name of a station given the two, three, or four letter name.

    Parameters
    ----------
    a_name:
        A two, three, or four letter station name.

    Returns
    -------
    string
        The full name of the given station or an empty string if not found.
    """
    a_name = a_name.upper() # change the input to all upper case
    column_index = 0        # assume the input is a two letter abbreviation
    if len( a_name) == 3 :
        column_index = 1    # the input string is a three letter abbreviation
    elif len( a_name) == 4 :
        column_index = 2
    row_index = -1          # start with an illegal row number
    for row in range(16) :  # 0 to 15, the row numbers of names array.
        if names[row][column_index] == a_name :
            row_index = row
            break
    if row_index < 0 :      # did not find a match
        return ""           # FIXME: return nil?
    else :
        return names[row_index][3]  # 3 is the column of the full station name.
