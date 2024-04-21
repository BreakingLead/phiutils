from bs4 import BeautifulSoup
import requests
import os
import json


# Not

buffer_path = "raw.html"


def get_html():
    html = ""
    if os.path.exists(buffer_path):
        f = open(buffer_path, "r", encoding="utf-8")
        html = f.read()
        f.close()
    else:
        data_url = (
            "https://zh.moegirl.org.cn/Phigros/%E8%B0%B1%E9%9D%A2%E4%BF%A1%E6%81%AF"
        )
        r = requests.get(data_url, timeout=5, headers={"User-agent": "the ua"})
        html = r.text
        f = open(buffer_path, "w+", encoding="utf-8")
        f.write(r.text)
        f.close()
    return html


def main():
    data = []

    soup = BeautifulSoup(get_html(), "lxml")
    tables = soup.find_all("table", attrs={"class": "wikitable"})

    for table in tables:

        item = {}

        for n, row in enumerate(table.find_all("tr")):
            if n == 0:
                item["name"] = row.th.string
            if n == 2:
                item["chapter"] = row.find_all("td")[1].string
            if n == 3:
                item["bpm"] = row.find_all("td")[1].string
                item["song_author"] = row.find_all("td")[3].string
            if n == 4:
                item["length"] = row.find_all("td")[1].string
                item["paint_author"] = row.find_all("td")[3].string
            if n == 6:
                # EZ
                # special judge for tutorial
                if not str(row("td")[2].string).isdecimal():
                    diff = 1.0
                else:
                    diff = float(row("td")[2].string)

                item["EZ"] = {
                    "rank": int(row("td")[1].string),
                    "difficulty": diff,
                    "count": int(row("td")[3].string),
                    "chart_author": row("td")[4].string,
                }
                pass
            if n == 7:
                # HD
                item["HD"] = {
                    "rank": int(row("td")[1].string),
                    "difficulty": float(row("td")[2].string),
                    "count": int(row("td")[3].string),
                    "chart_author": row("td")[4].string,
                }
                pass
            if n == 8:
                # IN
                item["IN"] = {
                    "rank": int(row("td")[1].string),
                    "difficulty": float(row("td")[2].string),
                    "count": int(row("td")[3].string),
                    "chart_author": row("td")[4].string,
                }
                pass
            if n == 10:
                # AT
                item["AT"] = {
                    "rank": int(row("td")[1].td.str),
                    "difficulty": float(row("td")[2].td.string),
                    "count": int(row("td")[3].td.string),
                    "chart_author": row("td")[4].td.string,
                }

        data.append(item)

        # temp

    with open("phigros_chart_data.json", "w+", encoding="utf-8") as out:
        json.dump(data, out, indent=4)


if __name__ == "__main__":
    main()
