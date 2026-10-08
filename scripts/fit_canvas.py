#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构图留白补救：把成图原样贴到更大的白画布上，使人物高度占比降到目标值。

用途：ImageGen 出图常把人物画满（实测高度占比 92–97%、脚贴底边），
而重 roll 会换掉整张脸和服装。本脚本只做画布扩展 —— 不缩放、不重采样、零画质损失。

算法：
  1. 二值化测出人物 bbox（非白像素）
  2. 目标画布高 = 人物高 / fill（默认 0.80），对齐 16px
  3. 画布宽 = 画布高 * ratio（默认 9:16），对齐 16px
  4. 把原图贴到使四周留白均衡的位置（px 偏移可为负，此时裁掉的是原图自身白边，无损）

用法：
    python scripts/fit_canvas.py <图片> [更多图片]
    python scripts/fit_canvas.py <图> --fill 0.78        # 目标高度占比，默认 0.80
    python scripts/fit_canvas.py <图> --ratio 3 4        # 画布比例，默认 9 16
    python scripts/fit_canvas.py <图> --inplace          # 覆盖原图（默认另存 *_framed）
    python scripts/fit_canvas.py <图> --report           # 只输出测量值，不写盘

依赖 Pillow：  <python> -m pip install Pillow
"""

import argparse
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DEFAULT_FILL = 0.80  # 目标：人物高度占画布高度的比例（审图规范要求 75–85%）
DEFAULT_RATIO = (9, 16)  # 画布宽:高
WHITE_CUT = 240  # min(r,g,b) 低于此值视为人物像素
MEASURE_W, MEASURE_H = 320, 570  # 测量用缩略图尺寸（够用且快）


def load_pillow():
    try:
        from PIL import Image
    except ImportError:
        print("缺少依赖 Pillow，请先安装：")
        print(f"  {sys.executable} -m pip install Pillow")
        sys.exit(3)
    return Image


def measure(px, w, h):
    """在缩略图上测人物 bbox，返回缩略图坐标 (top, bottom, left, right)。"""
    rows = [any(min(px[x, y]) < WHITE_CUT for x in range(w)) for y in range(h)]
    cols = [any(min(px[x, y]) < WHITE_CUT for y in range(h)) for x in range(w)]
    top = rows.index(True)
    bottom = h - 1 - rows[::-1].index(True)
    left = cols.index(True)
    right = w - 1 - cols[::-1].index(True)
    return top, bottom, left, right


def fit(path: Path, fill: float, ratio, inplace: bool, report: bool):
    Image = load_pillow()
    if not path.is_file():
        print(f"  跳过（不存在）：{path}")
        return None

    with Image.open(path) as img:
        img.load()
        work = img.convert("RGB")
    w, h = work.size

    small = work.resize((MEASURE_W, MEASURE_H), Image.LANCZOS)
    t, b, l, r = measure(small.load(), MEASURE_W, MEASURE_H)
    sx, sy = w / MEASURE_W, h / MEASURE_H
    ft, fb = t * sy, (b + 1) * sy
    fl, fr = l * sx, (r + 1) * sx
    fh, fw = fb - ft, fr - fl

    cur_h = fh / h
    cur_w = fw / w
    if report:
        print(f"  {path.name}：{w}x{h}  人物高占比 {cur_h:.1%}  宽占比 {cur_w:.1%}  "
              f"留白 上{t*sy/h:.1%} 下{(h-fb)/h:.1%} 左{fl/w:.1%} 右{(w-fr)/w:.1%}")
        return None

    ch = max(round((fh / fill) / 16) * 16, h)
    cw = max(round((ch * ratio[0] / ratio[1]) / 16) * 16, w)
    ox = round((cw - fw) / 2 - fl)
    oy = round((ch - fh) / 2 - ft)

    canvas = Image.new("RGB", (cw, ch), (255, 255, 255))
    if ox < 0:
        # 负偏移：先裁掉原图左侧白边（纯白区域，无损）
        canvas.paste(work.crop((-ox, 0, w, h)), (0, oy))
    elif oy < 0:
        canvas.paste(work.crop((0, -oy, w, h)), (ox, 0))
    else:
        canvas.paste(work, (ox, oy))

    out = path if inplace else path.with_name(f"{path.stem}_framed{path.suffix}")
    canvas.save(out)

    t2, b2, l2, r2 = measure(canvas.resize((MEASURE_W, MEASURE_H), Image.LANCZOS).load(),
                             MEASURE_W, MEASURE_H)
    print(f"  {path.name}：{w}x{h} -> {cw}x{ch}  人物高占比 {cur_h:.1%} -> {(b2 - t2 + 1) / MEASURE_H:.1%}  "
          f"留白 上{t2/MEASURE_H:.1%} 下{(MEASURE_H-1-b2)/MEASURE_H:.1%} "
          f"左{l2/MEASURE_W:.1%} 右{(MEASURE_W-1-r2)/MEASURE_W:.1%} -> {out.name}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="构图留白补救：扩展画布使人物高度占比达标")
    ap.add_argument("images", nargs="+", type=Path, help="图片路径，可多张")
    ap.add_argument("--fill", type=float, default=DEFAULT_FILL,
                    help=f"目标人物高度占比，默认 {DEFAULT_FILL}")
    ap.add_argument("--ratio", nargs=2, type=int, metavar=("W", "H"), default=list(DEFAULT_RATIO),
                    help="画布比例，默认 9 16")
    ap.add_argument("--inplace", action="store_true", help="覆盖原图（默认另存 *_framed）")
    ap.add_argument("--report", action="store_true", help="只测量不写盘")
    args = ap.parse_args()

    load_pillow()
    if args.report:
        print("测量模式（不写盘）：")
    else:
        print(f"目标人物高度占比 {args.fill:.0%}，画布比例 {args.ratio[0]}:{args.ratio[1]}")
    for p in args.images:
        fit(p, args.fill, tuple(args.ratio), args.inplace, args.report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
