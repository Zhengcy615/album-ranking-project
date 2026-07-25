import csv
import re
from pathlib import Path

from bs4 import BeautifulSoup


HTML_PATHS = [
    Path("data/aoty_chart.html"),
    Path("data/aoty_chart_page_2.html"),
    Path("data/aoty_chart_page_3.html"),
    Path("data/aoty_chart_page_4.html"),
]


OUTPUT_PATH = Path("data/aoty_top100.csv")


def extract_year(date_text):
    match = re.search(r"\b(19|20)\d{2}\b", date_text)

    return match.group(0) if match else ""


def parse_item(item, rank):

    title_element = item.select_one(".albumListTitle")

    if not title_element:
        return None


    title = title_element.get_text(" ", strip=True)


    if " - " in title:
        artist, album = title.split(" - ", 1)
    else:
        artist = ""
        album = title


    date_element = item.select_one(".albumListDate")
    date_text = (
        date_element.get_text(" ", strip=True)
        if date_element
        else ""
    )


    score_element = item.select_one(".scoreValue")
    score = (
        score_element.get_text(" ", strip=True)
        if score_element
        else ""
    )


    rating_element = item.select_one(".scoreText")
    ratings = (
        rating_element.get_text(" ", strip=True)
        if rating_element
        else ""
    )


    genre_element = item.select_one(".albumListGenre")
    genres = (
        genre_element.get_text(" ", strip=True)
        if genre_element
        else ""
    )


    return {
        "rank": rank,
        "artist": artist,
        "album": album,
        "year": extract_year(date_text),
        "release_date": date_text,
        "user_score": score,
        "ratings_count": ratings,
        "genres": genres,
    }



def main():

    rows = []

    for html_path in HTML_PATHS:

        html = html_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )


        soup = BeautifulSoup(
            html,
            "html.parser"
        )


        items = soup.select(
            "div.albumListRow"
        )


        print(
            html_path.name,
            "找到",
            len(items),
            "条"
        )


        for item in items:

            rank = len(rows) + 1

            data = parse_item(
                item,
                rank
            )

            if data:
                rows.append(data)


    rows = rows[:100]


    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as f:


        writer = csv.DictWriter(
            f,
            fieldnames=[
                "rank",
                "artist",
                "album",
                "year",
                "release_date",
                "user_score",
                "ratings_count",
                "genres",
            ]
        )

        writer.writeheader()
        writer.writerows(rows)


    print(
        "成功保存",
        len(rows),
        "条数据"
    )


if __name__ == "__main__":
    main()
