from pathlib import Path

from playwright.sync_api import sync_playwright


BASE_URL = "https://rateyourmusic.com/charts/top/album/all-time/"
DATA_DIR = Path("data")


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        for page_number in range(1, 4):
            if page_number == 1:
                url = BASE_URL
            else:
                url = f"{BASE_URL}{page_number}/"

            print(f"正在打开第 {page_number} 页：{url}")
            page.goto(url, wait_until="domcontentloaded")

            input(
                f"确认第 {page_number} 页榜单加载完成后，"
                "回到这里按 Enter 保存："
            )

            output_path = DATA_DIR / f"rym_chart_page_{page_number}.html"
            output_path.write_text(
                page.content(),
                encoding="utf-8",
            )

            print(f"已保存：{output_path}")

        browser.close()


if __name__ == "__main__":
    main()
