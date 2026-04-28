import pandas as pd

from .config import COLUMNS, DATA_PATH, OUTLIER_QUANTILE


def load_data(path: str = DATA_PATH, columns: list[str] = COLUMNS) -> pd.DataFrame:
    return pd.read_csv(path, usecols=columns)


def add_date_parts(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df["year"] = df[date_col].dt.year
    df["month"] = df[date_col].dt.month
    return df


def remove_price_outliers(
    df: pd.DataFrame, price_col: str = "price", quantile: float = OUTLIER_QUANTILE
) -> pd.DataFrame:
    upper_limit = df[price_col].quantile(quantile)
    return df[df[price_col] <= upper_limit].copy()


def add_price_per_sqft(
    df: pd.DataFrame, price_col: str = "price", sqft_col: str = "sqft_living"
) -> pd.DataFrame:
    df = df.copy()
    df["price_per_sqft"] = df[price_col] / df[sqft_col]
    return df


def add_house_age(
    df: pd.DataFrame, year_col: str = "year", built_col: str = "yr_built"
) -> pd.DataFrame:
    df = df.copy()
    df["house_age"] = df[year_col] - df[built_col]
    return df


def add_price_segment(
    df: pd.DataFrame,
    price_col: str = "price",
    bins: int = 3,
    labels: tuple[str, str, str] = ("Low", "Mid", "High"),
) -> pd.DataFrame:
    df = df.copy()
    df["price_segment"] = pd.qcut(df[price_col], bins, labels=list(labels))
    return df
