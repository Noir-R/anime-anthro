#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""确保 assets/ 下的系列参考图就位。

SkillHub 平台拒收二进制媒体（.png/.jpg/.jpeg/.webp/.svg 等一律 400），
因此本技能**发布时不携带图片**，改由本脚本在首次使用时从公开 CDN 拉取。

用法：
    python scripts/fetch_assets.py              # 缺失才下载，已存在的跳过
    python scripts/fetch_assets.py --force      # 全部重新下载
    python scripts/fetch_assets.py --check      # 只检查，不下载（返回码 0=齐全）

Windows 下若报 UnicodeEncodeError，在命令前加 PYTHONIOENCODING=utf-8。
"""

import argparse
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# 系列参考图清单（正常比例 14 张 + Q 版 5 张）
ASSET_FILES = [
    # 正常比例：按模型 / 题材命名
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
    # Q 版
    "chibi-ref-1-黑蓝舞娘.webp",
    "chibi-ref-2-紫黑慵懒.webp",
    "chibi-ref-3-国风斗篷冷淡.webp",
    "chibi-ref-4-白金制服.webp",
    "chibi-ref-5-运动服.webp",
]

# 依次尝试；前一个失败自动回退到下一个
# 1) jsDelivr：国内通常更快  2) GitHub raw：兜底直连
BASE_URLS = [
    "https://cdn.jsdelivr.net/gh/Noir-R/anime-anthro@main/assets",
    "https://fastly.jsdelivr.net/gh/Noir-R/anime-anthro@main/assets",
    "https://raw.githubusercontent.com/Noir-R/anime-anthro/main/assets",
]

MIN_VALID_BYTES = 10 * 1024  # 小于 10KB 视为下载异常（占位/错误页）


def assets_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "assets"


def missing_files(target: Path, force: bool) -> list:
    if force:
        return list(ASSET_FILES)
    out = []
    for name in ASSET_FILES:
        p = target / name
        if not p.is_file() or p.stat().st_size < MIN_VALID_BYTES:
            out.append(name)
    return out


def download_one(base: str, name: str, dest: Path) -> bool:
    url = base + "/" + urllib.parse.quote(name)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "skill-asset-fetcher/1.0"})
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = resp.read()
        if len(data) < MIN_VALID_BYTES:
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

    target = assets_dir()
    target.mkdir(parents=True, exist_ok=True)
    todo = missing_files(target, args.force)

    if not todo:
        print(f"OK: 参考图已齐全（{len(ASSET_FILES)} 张）-> {target}")
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
