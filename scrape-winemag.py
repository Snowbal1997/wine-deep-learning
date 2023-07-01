import requests
import json
from urllib.request import urlopen
import pandas as pd
import time


def run_scraper(run_number):
    wine_cols = [
        "wine brand name",
        "wine name",
        "year",
        "region",
        "type",
        "winery",
        "price",
        "rating",
        "no. ratings",
        "country",
    ]
    wine_df = pd.DataFrame(columns=wine_cols)

    min_price = str(run_number)
    max_price = str(run_number + 1)

    for x in range(0, 85):
        r = requests.get(
            "https://www.vivino.com/api/explore/explore",
            params={
                "country_code": "FR",
                "currency_code": "EUR",
                "order_by": "price",
                "order": "asc",
                "price_range_max": max_price,
                "price_range_min": min_price,
                "wine_type_ids[]": "1",  # red
                # "wine_type_ids[]": "2",  # white
            },
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
            },
        )

        results = [
            (
                t["vintage"]["wine"]["name"],
                f'{t["vintage"]["wine"]["name"]} {t["vintage"]["year"]}',
                t["vintage"]["year"],
                t["vintage"]["wine"]["region"]["seo_name"],
                t["vintage"]["wine"]["vintage_type"],
                t["vintage"]["wine"]["winery"]["name"],
                t["price"]["amount"],
                t["vintage"]["statistics"]["wine_ratings_average"],
                t["vintage"]["statistics"]["wine_ratings_count"],
                t["vintage"]["wine"]["region"]["country"]["native_name"],
            )
            for t in r.json()["explore_vintage"]["matches"]
        ]

        temp_df = pd.DataFrame(results, columns=wine_cols)
        wine_df = wine_df._append(temp_df, ignore_index=True)

        # last_row = len(wine_df) - 1
        # min_price = str(wine_df.loc[last_row, "price"] + 0.01)

        wine_dict = json.loads(json.dumps(r.json()))

        str_addition = min_price + "_" + max_price
        str_x_addition = "_" + str(x)

        with open(
            "newest_red/newest_red_" + str_addition + str_x_addition + ".json",
            "w",
        ) as fp:
            json.dump(wine_dict, fp, sort_keys=True, indent=4)

    # print(wine_df.shape)
    # print(wine_df.head)

    wine_df.to_csv("newest_red_" + str_addition + ".csv")

    print(run_number)
    print(len(wine_df))

    # https://stackoverflow.com/questions/71264253/web-scraping-vivino-using-python


if __name__ == "__main__":
    for run_num in range(73, 100):
        run_scraper(run_num)
        time.sleep(5)
