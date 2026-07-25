from pathlib import Path
from bs4 import BeautifulSoup


HTML_PATH = Path("data/aoty_chart.html")


def main():
    html = HTML_PATH.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    soup = BeautifulSoup(html, "html.parser")

    item = soup.select_one("div.albumListRow")

    print("标题元素：")
    print(item.select_one(".albumListTitle"))

    print("\n所有 class：")

    for tag in item.find_all(class_=True):
        print(tag.name, tag.get("class"))


if __name__ == "__main__":
    main()
