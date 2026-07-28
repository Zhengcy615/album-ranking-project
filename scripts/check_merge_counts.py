import csv
import re
import unicodedata
from collections import defaultdict
from pathlib import Path


RYM_PATH = Path("data/processed/rym_top1000.csv")
AOTY_PATH = Path("data/processed/aoty_top500.csv")


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    text = text.casefold()
    text = text.replace("&", " and ")
    text = re.sub(r"[^\w]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def make_key(artist: str, album: str) -> tuple[str, str]:
    return (
        normalize_text(artist),
        normalize_text(album),
    )


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:
        return list(csv.DictReader(csv_file))


def find_duplicates(
    rows: list[dict[str, str]],
) -> dict[tuple[str, str], list[dict[str, str]]]:
    groups: dict[
        tuple[str, str],
        list[dict[str, str]],
    ] = defaultdict(list)

    for row in rows:
        key = make_key(
            row.get("artist", ""),
            row.get("album", ""),
        )
        groups[key].append(row)

    return {
        key: group
        for key, group in groups.items()
        if len(group) > 1
    }


def print_duplicate_report(
    name: str,
    duplicates: dict[
        tuple[str, str],
        list[dict[str, str]],
    ],
) -> None:
    print("=" * 70)
    print(f"{name} 内部重复键：{len(duplicates)} 组")

    for index, group in enumerate(
        duplicates.values(),
        start=1,
    ):
        print("-" * 70)
        print(f"第 {index} 组：")

        for row in group:
            print(
                f"rank={row.get('rank', '')} | "
                f"{row.get('artist', '')} - "
                f"{row.get('album', '')}"
            )


def main() -> None:
    rym_rows = read_csv(RYM_PATH)
    aoty_rows = read_csv(AOTY_PATH)

    rym_duplicates = find_duplicates(rym_rows)
    aoty_duplicates = find_duplicates(aoty_rows)

    rym_keys = {
        make_key(
            row.get("artist", ""),
            row.get("album", ""),
        )
        for row in rym_rows
    }

    aoty_keys = {
        make_key(
            row.get("artist", ""),
            row.get("album", ""),
        )
        for row in aoty_rows
    }

    overlap = rym_keys & aoty_keys
    union = rym_keys | aoty_keys

    print("=" * 70)
    print(f"RYM 原始行数：{len(rym_rows)}")
    print(f"RYM 唯一键数：{len(rym_keys)}")
    print(f"AOTY 原始行数：{len(aoty_rows)}")
    print(f"AOTY 唯一键数：{len(aoty_keys)}")
    print(f"跨榜单重合唯一键：{len(overlap)}")
    print(f"合并后理论唯一键：{len(union)}")
    print("=" * 70)

    print_duplicate_report(
        "RYM",
        rym_duplicates,
    )

    print_duplicate_report(
        "AOTY",
        aoty_duplicates,
    )


if __name__ == "__main__":
    main()
