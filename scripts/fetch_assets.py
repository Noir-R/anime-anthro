#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""确保 assets/ 下的系列参考图就位。

SkillHub 平台拒收二进制媒体（.png/.jpg/.jpeg/.webp/.svg 等一律 400），
因此本技能**发布时不携带图片**，改由本脚本在首次使用时从公开 CDN 拉取。

用法：
    python scripts/fetch_assets.py              # 缺失才下载，已存在的跳过
    python scripts/fetch_assets.py --force      # 全部重新下载
    python scripts/fetch_assets.py --check      # 只检查，不下载（返回码 0=齐全）

文件清单默认从 assets/README.md 的表格解析（单一数据源），解析失败才退回内置清单。
"""

import argparse
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:  # Windows 控制台默认 GBK，中文文件名会炸
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# 依次尝试；前一个失败自动回退到下一个
# 1) jsDelivr：国内通常更快  2) fastly 镜像  3) GitHub raw：兜底直连
BASE_URLS = [
    "https://cdn.jsdelivr.net/gh/Noir-R/anime-anthro@main/assets",
    "https://fastly.jsdelivr.net/gh/Noir-R/anime-anthro@main/assets",
    "https://raw.githubusercontent.com/Noir-R/anime-anthro/main/assets",
]

MIN_VALID_BYTES = 10 * 1024  # 小于 10KB 视为下载异常（占位/错误页）

# 内置兜底清单（仅当 assets/README.md 解析失败时使用）
FALLBACK_ASSET_FILES = [
    "style-ref-智谱-国风礼服.jpg",
    "style-ref-Kimi-三棱镜长裙.jpg",
    "style-ref-GPT-白龙.jpg",
    "style-ref-DeepSeek-鲸鱼女仆.jpg",
    "style-ref-Claude-古书.jpg",
    "style-ref-Grok-战斧.jpg",
    "style-ref-Qwen-轮椅病号服.jpg",
    "style-ref-MiniMax-场记板.jpg",
    "style-ref-Mistral-法棍猫耳.jpg",
    "style-ref-混元-冬装围巾.jpg",
    "style-ref-LLaMA-羊驼睡衣.jpg",
    "style-ref-Zai-黑狐.jpg",
    "style-ref-未确认-紫星猫耳.jpg",
    "style-ref-09-待确认.jpg",
    "chibi-ref-1-黑蓝舞娘.webp",
    "chibi-ref-2-紫黑慵懒.webp",
    "chibi-ref-3-国风斗篷冷淡.webp",
    "chibi-ref-4-白金制服.webp",
    "chibi-ref-5-运动服.webp",
]

README_NAME_RE = re.compile(r"`([^`\s]+\.(?:jpg|jpeg|png|webp))`")


def assets_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "assets"


def asset_files() -> tuple:
    """从 assets/README.md 解析清单，失败则退回内置清单。返回 (清单, 来源说明)。"""
    readme = assets_dir() / "README.md"
    if readme.is_file():
        try:
            text = readme.read_text(encoding="utf-8")
        except OSError:
            text = ""
        names, seen = [], set()
        for m in README_NAME_RE.finditer(text):
            n = m.group(1)
            if n not in seen:
                seen.add(n)
                names.append(n)
        if names:
            return names, "assets/README.md"
    return list(FALLBACK_ASSET_FILES), "内置兜底清单"


def looks_like_image(data: bytes, name: str) -> bool:
    """按魔数校验，防止把 HTML 错误页当成图片存下来。"""
    ext = Path(name).suffix.lower()
    if ext in (".jpg", ".jpeg"):
        return data[:3] == b"\xff\xd8\xff"
    if ext == ".png":
        return data[:8] == b"\x89PNG\r\n\x1a\n"
    if ext == ".webp":
        return data[:4] == b"RIFF" and data[8:12] == b"WEBP"
    return True  # 未知扩展名不校验


def is_valid_local(path: Path, name: str) -> bool:
    if not path.is_file() or path.stat().st_size < MIN_VALID_BYTES:
        return False
    try:
        with path.open("rb") as f:
            head = f.read(16)
    except OSError:
        return False
    return looks_like_image(head, name)


def missing_files(target: Path, files: list, force: bool) -> list:
    if force:
        return list(files)
    return [n for n in files if not is_valid_local(target / n, n)]


def download_one(base: str, name: str, dest: Path) -> bool:
    url = base + "/" + urllib.parse.quote(name)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "skill-asset-fetcher/1.1"})
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = resp.read()
        if len(data) < MIN_VALID_BYTES or not looks_like_image(data, name):
            return False
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        return True
    except (urllib.error.URLError, OSError, TimeoutError):
        return False


def main() -> int:
    ap = argparse.ArgumentParser(description="确保参考图就位")
    ap.add_argument("--force", action="store_true", help="无视已存在文件，全部重新下载")
    ap.add_argument("--check", action="store_true", help="只检查不下载")
    args = ap.parse_args()

    files, source = asset_files()
    target = assets_dir()
    target.mkdir(parents=True, exist_ok=True)
    todo = missing_files(target, files, args.force)

    if not todo:
        print(f"OK: 参考图已齐全（{len(files)} 张，清单来源：{source}）-> {target}")
        return 0

    if args.check:
        print(f"MISSING: 缺 {len(todo)} 张参考图：")
        for n in todo:
            print(f"  - {n}")
        print("提示：运行 python scripts/fetch_assets.py 下载，或手动放入 assets/ 目录。")
        return 1

    print(f"需要获取 {len(todo)} 张参考图 -> {target}")
    failed = []
    for i, name in enumerate(todo, 1):
        dest = target / name
        ok = False
        for base in BASE_URLS:
            if download_one(base, name, dest):
                print(f"  [{i}/{len(todo)}] {name}  ({dest.stat().st_size / 1024:.0f} KB)")
                ok = True
                break
        if not ok:
            print(f"  [{i}/{len(todo)}] {name}  失败")
            failed.append(name)

    if failed:
        print(f"\n警告：{len(failed)} 张下载失败：")
        for n in failed:
            print(f"  - {n}")
        print("可手动从 https://github.com/Noir-R/anime-anthro/tree/main/assets 下载后放入 assets/。")
        print("无参考图仍可生成，但画风一致性会下降。")
        return 2

    print(f"\n完成：{len(todo)} 张参考图已就位。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
