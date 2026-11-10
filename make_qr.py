#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成二维码（PNG + SVG）。

用法：
    python make_qr.py https://你的网址
    python make_qr.py https://你的网址 --color "#8c1418" --name qr-final

依赖：pip install segno
"""
import argparse
import os
import sys

try:
    import segno
except ImportError:
    sys.exit("缺少依赖，请先运行：pip install segno")


def main():
    ap = argparse.ArgumentParser(description="把网址生成二维码")
    ap.add_argument("url", help="二维码要指向的网址（含 https://）")
    ap.add_argument("--name", default="qr", help="输出文件名（不含扩展名）")
    ap.add_argument("--outdir", default=".", help="输出目录")
    ap.add_argument("--color", default="#000000", help="前景色，默认纯黑")
    ap.add_argument("--scale", type=int, default=None, help="每模块像素数")
    args = ap.parse_args()

    qr = segno.make(args.url, error="q")  # Q 级容错，脏一点、斜一点也能扫

    os.makedirs(args.outdir, exist_ok=True)
    png = os.path.join(args.outdir, args.name + ".png")
    svg = os.path.join(args.outdir, args.name + ".svg")

    # 打印用：每模块按目标宽度反推，默认约 1200px
    scale = args.scale or max(6, 1200 // (qr.symbol_size(border=4)[0]))
    qr.save(png, scale=scale, border=4, dark=args.color, light="#ffffff")
    qr.save(svg, scale=10, border=4, dark=args.color, light="#ffffff")

    print("已生成：")
    print("  ", os.path.abspath(png))
    print("  ", os.path.abspath(svg))
    print("指向：", args.url)
    print("版本：", qr.version, " 纠错级别：", qr.error)


if __name__ == "__main__":
    main()