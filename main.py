import os

import pandas as pd
from args_init import parser
from data_handling import get_unique_names
from utils import validate_and_convert_int, display_error_and_exit, display_progress

INTERACTIVE_MODE_EXIT_COMMAND = "-exit"


args = parser.parse_args()
input_file_name = args.filename
if not os.path.isfile(input_file_name):
    display_error_and_exit("Input file does not exist")

df = pd.read_csv(input_file_name, sep="\t")

ALL_TEAMS = get_unique_names(df=df, column_name="Team")
ALL_NOCS = get_unique_names(df=df, column_name="NOC")

output_file_name = None
if args.__contains__("output"):
    output_file_name = args.output
if args.medals is not None:
    if len(args.medals) < 2:
        display_error_and_exit("Medals lacks arguments! Aborting")

    received_team_code = ""
    received_year = None

    for arg in args.medals:
        received_year = validate_and_convert_int(arg)
        if received_year is None:
            received_team_code += str(arg) + " "
        else:
            received_year = received_year
            break

    received_team_code = received_team_code.lstrip().rstrip()

    if received_team_code is None or received_team_code == "":
        display_error_and_exit("Team argument is empty! Aborting")
    if received_year is None:
        display_error_and_exit("Year argument is not a valid int. Aborting")

    display_progress("Loaded year: " + str(received_year))

    found_NOC = None
    for NOC in ALL_NOCS:
        if received_team_code == NOC:
            found_NOC = NOC
            break

    found_team = None
    for TEAM_CODE in ALL_TEAMS:
        if received_team_code == TEAM_CODE:
            found_team = TEAM_CODE
            break

    if found_NOC is None and found_team is None:
        display_error_and_exit("No NOC or team found! Aborting")

    if found_team is None:
        display_progress("Loaded NOC: " + found_NOC)
    else:
        display_progress("Loaded team: " + found_team)

    # TODO print data

    if output_file_name is not None:
        with open(output_file_name, "w") as output_file:
            output_file.write("saf +\n + hello saf! \n !!!")
            display_progress("Writing output to file")

elif args.total is not None:
    year = args.total
    year = validate_and_convert_int(year)
    if year is None:
        display_error_and_exit("Year argument is not a valid int. Aborting")
    print(year)
    # TODO print data
elif args.overall is not None:
    received_teams = args.overall
    found_NOCs = []
    found_teams = []
    for team in received_teams:
        for NOC in ALL_NOCS:
            if team == NOC:
                found_NOCs.append(NOC)
    received_teams = list((x for x in received_teams if x not in found_NOCs))

    while len(received_teams) > 0:
        for TEAM_CODE in ALL_TEAMS:
            for i in range(0,7):
                new_value = ' '.join(received_teams[0:i]).lstrip().rstrip()

                if new_value == TEAM_CODE.lstrip().rstrip():
                    found_teams.append(TEAM_CODE)
                    for j in range(len(received_teams)):
                        del received_teams[0]
                    break
            else:
                continue
            break
        else:
            del received_teams[0]
        break

    display_progress("Loaded NOCs: " + str(found_NOCs))
    display_progress("Loaded teams: " + str(found_teams))

    # TODO print data

elif args.interactive is not None:
    display_progress("Interactive mode entered")
    while True:
        user_input = input("Enter team: ")
        found_NOC = None
        found_team = None

        if user_input == INTERACTIVE_MODE_EXIT_COMMAND:
            exit()

        for NOC in ALL_NOCS:
            if user_input == NOC:
                found_NOC = NOC
                break

        for TEAM_CODE in ALL_TEAMS:
            if user_input == TEAM_CODE:
                found_team = TEAM_CODE
                break

        if found_NOC is None and found_team is None:
            print("[ERROR]: No NOC or team found!")
            continue

        if found_team is None:
            display_progress("Loaded NOC: " + found_NOC)
        else:
            display_progress("Loaded team: " + found_team)
        # TODO print data