from typing import Iterable

import pandas as pd
from pandas import DataFrame


def get_unique_names(df: DataFrame, column_name: str) -> list:
    return list(df[column_name].unique())


def get_medals_by_team_and_year(df: DataFrame, year: int, noc=None, team=None) -> Iterable:
    if noc is not None:
        filtered_df = df.loc[(df["NOC"] == noc) & (df["Year"] == year)]
    elif team is not None:
        filtered_df = df.loc[(df["Team"] == team) & (df["Year"] == year)]
    else:
        return ("I need a team name or NOC", )

    if len(filtered_df) == 0:
        return ("There wasn't such a team in that a year. Check you input pls",)

    result_df = filtered_df.loc[
        (df["Year"] == year) & (df["Medal"].notna()),
        ["Name", "Sport", "Medal"]
    ]
    if len(result_df) == 0:
        return ("This team haven't earned any medals that year",)

    bronze = len(result_df.loc[result_df["Medal"] == "Bronze"])
    silver = len(result_df.loc[result_df["Medal"] == "Silver"])
    gold = len(result_df.loc[result_df["Medal"] == "Gold"])

    up_to_ten_lines = result_df[:10]
    result_str = up_to_ten_lines.to_string(index=False)

    return result_str, f"{noc or team}-{year}: {bronze} bronze medals, {silver} silver medals, {gold} gold medals"


def get_total_by_year(df: DataFrame, year: int) -> Iterable:
    only_winners = df.loc[(df["Year"] == year) & (df["Medal"].notna())]

    if len(only_winners) == 0:
        return ("There wasn't Olympics in that year. Check you input pls", )

    medals = pd.get_dummies(
        only_winners, columns=["Medal"], dtype=int, prefix="", prefix_sep=""
    )
    medals = medals.loc[:, ["Team", "Bronze", "Silver", "Gold"]]
    result = medals.groupby(["Team"], as_index=False).sum()
    result = result.to_string(index=False)

    return (result, )


def get_teams_overall(df: DataFrame, teams: tuple) -> Iterable:
    df["Medal_digit"] = 0
    df.loc[df["Medal"].notna(), "Medal_digit"] = 1

    result_str_list = []
    for team in teams: 
        team_df = df.loc[df["Team"] == team, ["Year", "Medal_digit"]]
        result_df = team_df.groupby(["Year"], as_index=False).sum()
        best_medals_number = result_df["Medal_digit"].max()
        best_years = result_df[result_df["Medal_digit"] == best_medals_number]["Year"].to_string(index=False)
        result_str_list.append(f"{team} had best result in {best_years}: {best_medals_number} medals")

    return result_str_list


def get_stat_by_team(df: DataFrame, noc=None, team=None) -> Iterable:
    if noc is not None:
        filtered_df = df[df["NOC"] == noc]
    elif team is not None:
        filtered_df = df[df["Team"] == team]
    else:
        return ("I need a team name or NOC",)

    if len(filtered_df) == 0:
        return ("There isn't such a team. Check you input pls",)

    result_str_list = []

    filtered_df = filtered_df.sort_values(by=["Year"])

    first_year = filtered_df["Year"].iloc[0]
    first_city = filtered_df["City"].iloc[0]
    result_str_list.append(f"{team or noc} first time participated Olympics in {first_year}. It was in {first_city}")

    medals = pd.get_dummies(
        filtered_df, columns=["Medal"], dtype=int, prefix="", prefix_sep=""
    )
    medals = medals.loc[:, ["Year", "Bronze", "Silver", "Gold"]]
    medals_by_year = medals.groupby("Year", as_index=False).sum()
    medals_by_year["Sum of medals"] = medals_by_year["Bronze"] + medals_by_year["Silver"] + medals_by_year["Gold"]

    best_year = medals_by_year[
        medals_by_year["Sum of medals"] == medals_by_year["Sum of medals"].max()
        ]
    result_str_list.append(f"\nBest year: \n{best_year.to_string(index=False)}")

    worst_year = medals_by_year[
        medals_by_year["Sum of medals"] == medals_by_year["Sum of medals"].min()
        ]
    result_str_list.append(f"\nWorst year: \n{worst_year.to_string(index=False)}")

    num_of_olympics = len(pd.unique(filtered_df["Year"]))
    av_bronze = round(medals_by_year["Bronze"].sum()/num_of_olympics, 1)
    av_silver = round(medals_by_year["Silver"].sum()/num_of_olympics, 1)
    av_gold = round(medals_by_year["Gold"].sum()/num_of_olympics, 1)

    result_str_list.append(f"\nAverage results by one Olympics: \n"
                           f"Bronze {av_bronze}; Silver {av_silver}; Gold {av_gold}")

    return result_str_list

def get_stat_by_age_and_sex(df: DataFrame, is_male: bool, age_group: int) -> Iterable:
    """
    age groups:
    1: 12-18


    5:   -85
    """
    pass