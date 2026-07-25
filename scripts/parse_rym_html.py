import re
from pathlib import Path

from bs4 import BeautifulSoup, Tag


HTML_PATH = Path("data/rym_chart.html")


def get_link_text(item: Tag, href_part: str) -> str:
    """读取指定链接中的文字。"""
    link = item.select_one(f'a[href*="{href_part}"]')
    return link.get_text(" ", strip=True) if link else ""


def get_date_text(item: Tag) -> str:
    """读取发行日期。"""
    selectors = [
        ".page_charts_section_charts_item_title_date_compact",
        ".page_charts_section_charts_item_date",
    ]

    for selector in selectors:
        element = item.select_one(selector)
        if element:
            text = element.get_text(" ", strip=True)
            return re.sub(r"\s+Album$", "", text)

    return ""


def extract_year(date_text: str) -> str:
    """从日期中提取四位年份。"""
    match = re.search(r"\b(?:19|20)\d{2}\b", date_text)
    return match.group(0) if match else ""


def get_album_title(item: Tag) -> str:
    """读取专辑名称。"""
    album_element = item.select_one(
        "a.page_charts_section_charts_item_link.release"
    )

    if album_element:
        return album_element.get_text(" ", strip=True)

    return ""


def main() -> None:
    if not HTML_PATH.exists():
        raise FileNotFoundError(f"找不到文件：{HTML_PATH}")

    html = HTML_PATH.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    soup = BeautifulSoup(html, "html.parser")

    items = soup.select(".page_charts_section_charts_item")

    print(f"找到 {len(items)} 个榜单条目")
    print("-" * 60)

    for rank, item in enumerate(items[:10], start=1):
        artist = get_link_text(item, "/artist/")
        album = get_album_title(item)
        date_text = get_date_text(item)
        year = extract_year(date_text)

        print(f"排名：{rank}")
        print(f"艺人：{artist}")
        print(f"专辑：{album}")
        print(f"年份：{year}")
        print(f"完整日期：{date_text}")
        print("-" * 60)


if __name__ == "__main__":
    main()
