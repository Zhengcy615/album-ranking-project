from playwright.sync_api import sync_playwright


RYM_URL = "https://rateyourmusic.com/charts/top/album/all-time/"


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False
        )

        page = browser.new_page()
        page.goto(RYM_URL, wait_until="domcontentloaded")

        print("页面标题：", page.title())
        print("当前网址：", page.url)

        input("页面打开后，按 Enter 关闭浏览器……")
        browser.close()


if __name__ == "__main__":
    main()
