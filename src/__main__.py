"""This script is used to gather data from MercadoLibre API and storeit in a
+database."""

import pandas as pd

from src.core import Country, MercadoLibreItems, MercadoLibreUniverse
from src.libs import DatabaseHandler, read_config_from_file


def main(config: dict) -> None:
    """Main function to gather data from MercadoLibre API and store it in a
    +    database."""
    _country = config["country"]

    meli = MercadoLibreItems(Country(country=_country))
    country_products = meli.gell_all_country_products()

    country_products = country_products.filter(
        ["id", "title", "price", "permalink", "condition", "available_quantity"]
    )

    meli_universe = MercadoLibreUniverse()
    categories_universe = meli_universe.get_all_categories_from_all_countries()

    with DatabaseHandler("meli.db") as db:
        country_products.to_sql(name=f"country_products_{_country}", con=db.cnx)
        categories_universe.to_sql(name="categories_universe", con=db.cnx)

        print("Data has been stored in the database.")

        print(db.get_table_names())
        print(db.get_table_columns("country_products_Bolivia"))
        print(db.get_table_columns("categories_universe"))
        print(db.get_table_data("categories_universe"))
        print(db.get_table_data("country_products_Bolivia"))

        df = pd.read_sql_query("SELECT * FROM categories_universe", db.cnx)
        print(df.head(2))

        df2 = pd.read_sql_query(f"SELECT * FROM country_products_{_country}", db.cnx)
        print(df2.head(2))


if __name__ == "__main__":
    config = read_config_from_file("src/config.json")
    main(config)
