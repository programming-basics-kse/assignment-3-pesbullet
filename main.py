import os

import pandas as pd
from args_init import parser
from config import INTERACTIVE_MODE_EXIT_COMMAND, MAX_COMMAND_WORD_SIZE
from data_handling import get_unique_names, get_medals_by_team_and_year, get_total_by_year, get_teams_overall, \
    get_stat_by_team, get_stat_by_age_and_sex
from utils import validate_and_convert_int, display_error_and_exit, display_progress, display_warning

args = parser.parse_args()
input_file_name = args.filename
if not os.path.isfile(input_file_name):
    display_error_and_exit("Input file does not exist")

df = pd.read_csv(input_file_name)

ALL_TEAMS = get_unique_names(df=df, column_name="Team")
ALL_NOCS = get_unique_names(df=df, column_name="NOC")

loaded_data = ""

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
    elif found_team is not None:
        display_progress("Loaded team: " + found_team)
    else:
        display_progress("Loaded NOC: " + found_NOC)

    for element in get_medals_by_team_and_year(df=df, year=received_year, noc=found_NOC, team=found_team):
        print(element)
        loaded_data += str(element) + "\n"

elif args.total is not None:
    year = args.total
    year = validate_and_convert_int(year)
    if year is None:
        display_error_and_exit("Year argument is not a valid int. Aborting")
    print("Received year: " + str(year))

    for element in get_total_by_year(df=df, year=year):
        print(element)
        loaded_data += str(element) + "\n"

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
            for i in range(0, MAX_COMMAND_WORD_SIZE):
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
    if len(found_teams) > 1:
        display_warning("Sorry NOC are not supported")

    for element in get_teams_overall(df=df, teams=tuple(found_teams)):
        print(element)
        loaded_data += str(element) + "\n"

elif args.interactive:
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
        elif found_team is not None:
            display_progress("Loaded team: " + found_team)
        else:
            display_progress("Loaded NOC: " + found_NOC)

        for element in get_stat_by_team(df=df, noc=found_NOC, team=found_team):
            print(element)
            loaded_data += str(element) + "\n"

elif args.champions is not None:

    gender, min_age, max_age = args.champions

    if gender.upper() != "F" and gender.upper() != "M":
        display_error_and_exit("Gender must be M or F. So old-fashioned script...")
    is_male = True if gender.upper() == "M" else False

    try:
        min_age, max_age = sorted([int(min_age), int(max_age)])
    except ValueError:
        display_error_and_exit("Min and max age must be whole numbers")

    for element in get_stat_by_age_and_sex(df=df, is_male=is_male, min_age=min_age, max_age=max_age):
        print(element)
        loaded_data += str(element) + "\n"


if args.output is not None:
    with open(str(args.output), "w") as output_file:
        output_file.write(loaded_data)
        display_progress("Writing output to file")
