import argparse

from bs4 import BeautifulSoup as soup
from multiprocessing.dummy import Pool
import os
import shutil
import time
import requests
import re
import json
import glob
from urllib.request import Request, urlopen
import pandas as pd


if __name__ == "__main__":
    # wine_cols = ['Winery','Wine','Rating','Review_Count','Region','SubRegion']
    # wine_cols = ['wine brand name', 'wine name', 'year', 'style name', 'regional name', 'varietal name',
    #             'region', 'winery', 'price', 'rating', 'no. ratings', 'acidity', 'fizziness', 'intensity', 'sweetness', 'tannin']
    wine_cols = ['wine brand name', 'wine name', 'year', 'region', 'type', 'winery',
                 'price', 'rating', 'no. ratings']
    wine_df = pd.DataFrame(columns=wine_cols)

    for x in range(800, 900):

        r = requests.get(
            "https://www.vivino.com/api/explore/explore",
            params={
                "country_code": "FR",
                # "country_codes[]":"pt",
                "currency_code": "EUR",
                # "grape_filter":"varietal",
                "min_rating": "1",
                "order_by": "price",
                "order": "asc",
                "page": x,
                "price_range_max": "500",
                "price_range_min": "0",
                "wine_type_ids[]": "1"
            },
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
            }
        )

        # print(r.text)

        results = [
            (
                t["vintage"]["wine"]["name"],
                f'{t["vintage"]["wine"]["name"]} {t["vintage"]["year"]}',
                t["vintage"]["year"],
                # t["vintage"]["wine"]["style"]["name"],
                # t["vintage"]["wine"]["style"]["regional_name"],
                # t["vintage"]["wine"]["style"]["varietal_name"],
                t["vintage"]["wine"]["region"]["name"],
                t["vintage"]["wine"]["vintage_type"],
                t["vintage"]["wine"]["winery"]["name"],
                t["price"]["amount"],
                t["vintage"]["statistics"]["wine_ratings_average"],
                t["vintage"]["statistics"]["wine_ratings_count"]

                # t["vintage"]["wine"]["taste"]["structure"]["acidity"],
                # t["vintage"]["wine"]["taste"]["structure"]["fizziness"],
                # t["vintage"]["wine"]["taste"]["structure"]["intensity"],
                # t["vintage"]["wine"]["taste"]["structure"]["sweetness"],
                # t["vintage"]["wine"]["taste"]["structure"]["tannin"]
            )
            # (
            #    t["vintage"]["wine"]["winery"]["name"],
            #    f'{t["vintage"]["wine"]["name"]} {t["vintage"]["year"]}',
            #    t["vintage"]["statistics"]["ratings_average"],
            #    t["vintage"]["statistics"]["ratings_count"],
            #    t["vintage"]["wine"]["region"]["country"]["name"],
            #    t["vintage"]["wine"]["region"]["name"]
            # )
            for t in r.json()["explore_vintage"]["matches"]
        ]

        # for t in r.json()["explore_vintage"]["matches"]:
        #    print("newline\n")
        #    print(t)
        #    print("end newline\n")

        temp_df = pd.DataFrame(results, columns=wine_cols)
        wine_df = wine_df._append(temp_df, ignore_index=True)
        # dataframe = pd.DataFrame(results,columns=['Winery','Wine','Rating','num_review', ])

    print(wine_df.shape)
    print(wine_df.head)
    # wine_df.to_csv('test.csv')
    # Explore Columns To Include
    wine_dict = json.loads(json.dumps(r.json()))

    wine_df.to_csv('red8.csv')

    with open('red8.json', 'w') as fp:
        json.dump(wine_dict, fp, sort_keys=True, indent=4)

        # https://stackoverflow.com/questions/71264253/web-scraping-vivino-using-python
