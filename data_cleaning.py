"""Funciones de limpieza y formateo para el dataset de clientes de la aseguradora."""

import pandas as pd

URL = "https://raw.githubusercontent.com/data-bootcamp-v4/data/main/file1.csv"

STATE_MAP = {"AZ": "Arizona", "Cali": "California", "WA": "Washington"}
GENDER_MAP = {"F": "F", "Femal": "F", "female": "F", "M": "M", "Male": "M"}
LUXURY_CLASSES = ["Sports Car", "Luxury SUV", "Luxury Car"]


def load_data(url=URL):
    return pd.read_csv(url)


def clean_column_names(df):
    df = df.copy()
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
    return df.rename(columns={"st": "state"})


def clean_invalid_values(df):
    df = df.copy()
    df["gender"] = df["gender"].map(GENDER_MAP)
    df["state"] = df["state"].replace(STATE_MAP)
    df["education"] = df["education"].replace("Bachelors", "Bachelor")
    df["customer_lifetime_value"] = df["customer_lifetime_value"].str.replace("%", "")
    df["vehicle_class"] = df["vehicle_class"].replace(LUXURY_CLASSES, "Luxury")
    return df


def format_data_types(df):
    df = df.copy()
    df["customer_lifetime_value"] = pd.to_numeric(df["customer_lifetime_value"])
    # "1/5/00" -> 5: nos quedamos con el valor del medio
    df["number_of_open_complaints"] = pd.to_numeric(
        df["number_of_open_complaints"].str.split("/").str[1]
    )
    return df


def handle_nulls(df):
    df = df.copy()
    # Filas 100% vacías: no aportan nada, se eliminan
    df = df.dropna(how="all")
    df["customer_lifetime_value"] = df["customer_lifetime_value"].fillna(
        df["customer_lifetime_value"].median()
    )
    df["gender"] = df["gender"].fillna("Unknown")
    numeric_cols = df.select_dtypes("number").columns
    df[numeric_cols] = df[numeric_cols].round().astype(int)
    return df


def handle_duplicates(df):
    return df.drop_duplicates().reset_index(drop=True)


def main(url=URL, output_path=None):
    df = load_data(url)
    df = clean_column_names(df)
    df = clean_invalid_values(df)
    df = format_data_types(df)
    df = handle_nulls(df)
    df = handle_duplicates(df)
    if output_path:
        df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    main(output_path="cleaned_insurance_data.csv")
