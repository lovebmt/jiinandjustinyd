import csv
from pathlib import Path


EXPECTED = [
    ("1-7", "Đặc điểm mẫu khảo sát", "7"),
    ("8-25", "Đánh giá thực trạng", "18"),
    ("26-31", "Phân tích nguyên nhân", "6"),
    ("32-38", "Căn cứ lựa chọn giải pháp", "7"),
    ("39-40", "Minh chứng định tính", "2"),
]


for root in [
    Path("charts/khao_sat_du_lich_nong_nghiep_xanh_cu_chi"),
    Path("charts/khao_sat_fake_241"),
]:
    path = root / "bang_nhom_cau_hoi_khao_sat.csv"
    assert path.exists(), f"question-group summary CSV must exist: {path}"
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    actual = [(row["range"], row["group"], row["question_count"]) for row in rows]
    assert actual == EXPECTED, f"unexpected question-group summary in {path}: {actual}"
