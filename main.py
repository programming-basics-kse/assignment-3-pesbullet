import pandas as pd
import argparse

from args_init import parser
from data_handling import get_unique_names
from utils import validate_and_convert_int, display_warning, display_error_and_exit

df = pd.read_csv("source.tsv", sep="\t")

ALL_TEAMS = get_unique_names(df=df, column_name="Team")
ALL_NOCS = get_unique_names(df=df, column_name="NOC")

args = parser.parse_args()
output_file_name = args.filename
if args.medals is None:
    display_error_and_exit("Medals is None! Aborting")
else:
    if len(args.medals) < 2:
        display_error_and_exit("Medals lacks arguments! Aborting")
    if len(args.medals) > 2:
        display_warning("given more arguments than needed. Ignoring the rest")
    received_team_code = args.medals[0]
    if received_team_code is None or received_team_code == "":
        display_error_and_exit("Team argument is empty! Aborting")
    received_year = args.medals[1]
    received_year = validate_and_convert_int(received_year)
    if received_year is None:
        display_error_and_exit("Year argument is not a valid int. Aborting")



