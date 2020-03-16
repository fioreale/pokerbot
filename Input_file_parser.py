# 1 reading the input file from txt to a raw

import re

# set up regular expressions
# use https://regexper.com to visualise these if required
import game_model

rx_dict = {
    'action_node': re.compile(r'node /(?P<chance1>C.*?)(?P<history1>/.*?)?(/(?P<chance2>(C.*?))(?P<history2>(/.*?)))? (?P<player>.*( )?.*?) actions (?P<actions>.*)'),
    'chance_node': re.compile(r'node /(?P<chance1>C.*?)(?P<history1>/.*?)(/(?P<chance2>(C.*?))(?P<history2>(/.*?)))? chance actions (?P<actions>.*)'),
    'leaf_node': re.compile(r'node /(?P<chance1>C.*?)(?P<history1>/.*?)(/(?P<chance2>(C.*?))(?P<history2>(/.*?)))? leaf payoffs (?P<payoffs>.*)'),
    'root_node': re.compile(r'node / chance actions (?P<actions>.*)'),
    'infoset': re.compile(r'infoset (?P<history>.*?) nodes (?P<nodes>.*)'),
}


def parse_line(line):
    """
    Do a regex search against all defined regexes and
    return the key and match result of the first matching regex

    """

    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None


def parse_file(filepath):
    """
    Parse text at given filepath

    Parameters
    ----------
    filepath : str
        Filepath for file_object to be parsed

    Returns
    -------
    data : pd.DataFrame
        Parsed data

    """

    data = []  # create an empty list to collect the data
    # open the file and read through it line by line
    with open(filepath, 'r') as file_object:
        line = file_object.readline()
        while line:
            # at each line check for a match with a regex
            key, match = parse_line(line)

            # extract school name
            if key == 'root_node':
                actions = match.group('actions')
                root = game_model.Node.setRoot(actions)



            if key == 'history_node':
                chance1 = match.group('chance1')
                history1 = match.group('history1')
                chance2 = match.group('chance2')
                history2 = match.group('history2')
                player = match.group('player')
                actions = match.group('arguments')

            if key == 'chance_node':

            if key == 'leaf_node':

            # if key == 'infoset':
            #     history = match.group('history')
            #     arguments = match.group('arguments')



            # # identify a table header
            # if key == 'name_score':
            #     # extract type of table, i.e., Name or Score
            #     value_type = match.group('name_score')
            #     line = file_object.readline()
            #     # read each line of the table until a blank line
            #     while line.strip():
            #         # extract number and value
            #         number, value = line.strip().split(',')
            #         value = value.strip()
            #         # create a dictionary containing this row of data
            #         row = {
            #             'School': school,
            #             'Grade': grade,
            #             'Student number': number,
            #             value_type: value
            #         }
            #         # append the dictionary to the data list
            #         data.append(row)
            #         line = file_object.readline()

            line = file_object.readline()

        # create a pandas DataFrame from the list of dicts
        data = pd.DataFrame(data)
        # set the School, Grade, and Student number as the index
        data.set_index(['School', 'Grade', 'Student number'], inplace=True)
        # consolidate df to remove nans
        data = data.groupby(level=data.index.names).first()
        # upgrade Score from float to integer
        data = data.apply(pd.to_numeric, errors='ignore')
    return data


if __name__ == '__main__':
    key, match = parse_line('node /C:JQ player 1 actions c r')
    print(key)
    print(match)
    print(match.group('history'))
    key, match = parse_line('infoset /C:J?/P1:c/P2:r nodes /C:JQ/P1:c/P2:r /C:JK/P1:c/P2:r')
    print(key)
    print(match)
    key, match = parse_line('infoset /C:J? nodes /C:JQ /C:JK')
    print(key)
    print(match)