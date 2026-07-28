import csv
import re
from pathlib import Path

from bs4 import BeautifulSoup, Tag


HTML_PATHS = [
    Path("data/raw/rym/rym_chart.html"),
] + [
    Path(f"data/raw/rym/rym_chart_page_{page}.html")
    for page in range(2, 26)
]

OUTPUT_PATH = Path("data/processed/rym_top1000.csv")
TOP_N = 1000


def get_link_text(item: Tag, href_part: str) -> str:
    """读取指定链接中的文字。"""
    link = item.select_one(
        f'a[href*="{href_part}"]'
    )

    if link is None:
        return ""

    return link.get_text(
        " ",
        strip=True,
    )


def get_date_text(item: Tag) -> str:
    """读取发行日期。"""
    selectors = [
        ".page_charts_section_charts_item_title_date_compact",
        ".page_charts_section_charts_item_date",
    ]

    for selector in selectors:
        element = item.select_one(
            selector
        )

        if element is not None:
            text = element.get_text(
                " ",
                strip=True,
            )

            return re.sub(
                r"\s+Album$",
                "",
                text,
            )

    return ""


def extract_year(date_text: str) -> str:
    """从日期中提取四位年份。"""
    match = re.search(
        r"\b(?:19|20)\d{2}\b",
        date_text,
    )

    if match:
        return match.group(0)

    return ""


def get_album_title(item: Tag) -> str:
    """读取专辑名称。"""
    album_element = item.select_one(
        "a.page_charts_section_charts_item_link.release"
    )

    if album_element is None:
        return ""

    return album_element.get_text(
        " ",
        strip=True,
    )


def extract_items(
    html_path: Path,
) -> list[Tag]:
    """从一个 HTML 文件中读取所有榜单条目。"""
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

    return soup.select(
        ".page_charts_section_charts_item"
    )


def main() -> None:
    all_items: list[Tag] = []

    for html_path in HTML_PATHS:
        items = extract_items(
            html_path
        )

        print(
            f"{html_path.name}："
            f"找到 {len(items)} 个榜单条目"
        )

        all_items.extend(items)

    print("-" * 60)
    print(
        f"25 页合计找到 "
        f"{len(all_items)} 个榜单条目"
    )

    rows: list[dict[str, str | int]] = []

    for rank, item in enumerate(
        all_items[:TOP_N],
        start=1,
    ):
        artist = get_link_text(
            item,
            "/artist/",
        )

        album = get_album_title(
            item
        )

        date_text = get_date_text(
            item
        )

        year = extract_year(
            date_text
        )

        rows.append(
            {
                "rank": rank,
                "artist": artist,
                "album": album,
                "year": year,
                "release_date": date_text,
            }
        )

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
            ],
        )

        writer.writeheader()
        writer.writerows(rows)

    print("-" * 60)
    print(
        f"成功保存 {len(rows)} 条数据"
    )
    print(
        f"文件位置："
        f"{OUTPUT_PATH.resolve()}"
    )

    if rows:
        first_row = rows[0]
        last_row = rows[-1]

        print(
            "第一条："
            f"{first_row['artist']} - "
            f"{first_row['album']}"
        )

        print(
            "最后一条："
            f"{last_row['artist']} - "
            f"{last_row['album']}"
        )


if __name__ == "__main__":
    main()
