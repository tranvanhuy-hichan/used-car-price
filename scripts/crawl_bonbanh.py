"""Thu thập tin ô tô cũ từ bonbanh.com (chỉ các trang danh sách, không vào từng tin).

Tuân thủ:
- robots.txt của bonbanh.com cho phép (Allow: /), không có hạn chế về AI.
- Chậm và lịch sự: nghỉ 2-3 giây giữa các yêu cầu, dừng ngay nếu bị chặn (403/429).
- Chỉ lưu thông tin về xe. KHÔNG lưu tên người bán, số điện thoại, ảnh.
- Dữ liệu thô nằm trong data/raw/ (đã .gitignore), không đưa lên GitHub.

Chạy:  python scripts/crawl_bonbanh.py --pages 200
Có thể chạy lại: các tin đã có (theo listing_id) sẽ không bị lặp.
"""
import argparse
import csv
import html
import random
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from used_car_price.config import RAW_PATH  # noqa: E402

BASE = "https://bonbanh.com"
UA = "Mozilla/5.0 (X11; Linux x86_64) student-ml-project"
FIELDS = ["listing_id", "brand", "model", "year", "gearbox", "fuel", "province", "origin",
          "seats", "km", "price_million", "crawled_at"]

# Hãng có tên nhiều từ (tên 1 từ lấy từ đầu tiên của tiêu đề)
MULTI_WORD_BRANDS = ["Mercedes Benz", "Mercedes-Benz", "Land Rover", "Rolls Royce", "Rolls-Royce",
                     "Aston Martin", "Alfa Romeo", "Great Wall", "Mini Cooper"]
BRAND_ALIASES = {"Mercedes-Benz": "Mercedes Benz", "Rolls-Royce": "Rolls Royce", "Mini Cooper": "Mini"}


def fetch(url: str, retries: int = 3) -> str | None:
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "vi"})
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.read().decode("utf-8", errors="ignore")
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                print(f"  ! Bị chặn/giới hạn tốc độ (HTTP {e.code}). Dừng để không gây tải.")
                raise SystemExit(1)
            print(f"  ! HTTP {e.code}, thử lại ({attempt + 1}/{retries})")
        except Exception as e:  # mạng chập chờn
            print(f"  ! {type(e).__name__}: {e}, thử lại ({attempt + 1}/{retries})")
        time.sleep(5 * (attempt + 1))
    return None


def split_brand_model(name: str):
    for b in MULTI_WORD_BRANDS:
        if name.lower().startswith(b.lower() + " "):
            rest = name[len(b):].split()
            return BRAND_ALIASES.get(b, b), (rest[0] if rest else "")
    parts = name.split()
    return (parts[0], parts[1]) if len(parts) > 1 else (parts[0], "")


def parse_item(block: str) -> dict | None:
    cond = re.search(r'<div class="cb1">\s*(.*?)<br>', block, re.S)
    if not cond or "cũ" not in cond.group(1):          # bỏ xe mới
        return None
    href = re.search(r'itemprop="url" href="[^"]*?-(\d+)"', block)
    name = re.search(r'<h3 itemprop="name">(.*?)</h3>', block, re.S)
    price = re.search(r'itemprop="price" content="(\d+)"', block)
    prov = re.search(r'<div class="cb4">\s*<b>(.*?)</b>', block, re.S)
    desc = re.search(r'itemprop="description">\s*(.*?)<br>', block, re.S)
    if not (href and name and price and prov and desc):
        return None

    title = html.unescape(re.sub(r"<.*?>", "", name.group(1))).strip()
    m = re.match(r"(.*?)\s*-\s*(\d{4})\s*$", title)
    if not m:
        return None
    car_name, year = m.group(1), int(m.group(2))
    brand, model = split_brand_model(car_name)

    d = html.unescape(re.sub(r"<.*?>", "", desc.group(1))).lower()
    fuel = ("điện" if re.search(r"xe điện|động cơ điện", d) else
            "hybrid" if "hybrid" in d else
            "dầu" if re.search(r"máy dầu", d) else
            "xăng" if re.search(r"máy xăng", d) else "")
    gearbox = "tự động" if "số tự động" in d else "số sàn" if re.search(r"số tay|số sàn", d) else ""
    origin = "nhập khẩu" if "nhập khẩu" in d else "trong nước" if "trong nước" in d else ""
    seats = re.search(r"(\d+)\s*chỗ", d)
    km = re.search(r"đã đi\s*([\d.,]+)\s*km", d)

    return {
        "listing_id": href.group(1), "brand": brand, "model": model, "year": year,
        "gearbox": gearbox, "fuel": fuel, "province": html.unescape(prov.group(1)).strip(),
        "origin": origin, "seats": int(seats.group(1)) if seats else "",
        "km": int(re.sub(r"[.,]", "", km.group(1))) if km else "",
        "price_million": round(int(price.group(1)) / 1e6, 1), "crawled_at": date.today().isoformat(),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--pages", type=int, default=200, help="số trang cần lấy")
    ap.add_argument("--delay", type=float, default=2.0, help="giây nghỉ tối thiểu giữa các yêu cầu")
    ap.add_argument("--out", type=Path, default=RAW_PATH)
    args = ap.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    seen = set()
    if args.out.exists():
        with open(args.out, encoding="utf-8") as f:
            seen = {r["listing_id"] for r in csv.DictReader(f)}
        print(f"Đã có {len(seen)} tin trong {args.out.name}, sẽ bỏ qua tin trùng.")
    new_file = not args.out.exists()

    total_new = 0
    with open(args.out, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            w.writeheader()
        for page in range(args.start, args.start + args.pages):
            page_html = fetch(f"{BASE}/oto/page,{page}")
            if page_html is None:
                print(f"Trang {page}: không tải được, dừng.")
                break
            blocks = re.split(r'<li class="car-item', page_html)[1:]
            if not blocks:
                print(f"Trang {page}: không còn tin, dừng.")
                break
            got = 0
            for b in blocks:
                row = parse_item(b)
                if row and row["listing_id"] not in seen:
                    seen.add(row["listing_id"]); w.writerow(row); got += 1
            f.flush(); total_new += got
            print(f"Trang {page}: {len(blocks)} tin, lưu mới {got} (tổng mới {total_new})")
            time.sleep(args.delay + random.uniform(0, 1.0))
    print(f"Xong. Đã thêm {total_new} tin vào {args.out}")


if __name__ == "__main__":
    main()
