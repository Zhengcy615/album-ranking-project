import csv
import re
from pathlib import Path
from bs4 import BeautifulSoup, Tag

HTML_PATHS = [
    Path("data/raw/aoty/aoty_chart.html"),
] + [
    Path(f"data/raw/aoty/aoty_chart_page_{i}.html")
    for i in range(2, 21)
]

OUTPUT_PATH = Path("data/processed/aoty_top500.csv")


def text(item: Tag, selector: str) -> str:
    node = item.select_one(selector)
    if node is None:
        return ""
    return node.get_text(" ", strip=True)


def year_from(text_value: str) -> str:
    m = re.search(r"\b(?:19|20)\d{2}\b", text_value or "")
    return m.group(0) if m else ""


def clean_rank(value: str, fallback: int) -> str:
    m = re.search(r"\d+", value or "")
    return m.group(0) if m else str(fallback)


def parse_title(item: Tag):
    node = item.select_one(".albumListTitle a")
    if node is None:
        return "", ""

    title = node.get_text(" ", strip=True)

    if " - " in title:
        artist, album = title.split(" - ", 1)
        return artist.strip(), album.strip()

    return "", title.strip()


def parse_page(path: Path, start_rank: int):
    html = path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    soup = BeautifulSoup(html, "html.parser")

    items = soup.select("div.albumListRow")

    rows = []

    for index, item in enumerate(items):
        artist, album = parse_title(item)

        if not album:
            continue

        date = text(item, ".albumListDate")

        rows.append({
            "rank": clean_rank(
                text(item, ".albumListRank"),
                start_rank + index
            ),
            "artist": artist,
            "album": album,
            "year": year_from(date),
            "release_date": date,
            "user_score": text(item, ".scoreValue"),
            "ratings_count": re.sub(
                r"\D",
                "",
                text(item, ".scoreText")
            ),
            "genres": text(item, ".albumListGenre"),
        })

    return rows


def main():
    rows = []

    for i, path in enumerate(HTML_PATHS):
        page_rows = parse_page(
            path,
            i * 25 + 1
        )

        print(
            f"{path.name}: 找到 {len(page_rows)} 条"
        )

        rows.extend(page_rows)

    # 保留500条，按网页顺序
    rows = rows[:500]

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

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
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print("-" * 60)
    print(f"成功保存 {len(rows)} 条数据")
    print(f"文件位置：{OUTPUT_PATH.resolve()}")

    if rows:
        print(
            f"第一条：{rows[0]['artist']} - {rows[0]['album']}"
        )
        print(
            f"最后一条：{rows[-1]['artist']} - {rows[-1]['album']}"
        )


if __name__ == "__main__":
    main()
