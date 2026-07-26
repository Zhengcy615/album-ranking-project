import csv
import re
from pathlib import Path

from bs4 import BeautifulSoup, Tag


HTML_PATHS = [
    Path("data/raw/aoty/aoty_chart.html"),
    Path("data/raw/aoty/aoty_chart_page_2.html"),
    Path("data/raw/aoty/aoty_chart_page_3.html"),
    Path("data/raw/aoty/aoty_chart_page_4.html"),
]

OUTPUT_PATH = Path("data/processed/aoty_top100.csv")
TOP_N = 100


def get_text(item: Tag, selector: str) -> str:
    """读取指定元素中的文字。"""
    element = item.select_one(selector)

    if element is None:
        return ""

    return element.get_text(" ", strip=True)


def extract_year(date_text: str) -> str:
    """从完整日期中提取四位年份。"""
    match = re.search(r"\b(?:19|20)\d{2}\b", date_text)

    if match:
        return match.group(0)

    return ""


def extract_rank(item: Tag, fallback_rank: int) -> int:
    """读取网页中的实际排名；读取失败时使用顺序排名。"""
    rank_text = get_text(item, ".albumListRank")
    match = re.search(r"\d+", rank_text)

    if match:
        return int(match.group(0))

    return fallback_rank


def extract_artist_and_album(item: Tag) -> tuple[str, str]:
    """
    只读取专辑链接中的标题，
    避免把 albumListRank 中的排名混入艺人名称。
    """
    title_link = item.select_one(
        ".albumListTitle a[itemprop='url']"
    )

    if title_link is None:
        return "", ""

    full_title = title_link.get_text(" ", strip=True)

    if " - " in full_title:
        artist, album = full_title.split(" - ", 1)

        return artist.strip(), album.strip()

    return "", full_title.strip()


def clean_ratings_count(text: str) -> str:
    """从评分人数文字中只保留数字和逗号。"""
    match = re.search(r"[\d,]+", text)

    if match:
        return match.group(0)

    return ""


def parse_item(
    item: Tag,
    fallback_rank: int,
) -> dict[str, str] | None:
    """解析一个 AOTY 专辑条目。"""
    artist, album = extract_artist_and_album(item)

    if not album:
        return None

    date_text = get_text(item, ".albumListDate")
    user_score = get_text(item, ".scoreValue")
    ratings_text = get_text(item, ".scoreText")
    genres = get_text(item, ".albumListGenre")

    return {
        "rank": str(extract_rank(item, fallback_rank)),
        "artist": artist,
        "album": album,
        "year": extract_year(date_text),
        "release_date": date_text,
        "user_score": user_score,
        "ratings_count": clean_ratings_count(ratings_text),
        "genres": genres,
    }


def read_items(html_path: Path) -> list[Tag]:
    """读取一个 HTML 文件中的全部专辑条目。"""
    if not html_path.exists():
        raise FileNotFoundError(
            f"找不到文件：{html_path.resolve()}"
        )

    html = html_path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    return soup.select("div.albumListRow")


def main() -> None:
    rows: list[dict[str, str]] = []

    for html_path in HTML_PATHS:
        items = read_items(html_path)

        print(
            f"{html_path.name}：找到 {len(items)} 条"
        )

        for item in items:
            fallback_rank = len(rows) + 1

            row = parse_item(
                item,
                fallback_rank,
            )

            if row is not None:
                rows.append(row)

    rows = rows[:TOP_N]

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
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
        first_row = rows[0]

        print(
            "第一条："
            f"{first_row['artist']} - "
            f"{first_row['album']}"
        )


if __name__ == "__main__":
    main()
