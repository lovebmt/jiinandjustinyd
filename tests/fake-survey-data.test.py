from collections import Counter
import csv
from pathlib import Path


root = Path("charts/khao_sat_fake_241")
csv_path = root / "du_lieu_cau_tra_loi_khao_sat_fake_241.csv"

assert csv_path.exists(), "fake survey CSV must exist"

with csv_path.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.reader(f))

assert len(rows) == 242, f"expected header + 241 rows, got {len(rows)}"
assert len(rows[0]) == 42, f"expected source label + 41 original columns, got {len(rows[0])}"
assert rows[0][0] == "Loại dữ liệu", "first column must identify Real/Fake rows"

source_counts = Counter(row[0] for row in rows[1:])
assert source_counts["Real"] == 95, f"expected 95 real rows, got {source_counts['Real']}"
assert source_counts["Fake"] == 146, f"expected 146 fake rows, got {source_counts['Fake']}"

expected_images = [
    "01_phan_phoi_mau_khao_sat.png",
    "02_phan_phoi_likert_q8_q38.png",
    "03_diem_trung_binh_theo_cau_hoi.png",
    "04_so_sanh_theo_nhom_noi_dung.png",
    "05_muc_ung_ho_giai_phap_de_xuat.png",
    "06_phan_tich_cau_hoi_mo.png",
    "07_nhom_cau_hoi_khao_sat.png",
]

for image in expected_images:
    path = root / image
    assert path.exists(), f"fake survey chart must exist: {image}"
    assert path.stat().st_size > 100_000, f"fake survey chart is unexpectedly small: {image}"
