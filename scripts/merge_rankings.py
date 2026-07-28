
# merge_rankings.py
# RYM Top1000 + AOTY Top500
# 匹配规则：artist + album + year

import csv
import re
import unicodedata
from pathlib import Path

RYM_PATH = Path("data/processed/rym_top1000.csv")
AOTY_PATH = Path("data/processed/aoty_top500.csv")
OUTPUT_PATH = Path("data/processed/album_master.csv")


def normalize(text):
    text = unicodedata.normalize("NFKC", text or "")
    text = text.casefold()
    text = text.replace("&", " and ")
    text = re.sub(r"[^\w]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def make_key(row):
    return (
        normalize(row.get("artist", "")),
        normalize(row.get("album", "")),
        str(row.get("year", "")).strip(),
    )


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    rym = read_csv(RYM_PATH)
    aoty = read_csv(AOTY_PATH)

    albums = {}

    for row in rym:
        key = make_key(row)
        albums[key] = {
            "artist": row.get("artist", ""),
            "album": row.get("album", ""),
            "year": row.get("year", ""),
            "rym_rank": row.get("rank", ""),
            "aoty_rank": "",
            "source": "RYM",
            "aoty_user_score": "",
            "aoty_ratings_count": "",
            "aoty_genres": "",
        }

    overlap = 0

    for row in aoty:
        key = make_key(row)

        if key in albums:
            overlap += 1
            record = albums[key]
            record["aoty_rank"] = row.get("rank", "")
            record["aoty_user_score"] = row.get("user_score", "")
            record["aoty_ratings_count"] = row.get("ratings_count", "")
            record["aoty_genres"] = row.get("genres", "")
            record["source"] = "RYM + AOTY"

        else:
            albums[key] = {
                "artist": row.get("artist", ""),
                "album": row.get("album", ""),
                "year": row.get("year", ""),
                "rym_rank": "",
                "aoty_rank": row.get("rank", ""),
                "source": "AOTY",
                "aoty_user_score": row.get("user_score", ""),
                "aoty_ratings_count": row.get("ratings_count", ""),
                "aoty_genres": row.get("genres", ""),
            }

    rows = list(albums.values())

    rows.sort(
        key=lambda x: (
            int(x["rym_rank"]) if x["rym_rank"].isdigit() else 9999,
            int(x["aoty_rank"]) if x["aoty_rank"].isdigit() else 9999,
        )
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "artist",
                "album",
                "year",
                "rym_rank",
                "aoty_rank",
                "source",
                "aoty_user_score",
                "aoty_ratings_count",
                "aoty_genres",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print("-" * 60)
    print(f"RYM 数据：{len(rym)} 条")
    print(f"AOTY 数据：{len(aoty)} 条")
    print(f"两个榜单重合：{overlap} 张")
    print(f"合并后共有：{len(rows)} 张不同专辑")
    print(f"已保存：{OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()
