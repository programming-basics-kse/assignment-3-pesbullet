import pandas as pd

from data_handling import get_unique_names

df = pd.read_csv("source.tsv", sep="\t")

teams = get_unique_names(df=df, column_name="Team")
nocs = get_unique_names(df=df, column_name="NOC")
