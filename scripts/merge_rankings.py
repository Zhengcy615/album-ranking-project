import csv
import re
import unicodedata
from pathlib import Path


RYM_PATH = Path("data/processed/rym_top100.csv")
AOTY_PATH = Path("data/processed/aoty_top100.csv")
OUTPUT_PATH = Path("data/processed/album_master.csv")


def remove_leading_rank(text: str) -> str:
    """
    清除 AOTY 艺人名前误加入的排名。

    示例：
    1. Kendrick Lamar -> Kendrick Lamar
    25 . David Bowie  -> David Bowie
    """
    text = text or ""

    return re.sub(
        r"^\s*\d+\s*[.)．、]?\s*",
        "",
        text,
    ).strip()


def normalize_text(text: str) -> str:
    """
    标准化艺人名和专辑名，用于匹配同一张专辑。

    处理内容：
    - 统一全角和半角字符
    - 忽略大小写
    - 将 & 统一为 and
    - 将斜杠、连字符和其他标点替换为空格
    - 合并多余空格

    示例：
    Either / Or -> either or
    Either/Or   -> either or
    """
    text = unicodedata.normalize(
        "NFKC",
        text or "",
    )

    text = text.casefold()

    text = text.replace(
        "&",
        " and ",
    )

    # 将所有标点和符号替换为空格，
    # 而不是直接删除，避免 Either/Or 变成 eitheror
    text = re.sub(
        r"[^\w]+",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def make_key(
    artist: str,
    album: str,
) -> tuple[str, str]:
    """生成用于匹配专辑的标准化键。"""
    return (
        normalize_text(artist),
        normalize_text(album),
    )


def read_csv(
    path: Path,
) -> list[dict[str, str]]:
    """读取一个 CSV 文件。"""
    if not path.exists():
        raise FileNotFoundError(
            f"找不到文件：{path.resolve()}"
        )

    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:
        return list(
            csv.DictReader(csv_file)
        )


def create_empty_record(
    artist: str,
    album: str,
    year: str,
) -> dict[str, str]:
    """创建统一格式的专辑记录。"""
    return {
        "artist": artist,
        "album": album,
        "year": year,
        "rym_rank": "",
        "aoty_rank": "",
        "source": "",
        "aoty_user_score": "",
        "aoty_ratings_count": "",
        "aoty_genres": "",
        "listening_status": "",
        "personal_rating": "",
        "favorite_level": "",
        "collection_status": "",
        "purchase_priority": "",
        "notes": "",
    }


def rank_number(value: str) -> int:
    """把排名转换成用于排序的数字。"""
    value = value.strip()

    if value.isdigit():
        return int(value)

    return 9999


def main() -> None:
    rym_rows = read_csv(RYM_PATH)
    aoty_rows = read_csv(AOTY_PATH)

    albums: dict[
        tuple[str, str],
        dict[str, str],
    ] = {}

    # 加入 RYM 数据
    for row in rym_rows:
        artist = row.get(
            "artist",
            "",
        ).strip()

        album = row.get(
            "album",
            "",
        ).strip()

        year = row.get(
            "year",
            "",
        ).strip()

        key = make_key(
            artist,
            album,
        )

        record = create_empty_record(
            artist=artist,
            album=album,
            year=year,
        )

        record["rym_rank"] = row.get(
            "rank",
            "",
        ).strip()

        record["source"] = "RYM"

        albums[key] = record

    # 加入 AOTY 数据
    for row in aoty_rows:
        artist = remove_leading_rank(
            row.get(
                "artist",
                "",
            )
        )

        album = row.get(
            "album",
            "",
        ).strip()

        year = row.get(
            "year",
            "",
        ).strip()

        key = make_key(
            artist,
            album,
        )

        if key not in albums:
            albums[key] = create_empty_record(
                artist=artist,
                album=album,
                year=year,
            )

        record = albums[key]

        record["aoty_rank"] = row.get(
            "rank",
            "",
        ).strip()

        record["aoty_user_score"] = row.get(
            "user_score",
            "",
        ).strip()

        record["aoty_ratings_count"] = row.get(
            "ratings_count",
            "",
        ).strip()

        record["aoty_genres"] = row.get(
            "genres",
            "",
        ).strip()

        if not record["year"]:
            record["year"] = year

        if record["rym_rank"]:
            record["source"] = "RYM + AOTY"
        else:
            record["source"] = "AOTY"

    output_rows = list(
        albums.values()
    )

    def sort_key(
        row: dict[str, str],
    ) -> tuple[int, int]:
        rym_rank = rank_number(
            row["rym_rank"]
        )

        aoty_rank = rank_number(
            row["aoty_rank"]
        )

        return (
            min(rym_rank, aoty_rank),
            max(rym_rank, aoty_rank),
        )

    output_rows.sort(
        key=sort_key
    )

    fieldnames = [
        "artist",
        "album",
        "year",
        "rym_rank",
        "aoty_rank",
        "source",
        "aoty_user_score",
        "aoty_ratings_count",
        "aoty_genres",
        "listening_status",
        "personal_rating",
        "favorite_level",
        "collection_status",
        "purchase_priority",
        "notes",
    ]

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
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(output_rows)

    overlap_count = sum(
        1
        for row in output_rows
        if row["rym_rank"]
        and row["aoty_rank"]
    )

    print(f"RYM 数据：{len(rym_rows)} 条")
    print(f"AOTY 数据：{len(aoty_rows)} 条")
    print(f"两个榜单重合：{overlap_count} 张")
    print(
        f"合并后共有："
        f"{len(output_rows)} 张不同专辑"
    )
    print(
        f"已保存："
        f"{OUTPUT_PATH.resolve()}"
    )


if __name__ == "__main__":
    main()
