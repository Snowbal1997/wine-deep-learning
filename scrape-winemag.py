import requests
import json
from urllib.request import urlopen
import pandas as pd


if __name__ == "__main__":
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
    min_price = str(0)  # 0 red
    # min_price = str(15.41)  # 1 red
    # min_price = str(25.21)  # 2 red
    # min_price = str(41.26)  # 3 red
    # min_price = str(72.96)  # 4 red
    # min_price = str(152.81)  # 5 red

    # min_price = str(0)  # 0 white
    # min_price = str(18.51)  # 1 white
    # min_price = str(41.76)  # 2 white

    # min_price = str(0) # 0 rose
    # min_price = str(345.41)  # 1 rose

    # try_name = "1"

    # for x in range(0, 85):
    for x in range(0, 2):
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
                # "page": x,
                "price_range_max": "500",
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
                # t["vintage"]["wine"]["style"]["name"],
                # t["vintage"]["wine"]["style"]["regional_name"],
                # t["vintage"]["wine"]["style"]["varietal_name"],
                t["vintage"]["wine"]["region"]["seo_name"],
                t["vintage"]["wine"]["vintage_type"],
                t["vintage"]["wine"]["winery"]["name"],
                t["price"]["amount"],
                t["vintage"]["statistics"]["wine_ratings_average"],
                t["vintage"]["statistics"]["wine_ratings_count"],
                t["vintage"]["wine"]["region"]["country"]["native_name"]
                # t["vintage"]["wine"]["taste"]["structure"]["acidity"] == NULL
                # t["vintage"]["wine"]["taste"]["structure"]["fizziness"],
                # t["vintage"]["wine"]["taste"]["structure"]["intensity"],
                # t["vintage"]["wine"]["taste"]["structure"]["sweetness"],
                # t["vintage"]["wine"]["taste"]["structure"]["tannin"]
            )
            for t in r.json()["explore_vintage"]["matches"]
        ]

        temp_df = pd.DataFrame(results, columns=wine_cols)
        wine_df = wine_df._append(temp_df, ignore_index=True)

        last_row = len(wine_df) - 1
        min_price = str(wine_df.loc[last_row, "price"] + 0.01)

        wine_dict = json.loads(json.dumps(r.json()))

        with open("testtt" + str(x) + ".json", "w") as fp:
            json.dump(wine_dict, fp, sort_keys=True, indent=4)

    print(wine_df.shape)
    print(wine_df.head)

    wine_df.to_csv("testtt.csv")
    print(min_price)

    # https://stackoverflow.com/questions/71264253/web-scraping-vivino-using-python
