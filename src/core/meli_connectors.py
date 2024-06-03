"""This module contains the classes to connect to MercadoLibre API and gather
+data from it."""

import pandas as pd
from httpx import Client
from loguru import logger

from src.core import Country

log = logger.opt(colors=True)


class MercadoLibreItems:
    """This class is used to request the MercadoLibre API by country and gather
    +    all the products from all categories."""

    def __init__(self, country: Country):
        self._country = str(country.country)

        self.client = Client(base_url="https://api.mercadolibre.com/")
        self.country_id = self.get_country_id(country.country)
        self.cats = self.get_categories_given_country_id(self.country_id)

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, value: Country):
        self._country = str(value.country)
        self.country_id = self.get_country_id(self._country)
        self.cats = self.get_categories_given_country_id(self.country_id)

    def get_country_id(self, country: str) -> str:
        response = self.client.get("sites").json()
        for site in response:
            if site["name"] == country:
                return site["id"]
        raise ValueError("Country not found")

    def get_categories_given_country_id(self, country_id: str) -> dict:
        return self.client.get(f"sites/{country_id}/categories").json()

    def get_categories(self):
        self.cats = self.client.get(f"sites/{self.country_id}/categories").json()
        return self.cats

    def get_products_by_category(self, category_id: str, limit: int = 1000) -> pd.DataFrame:
        all_category_products = pd.DataFrame()

        for off in range(0, limit, 50):
            products = self.client.get(
                f"/sites/{self.country_id}/search?category={category_id}&offset={off}"
            ).json()

            all_category_products = pd.concat(
                [all_category_products, pd.DataFrame(products["results"])], ignore_index=True
            )

        return all_category_products

    def gell_all_country_products(self, limit: int = 1000) -> pd.DataFrame:
        all_country_products = pd.DataFrame()
        for category in self.cats:
            all_country_products = pd.concat(
                [all_country_products, self.get_products_by_category(category["id"], limit=limit)]
            )

        log.info(
            f"""You have collected: \n
            {all_country_products.shape[0]} products from {self.country} from {len(self.cats)} categories
            """
        )

        return all_country_products


class MercadoLibreUniverse:
    """This class is used to request the MercadoLibre API and gather all the
    +    categories from all countries."""

    def __init__(self):
        self.client = Client(base_url="https://api.mercadolibre.com/")

    def get_categories_given_country_id(self, country_id: str) -> dict:
        return self.client.get(f"sites/{country_id}/categories").json()

    def gather_countries_info(self):
        self.countries_details = self.client.get("/sites/").json()
        self.countries = [country["name"] for country in self.countries_details]
        self.df_countries_details = pd.DataFrame(self.countries_details)

    def get_all_categories_from_all_countries(self) -> pd.DataFrame:
        self.gather_countries_info()

        all_universe_cats = pd.DataFrame()

        for country in self.countries_details:
            cats = self.get_categories_given_country_id(country["id"])
            df_cats = pd.DataFrame(cats)
            df_cats["country_id"] = df_cats["id"].apply(lambda x: x[:3])
            df_cats["cat_code"] = df_cats["id"].apply(lambda x: x[3:])

            all_universe_cats = pd.concat([all_universe_cats, df_cats])

        del df_cats

        merged = all_universe_cats.merge(
            self.df_countries_details,
            left_on="country_id",
            right_on="id",
            suffixes=("_cat", "_country"),
        ).drop(columns=["country_id"])

        log.info(
            f"Total categories from all countries: {all_universe_cats.shape[0]} from {len(self.countries)} countries"
        )

        return merged
