#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""去除生成图右下角的自动合规水印。

原理：白底立绘的右下角本应是纯白，水印是偏灰/偏深的像素。
在指定区域内把"亮度高于阈值"的像素直接置为纯白 —— 只有接近白色的像素会被改写，
人物边缘（暗色轮廓线）不会被误伤。

用法：
    python scripts/remove_watermark.py <图片路径> [更多路径...]
    python scripts/remove_watermark.py <图> --inplace          # 覆盖原图（默认另存 *_clean）
    python scripts/remove_watermark.py <图> --dry-run          # 只报告命中像素数，不写盘
    python scripts/remove_watermark.py <图> --region 0.72 0.90 # 自定义区域起点比例
    python scripts/remove_watermark.py <图> --threshold 145    # 自定义亮度阈值

依赖 Pillow。未安装时先执行：
    <python> -m pip install Pillow
"""

import argparse
import sys
from collections import deque
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DEFAULT_X0 = 0.72  # 区域起点：宽度的 72%
DEFAULT_Y0 = 0.90  # 区域起点：高度的 90%
DEFAULT_THRESHOLD = 145  # 亮度低于此值视为人物/轮廓，跳过
NEAR_WHITE = 250  # 亮度高于此值视为本就是白背景，跳过（否则整片背景都会被"处理"）
DEFAULT_MAX_BLOCK = 400  # 连通块像素上限：超过此值判定为衣物/裙摆，不处理（水印是细碎笔画）
# 教训：只按"区域+亮度"判断会把伸进角落的裙摆当成水印涂白（实测一次误判 2964 像素）。
# 水印特征 = 多个小连通块 + 贴底；裙摆特征 = 一两个大块 + 不贴底。


def load_pillow():
    try:
        from PIL import Image
    except ImportError:
        print("缺少依赖 Pillow，请先安装：")
        print(f"  {sys.executable} -m pip install Pillow")
        sys.exit(3)
    return Image


def build_blocks(hit, w, h):
    """把命中像素切成 4-邻接连通块，返回 (块大小列表, 每像素所属块号矩阵)。"""
    label = [[-1] * w for _ in range(h)]
    sizes = []
    for sy in range(h):
        for sx in range(w):
            if not hit[sy][sx] or label[sy][sx] != -1:
                continue
            bid = len(sizes)
            q = deque([(sy, sx)])
            label[sy][sx] = bid
            n = 0
            while q:
                cy, cx = q.popleft()
                n += 1
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < w and hit[ny][nx] and label[ny][nx] == -1:
                        label[ny][nx] = bid
                        q.append((ny, nx))
            sizes.append(n)
    return sizes, label


def process(path: Path, x0: float, y0: float, threshold: int, inplace: bool, dry_run: bool,
            max_block: int = DEFAULT_MAX_BLOCK):
    Image = load_pillow()
    if not path.is_file():
        print(f"  跳过（不存在）：{path}")
        return None

    with Image.open(path) as img:
        img.load()
        mode = img.mode
        if mode in ("RGBA", "LA", "P"):
            work = img.convert("RGBA")
            has_alpha = True
        else:
            work = img.convert("RGB")
            has_alpha = False

        w, h = work.size
        px = work.load()
        x_start, y_start = int(w * x0), int(h * y0)
        rw, rh = w - x_start, h - y_start

        # 第一遍：标记"灰"像素（非人物暗部、非纯白背景）
        hit = [[False] * rw for _ in range(rh)]
        for y in range(rh):
            for x in range(rw):
                r, g, b = px[x_start + x, y_start + y][:3]
                lum = 0.299 * r + 0.587 * g + 0.114 * b
                if threshold <= lum <= NEAR_WHITE:
                    hit[y][x] = True

        # 第二遍：连通域过滤 —— 大块是衣物/裙摆，不是水印
        sizes, label = build_blocks(hit, rw, rh)
        total_hit = sum(sizes)
        keep = [i for i, n in enumerate(sizes) if n <= max_block] if max_block else list(range(len(sizes)))
        keep_set = set(keep)
        kept = sum(sizes[i] for i in keep)

        # 形态报告：水印应是多个小块 + 贴底；裙摆是大块 + 不贴底
        bottom_hits = sum(1 for x in range(rw) if hit[rh - 1][x])
        biggest = max(sizes) if sizes else 0

        if dry_run:
            print(f"  {path.name}：区域 {rw}x{rh}，灰像素 {total_hit}，连通块 {len(sizes)}，最大块 {biggest}")
            print(f"      可处理（块 <= {max_block}px）{kept} 像素；底边命中 {bottom_hits}")
            if total_hit and kept == 0:
                print("      判定：大块集中，疑似衣物/裙摆而非水印 —— 未处理（如需强行处理用 --max-block 0）")
            elif kept and bottom_hits == 0 and biggest > max_block:
                print("      判定：混合区域，仅处理小块部分，请人工确认")
            return kept

        changed = 0
        for y in range(rh):
            row = label[y]
            for x in range(rw):
                b = row[x]
                if b in keep_set:
                    px[x_start + x, y_start + y] = (255, 255, 255, 255) if has_alpha else (255, 255, 255)
                    changed += 1

        if changed == 0:
            print(f"  {path.name}：未发现需要处理的像素（灰像素 {total_hit}，最大块 {biggest}），跳过")
            return 0

        if inplace:
            out = path
        else:
            out = path.with_name(f"{path.stem}_clean{path.suffix}")
        work.save(out)
        print(f"  {path.name}：处理 {changed} 像素（共 {len(keep)} 块）-> {out.name}")
        return changed


def main() -> int:
    ap = argparse.ArgumentParser(description="去除生成图右下角自动水印")
    ap.add_argument("images", nargs="+", type=Path, help="图片路径，可多张")
    ap.add_argument("--inplace", action="store_true", help="覆盖原图（默认另存 *_clean）")
    ap.add_argument("--dry-run", action="store_true", help="只报告，不写盘")
    ap.add_argument("--region", nargs=2, type=float, metavar=("X0", "Y0"),
                    default=[DEFAULT_X0, DEFAULT_Y0], help="区域起点比例，默认 0.72 0.90")
    ap.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD,
                    help=f"亮度阈值，默认 {DEFAULT_THRESHOLD}（越高越保守）")
    ap.add_argument("--max-block", type=int, default=DEFAULT_MAX_BLOCK,
                    help=f"连通块像素上限，默认 {DEFAULT_MAX_BLOCK}；0 = 不过滤（危险，会涂白裙摆）")
    args = ap.parse_args()

    load_pillow()  # 提前失败，避免逐张重复报错
    print(f"处理 {len(args.images)} 张，区域起点 ({args.region[0]}, {args.region[1]})，"
          f"阈值 {args.threshold}，块上限 {args.max_block or '不限'}")
    for p in args.images:
        process(p, args.region[0], args.region[1], args.threshold, args.inplace, args.dry_run,
                args.max_block)
    return 0


if __name__ == "__main__":
    sys.exit(main())
