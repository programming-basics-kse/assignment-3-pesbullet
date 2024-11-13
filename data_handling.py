from pandas import DataFrame


def get_unique_names(df: DataFrame, column_name: str) -> list:
    return list(df[column_name].unique())


def get_medals_by_team_and_year(df: DataFrame, year: int, team=None, noc=None) -> DataFrame:
    pass


def get_total_by_year(df: DataFrame, year: int) -> DataFrame:
    pass


def get_teams_overall(df: DataFrame, teams: tuple) -> DataFrame:
    pass


def get_stat_by_team(df: DataFrame, team=None, noc=None) -> dict:
    pass
