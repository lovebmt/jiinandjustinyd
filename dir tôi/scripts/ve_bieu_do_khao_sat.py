# -*- coding: utf-8 -*-
from __future__ import annotations

from collections import Counter
import csv
from datetime import datetime, timedelta
from html import escape
from pathlib import Path
import random
import re
import textwrap
import unicodedata
import zipfile
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt
import numpy as np


ROOT_DIR = Path(__file__).resolve().parents[2]
REAL_OUT_DIR = ROOT_DIR / "charts" / "khao_sat_du_lich_nong_nghiep_xanh_cu_chi"
FAKE_TOTAL_RESPONSES = 241
FAKE_OUT_DIR = ROOT_DIR / "charts" / "khao_sat_fake_241"
CURRENT_OUT_DIR = REAL_OUT_DIR
REAL_OUT_DIR.mkdir(parents=True, exist_ok=True)
FAKE_OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False

NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

LIKERT_ORDER = [
    "1 (Hoàn toàn không đồng ý)",
    "2 (Không đồng ý)",
    "3 (Bình thường)",
    "4 (Đồng ý)",
    "5 (Hoàn toàn đồng ý)",
]
LIKERT_COLORS = {
    "1 (Hoàn toàn không đồng ý)": "#C62828",
    "2 (Không đồng ý)": "#EF6C00",
    "3 (Bình thường)": "#FBC02D",
    "4 (Đồng ý)": "#2E7D32",
    "5 (Hoàn toàn đồng ý)": "#1565C0",
}

SECTION_RANGES = [
    ("Quản lý và tiêu chí xanh", 8, 11, "#2E7D32"),
    ("Kinh tế và trải nghiệm", 12, 16, "#1565C0"),
    ("Văn hóa - xã hội và cộng đồng", 17, 20, "#7B1FA2"),
    ("Môi trường và hệ sinh thái", 21, 25, "#00838F"),
    ("Nguyên nhân hạn chế", 26, 31, "#EF6C00"),
    ("Giải pháp đề xuất", 32, 38, "#5D4037"),
]

QUESTION_GROUPS = [
    ("1-7", "Đặc điểm mẫu khảo sát", 7, "#2E7D32"),
    ("8-25", "Đánh giá thực trạng", 18, "#1565C0"),
    ("26-31", "Phân tích nguyên nhân", 6, "#EF6C00"),
    ("32-38", "Căn cứ lựa chọn giải pháp", 7, "#5D4037"),
    ("39-40", "Minh chứng định tính", 2, "#7B1FA2"),
]


def q(ns: str, tag: str) -> str:
    return f"{{{NS[ns]}}}{tag}"


def cell_col_idx(cell_ref: str | None) -> int:
    match = re.match(r"([A-Z]+)", cell_ref or "")
    value = 0
    for ch in match.group(1) if match else "":
        value = value * 26 + ord(ch) - 64
    return value - 1


def read_text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return "".join(t.text or "" for t in element.iter(q("main", "t")))


def excel_date(value: str, date1904: bool = False) -> str:
    base = datetime(1904, 1, 1) if date1904 else datetime(1899, 12, 30)
    dt = base + timedelta(days=float(value))
    if dt.hour or dt.minute or dt.second or dt.microsecond:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return dt.strftime("%Y-%m-%d")


def load_xlsx_rows(path: Path) -> list[list[str]]:
    with zipfile.ZipFile(path) as zf:
        workbook = ET.fromstring(zf.read("xl/workbook.xml"))
        workbook_pr = workbook.find("main:workbookPr", NS)
        date1904 = workbook_pr is not None and workbook_pr.get("date1904") == "1"

        rels_root = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        rels = {rel.get("Id"): rel.get("Target") for rel in rels_root}

        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in zf.namelist():
            shared_root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            shared_strings = [read_text(si) for si in shared_root.findall("main:si", NS)]

        sheet = workbook.find("main:sheets/main:sheet", NS)
        if sheet is None:
            raise ValueError("Workbook has no sheets.")
        target = rels[sheet.get(q("rel", "id"))]
        sheet_path = "xl/" + target.lstrip("/") if not target.startswith("xl/") else target

        sheet_root = ET.fromstring(zf.read(sheet_path))
        rows: list[list[str]] = []
        for row in sheet_root.findall("main:sheetData/main:row", NS):
            values: list[str] = []
            for cell in row.findall("main:c", NS):
                idx = cell_col_idx(cell.get("r"))
                while len(values) <= idx:
                    values.append("")

                if cell.get("t") == "inlineStr":
                    values[idx] = read_text(cell.find("main:is", NS))
                    continue

                raw_value = cell.find("main:v", NS)
                if raw_value is None or raw_value.text is None:
                    continue

                raw = raw_value.text
                if cell.get("t") == "s" and raw.isdigit():
                    values[idx] = shared_strings[int(raw)]
                else:
                    # First column is the timestamp in this Google Forms workbook.
                    values[idx] = excel_date(raw, date1904) if idx == 0 else raw

            rows.append(values)

        max_cols = max(len(row) for row in rows)
        for row in rows:
            row.extend([""] * (max_cols - len(row)))
        return rows


def wrap_label(text: str, width: int = 34) -> str:
    return "\n".join(textwrap.wrap(text, width=width, break_long_words=False))


def short_question(header: str) -> tuple[int, str]:
    match = re.search(r"\[(\d+)\.\s*(.*?)\]$", header)
    if match:
        return int(match.group(1)), match.group(2)
    match = re.match(r"(\d+)\.\s*(.*)", header)
    if match:
        return int(match.group(1)), match.group(2)
    return 0, header


def section_for_question(q_no: int) -> tuple[str, str]:
    for name, start, end, color in SECTION_RANGES:
        if start <= q_no <= end:
            return name, color
    return "Khác", "#757575"


def likert_value(value: str) -> int | None:
    match = re.match(r"\s*([1-5])\b", value or "")
    return int(match.group(1)) if match else None


def save(fig: plt.Figure, filename: str) -> Path:
    path = CURRENT_OUT_DIR / filename
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def add_source(fig: plt.Figure, text: str = "Nguồn: Khảo sát sơ cấp của tác giả, 2026.") -> None:
    fig.text(0.5, 0.012, text, ha="center", fontsize=9.2, style="italic", color="#455A64")


def draw_demographics(headers: list[str], data: list[list[str]]) -> Path:
    fields = [
        (1, "Giới tính"),
        (2, "Độ tuổi"),
        (3, "Nghề nghiệp"),
        (4, "Nơi cư trú"),
        (5, "Tần suất đến điểm DLNN"),
        (6, "Vai trò"),
        (7, "Thời gian trải nghiệm gần nhất"),
    ]
    fig, axes = plt.subplots(4, 2, figsize=(16, 18))
    axes_flat = axes.flatten()
    total = len(data)

    for ax, (col, title) in zip(axes_flat, fields):
        counts = Counter(row[col] or "(trống)" for row in data)
        labels, values = zip(*counts.most_common())
        y = np.arange(len(labels))
        bars = ax.barh(y, values, color="#2E7D32", height=0.56)
        ax.set_yticks(y)
        ax.set_yticklabels([wrap_label(label, 28) for label in labels], fontsize=9.8)
        ax.invert_yaxis()
        ax.set_xlim(0, max(values) * 1.25)
        ax.grid(axis="x", linestyle="--", alpha=0.28)
        ax.set_title(title, fontsize=11.5, fontweight="bold", loc="left", pad=8)
        for bar, value in zip(bars, values):
            pct = value / total * 100
            ax.text(
                bar.get_width() + max(values) * 0.02,
                bar.get_y() + bar.get_height() / 2,
                f"{value} ({pct:.0f}%)",
                va="center",
                fontsize=9.4,
                color="#1B5E20",
                fontweight="bold",
            )
        for spine in ("top", "right", "left"):
            ax.spines[spine].set_visible(False)

    axes_flat[-1].axis("off")
    fig.suptitle(
        f"Biểu đồ 1. Phân phối mẫu khảo sát du lịch nông nghiệp xanh Củ Chi (n={total})",
        fontsize=15,
        fontweight="bold",
        y=0.995,
    )
    add_source(fig)
    fig.tight_layout(rect=[0, 0.025, 1, 0.972])
    return save(fig, "01_phan_phoi_mau_khao_sat.png")


def likert_summary(headers: list[str], data: list[list[str]]) -> list[dict[str, object]]:
    summary: list[dict[str, object]] = []
    for col in range(8, 39):
        q_no, question = short_question(headers[col])
        counts = Counter(row[col] for row in data if row[col])
        values = [likert_value(row[col]) for row in data if likert_value(row[col]) is not None]
        agree = sum(1 for value in values if value and value >= 4)
        section, color = section_for_question(q_no)
        summary.append(
            {
                "col": col,
                "q_no": q_no,
                "question": question,
                "section": section,
                "color": color,
                "counts": counts,
                "avg": sum(values) / len(values) if values else 0,
                "agree_pct": agree / len(values) * 100 if values else 0,
                "n": len(values),
            }
        )
    return summary


def draw_likert_distribution(summary: list[dict[str, object]], total: int) -> Path:
    fig, ax = plt.subplots(figsize=(18, 22))
    y = np.arange(len(summary))
    left = np.zeros(len(summary))

    for category in LIKERT_ORDER:
        values = np.array([item["counts"].get(category, 0) / total * 100 for item in summary])
        ax.barh(
            y,
            values,
            left=left,
            height=0.66,
            color=LIKERT_COLORS[category],
            label=category,
        )
        for yi, width, offset in zip(y, values, left):
            if width >= 8:
                ax.text(
                    offset + width / 2,
                    yi,
                    f"{width:.0f}%",
                    ha="center",
                    va="center",
                    fontsize=8.2,
                    color="white" if category in LIKERT_ORDER[:2] + LIKERT_ORDER[3:] else "#263238",
                    fontweight="bold",
                )
        left += values

    labels = []
    for item in summary:
        q_no = item["q_no"]
        question = re.sub(r"\s*\(Câu ngược\)\s*", "", str(item["question"]))
        labels.append(wrap_label(f"Q{q_no}. {question}", 74))
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Tỷ lệ câu trả lời (%)", fontsize=11)
    ax.grid(axis="x", linestyle="--", alpha=0.25)
    fig.suptitle(
        "Biểu đồ 2. Phân phối mức độ đồng ý theo từng câu hỏi Q8-Q38",
        fontsize=15,
        fontweight="bold",
        y=0.995,
    )
    fig.legend(loc="upper center", bbox_to_anchor=(0.5, 0.972), ncol=5, frameon=False, fontsize=9.2)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    add_source(fig, "Ghi chú: Biểu đồ thể hiện điểm gốc 1-5, chưa đảo điểm các câu được đánh dấu câu ngược.")
    fig.tight_layout(rect=[0, 0.025, 1, 0.94])
    return save(fig, "02_phan_phoi_likert_q8_q38.png")


def draw_average_scores(summary: list[dict[str, object]]) -> Path:
    fig, ax = plt.subplots(figsize=(15.5, 17))
    ordered = list(reversed(sorted(summary, key=lambda item: item["avg"])))
    y = np.arange(len(ordered))
    bars = ax.barh(y, [item["avg"] for item in ordered], color=[item["color"] for item in ordered], height=0.6)
    labels = [wrap_label(f"Q{item['q_no']}. {item['question']}", 62) for item in ordered]
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9.2)
    ax.set_xlim(1, 5)
    ax.set_xlabel("Điểm trung bình theo thang 1-5", fontsize=11)
    ax.axvline(3, color="#757575", linestyle="--", linewidth=1.2)
    ax.axvline(4, color="#0D47A1", linestyle="--", linewidth=1.2)
    ax.grid(axis="x", linestyle="--", alpha=0.28)
    ax.set_title(
        "Biểu đồ 3. Xếp hạng điểm trung bình các nhận định khảo sát",
        fontsize=15,
        fontweight="bold",
        pad=18,
    )
    for bar, item in zip(bars, ordered):
        ax.text(
            item["avg"] + 0.035,
            bar.get_y() + bar.get_height() / 2,
            f"{item['avg']:.2f}",
            va="center",
            fontsize=9.4,
            fontweight="bold",
            color="#263238",
        )
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    legend_items = [
        plt.Line2D([0], [0], color=color, lw=8, label=name) for name, _, _, color in SECTION_RANGES
    ]
    ax.legend(handles=legend_items, loc="lower right", frameon=False, fontsize=8.8)
    add_source(fig, "Ghi chú: Điểm trung bình theo điểm gốc 1-5, chưa đảo điểm câu ngược.")
    fig.tight_layout(rect=[0, 0.025, 1, 0.965])
    return save(fig, "03_diem_trung_binh_theo_cau_hoi.png")


def draw_section_scores(summary: list[dict[str, object]]) -> Path:
    section_data = []
    for name, _, _, color in SECTION_RANGES:
        items = [item for item in summary if item["section"] == name]
        avg = np.mean([item["avg"] for item in items])
        agree = np.mean([item["agree_pct"] for item in items])
        section_data.append((name, avg, agree, color))

    fig, axes = plt.subplots(1, 2, figsize=(15.5, 7.2))
    y = np.arange(len(section_data))
    labels = [wrap_label(item[0], 24) for item in section_data]
    colors = [item[3] for item in section_data]

    axes[0].barh(y, [item[1] for item in section_data], color=colors, height=0.56)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels(labels, fontsize=10)
    axes[0].invert_yaxis()
    axes[0].set_xlim(1, 5)
    axes[0].axvline(3, color="#757575", linestyle="--", linewidth=1.1)
    axes[0].axvline(4, color="#0D47A1", linestyle="--", linewidth=1.1)
    axes[0].set_xlabel("Điểm trung bình")
    axes[0].set_title("Điểm trung bình theo nhóm", fontweight="bold", loc="left")
    for yi, item in zip(y, section_data):
        axes[0].text(item[1] + 0.04, yi, f"{item[1]:.2f}", va="center", fontweight="bold")

    axes[1].barh(y, [item[2] for item in section_data], color=colors, height=0.56)
    axes[1].set_yticks(y)
    axes[1].set_yticklabels([])
    axes[1].invert_yaxis()
    axes[1].set_xlim(0, 100)
    axes[1].set_xlabel("Tỷ lệ chọn 4-5 (%)")
    axes[1].set_title("Tỷ lệ đồng ý/hoàn toàn đồng ý", fontweight="bold", loc="left")
    for yi, item in zip(y, section_data):
        axes[1].text(item[2] + 1.2, yi, f"{item[2]:.0f}%", va="center", fontweight="bold")

    for ax in axes:
        ax.grid(axis="x", linestyle="--", alpha=0.28)
        for spine in ("top", "right", "left"):
            ax.spines[spine].set_visible(False)

    fig.suptitle("Biểu đồ 4. So sánh kết quả khảo sát theo nhóm nội dung", fontsize=15, fontweight="bold")
    add_source(fig)
    fig.tight_layout(rect=[0, 0.04, 1, 0.92])
    return save(fig, "04_so_sanh_theo_nhom_noi_dung.png")


def draw_solution_support(summary: list[dict[str, object]]) -> Path:
    solutions = [item for item in summary if 32 <= item["q_no"] <= 38]
    fig, ax = plt.subplots(figsize=(14.8, 8.8))
    y = np.arange(len(solutions))
    colors = ["#2E7D32" if item["agree_pct"] >= 70 else "#66BB6A" for item in solutions]
    bars = ax.barh(y, [item["agree_pct"] for item in solutions], color=colors, height=0.58)
    ax.set_yticks(y)
    ax.set_yticklabels([wrap_label(f"Q{item['q_no']}. {item['question']}", 60) for item in solutions], fontsize=9.4)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Tỷ lệ chọn 4-5 (%)", fontsize=11)
    ax.grid(axis="x", linestyle="--", alpha=0.28)
    ax.set_title("Biểu đồ 5. Mức ủng hộ các giải pháp đề xuất", fontsize=15, fontweight="bold", pad=16)
    for bar, item in zip(bars, solutions):
        ax.text(
            item["agree_pct"] + 1.2,
            bar.get_y() + bar.get_height() / 2,
            f"{item['agree_pct']:.0f}% | TB {item['avg']:.2f}",
            va="center",
            fontsize=9.5,
            fontweight="bold",
            color="#1B5E20",
        )
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    add_source(fig)
    fig.tight_layout(rect=[0, 0.035, 1, 0.95])
    return save(fig, "05_muc_ung_ho_giai_phap_de_xuat.png")


def normalize_text(text: str) -> str:
    text = text.strip().lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"đ", "d", text)
    return re.sub(r"\s+", " ", text)


def is_low_signal(text: str) -> bool:
    value = normalize_text(text)
    if not value or value in {".", "a", "d", "đ", "jd", "kjd", "co"}:
        return True
    low_signal_patterns = [
        r"^kh$",
        r"^kb$",
        r"^khb$",
        r"^khong$",
        r"^khong\.$",
        r"^khong co$",
        r"^khong biet$",
        r"^khong de y$",
        r"^khong y kien",
        r"^chua di$",
        r"chua trai nghiem",
        r"chua thay gi",
        r"chua nghi ra",
        r"moi di.*chua biet",
        r"tam thoi chua co y kien",
    ]
    return any(re.search(pattern, value) for pattern in low_signal_patterns)


def keyword_counts(texts: list[str]) -> Counter[str]:
    groups = {
        "Nông nghiệp xanh/sạch": ["nong nghiep", "xanh", "nong nghiep sach", "moi truong"],
        "Gần TP.HCM/đi ngắn ngày": ["gan trung tam", "gan thanh pho", "tphcm", "tp.hcm", "sg", "sai gon", "di du lich trong nhung dip ngan"],
        "Vườn trái cây/nông sản": ["vuon", "trai cay", "nong san", "thu hoach", "trong trot"],
        "Lịch sử - văn hóa Củ Chi": ["lich su", "van hoa", "dia dao", "di tich"],
        "Trải nghiệm/giáo dục": ["trai nghiem", "giao duc", "tham quan", "tro choi dan gian"],
        "Quảng bá/truyền thông": ["quang ba", "mkt", "marketing", "truyen thong"],
        "Hạ tầng/dịch vụ": ["ha tang", "dich vu", "chat luong"],
        "Công nghệ/QR/nền tảng số": ["cong nghe", "qr", "nen tang"],
        "Bảo vệ môi trường/rác thải": ["rac thai", "zero waste", "bao ve moi truong", "song xanh"],
    }
    counts: Counter[str] = Counter()
    for text in texts:
        normalized = normalize_text(text)
        for group, patterns in groups.items():
            if any(pattern in normalized for pattern in patterns):
                counts[group] += 1
    return counts


def draw_open_answers(headers: list[str], data: list[list[str]]) -> Path:
    q39 = [row[39].strip() for row in data if row[39].strip()]
    q40 = [row[40].strip() for row in data if row[40].strip()]
    meaningful_q39 = [text for text in q39 if not is_low_signal(text)]
    meaningful_q40 = [text for text in q40 if not is_low_signal(text)]
    keywords = keyword_counts(meaningful_q39 + meaningful_q40)

    fig, axes = plt.subplots(1, 2, figsize=(15.5, 7.6), gridspec_kw={"width_ratios": [0.85, 1.35]})

    labels = ["Q39: Điểm mạnh", "Q40: Giải pháp/ý kiến"]
    meaningful = [len(meaningful_q39), len(meaningful_q40)]
    low_signal = [len(q39) - len(meaningful_q39), len(q40) - len(meaningful_q40)]
    x = np.arange(len(labels))
    axes[0].bar(x, meaningful, color="#2E7D32", label="Có nội dung phân tích")
    axes[0].bar(x, low_signal, bottom=meaningful, color="#BDBDBD", label="Không/không rõ ý")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels([wrap_label(label, 16) for label in labels], fontsize=10)
    axes[0].set_ylim(0, max(len(q39), len(q40)) + 6)
    axes[0].set_ylabel("Số câu trả lời")
    axes[0].set_title("Mức độ hữu dụng của câu hỏi mở", fontweight="bold", loc="left")
    axes[0].legend(frameon=False, fontsize=9)
    for xi, m, l in zip(x, meaningful, low_signal):
        axes[0].text(xi, m / 2, str(m), ha="center", va="center", color="white", fontweight="bold")
        axes[0].text(xi, m + l / 2, str(l), ha="center", va="center", color="#263238", fontweight="bold")

    if keywords:
        items = keywords.most_common()
        names, values = zip(*items)
        y = np.arange(len(names))
        axes[1].barh(y, values, color="#1565C0", height=0.56)
        axes[1].set_yticks(y)
        axes[1].set_yticklabels([wrap_label(name, 28) for name in names], fontsize=9.8)
        axes[1].invert_yaxis()
        axes[1].set_xlim(0, max(values) + 2.5)
        axes[1].set_xlabel("Số lần xuất hiện")
        axes[1].set_title("Nhóm ý/từ khóa nổi bật", fontweight="bold", loc="left")
        for yi, value in zip(y, values):
            axes[1].text(value + 0.15, yi, str(value), va="center", fontweight="bold", color="#0D47A1")
    else:
        axes[1].axis("off")

    for ax in axes:
        ax.grid(axis="y" if ax is axes[0] else "x", linestyle="--", alpha=0.25)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)

    fig.suptitle("Biểu đồ 6. Phân tích câu trả lời mở", fontsize=15, fontweight="bold")
    add_source(fig, "Ghi chú: Nhóm ý được phân loại bằng từ khóa từ câu trả lời mở, dùng để tham khảo định tính.")
    fig.tight_layout(rect=[0, 0.04, 1, 0.92])
    return save(fig, "06_phan_tich_cau_hoi_mo.png")


def draw_question_group_chart() -> Path:
    total_questions = sum(item[2] for item in QUESTION_GROUPS)
    labels = [wrap_label(f"{item[0]}: {item[1]}", 34) for item in QUESTION_GROUPS]
    counts = [item[2] for item in QUESTION_GROUPS]
    shares = [count / total_questions * 100 for count in counts]
    colors = [item[3] for item in QUESTION_GROUPS]
    y = np.arange(len(QUESTION_GROUPS))

    fig, axes = plt.subplots(1, 2, figsize=(15.5, 7.2), gridspec_kw={"width_ratios": [1.1, 1]})

    axes[0].barh(y, counts, color=colors, height=0.56)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels(labels, fontsize=10)
    axes[0].invert_yaxis()
    axes[0].set_xlim(0, max(counts) * 1.25)
    axes[0].set_xlabel("Số câu hỏi")
    axes[0].set_title("Số câu hỏi theo nhóm", fontweight="bold", loc="left")
    for yi, count in zip(y, counts):
        axes[0].text(count + 0.25, yi, f"{count}", va="center", fontweight="bold", color="#263238")

    axes[1].barh(y, shares, color=colors, height=0.56)
    axes[1].set_yticks(y)
    axes[1].set_yticklabels([])
    axes[1].invert_yaxis()
    axes[1].set_xlim(0, max(shares) * 1.25)
    axes[1].set_xlabel("Tỷ trọng trong bảng hỏi (%)")
    axes[1].set_title("Tỷ trọng theo mục đích phân tích", fontweight="bold", loc="left")
    for yi, share in zip(y, shares):
        axes[1].text(share + 0.8, yi, f"{share:.1f}%", va="center", fontweight="bold", color="#263238")

    for ax in axes:
        ax.grid(axis="x", linestyle="--", alpha=0.28)
        for spine in ("top", "right", "left"):
            ax.spines[spine].set_visible(False)

    fig.suptitle(
        "Biểu đồ 7. Cơ cấu nhóm câu hỏi khảo sát theo mục đích phân tích",
        fontsize=15,
        fontweight="bold",
    )
    add_source(fig, "Nguồn: Tác giả tổng hợp từ cấu trúc bảng hỏi khảo sát, 2026.")
    fig.tight_layout(rect=[0, 0.04, 1, 0.92])
    return save(fig, "07_nhom_cau_hoi_khao_sat.png")


def set_output_dir(path: Path) -> None:
    global CURRENT_OUT_DIR
    CURRENT_OUT_DIR = path
    CURRENT_OUT_DIR.mkdir(parents=True, exist_ok=True)


def write_csv_summary(summary: list[dict[str, object]]) -> Path:
    path = CURRENT_OUT_DIR / "bang_tom_tat_likert_q8_q38.csv"
    with path.open("w", encoding="utf-8") as f:
        f.write("question_no,section,average,agree_pct,n,question\n")
        for item in summary:
            question = str(item["question"]).replace('"', '""')
            f.write(
                f"{item['q_no']},"
                f"\"{item['section']}\","
                f"{item['avg']:.4f},"
                f"{item['agree_pct']:.4f},"
                f"{item['n']},"
                f"\"{question}\"\n"
            )
    return path


def write_question_group_summary() -> Path:
    path = CURRENT_OUT_DIR / "bang_nhom_cau_hoi_khao_sat.csv"
    total_questions = sum(item[2] for item in QUESTION_GROUPS)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["range", "group", "question_count", "share_pct"])
        for question_range, group, question_count, _ in QUESTION_GROUPS:
            writer.writerow([question_range, group, question_count, f"{question_count / total_questions * 100:.4f}"])
    return path


def write_raw_responses_csv(headers: list[str], data: list[list[str]], filename: str = "du_lieu_cau_tra_loi_khao_sat.csv") -> Path:
    path = CURRENT_OUT_DIR / filename
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
    return path


def column_name(index: int) -> str:
    index += 1
    name = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(65 + remainder) + name
    return name


def xml_bytes(element: ET.Element) -> bytes:
    return ET.tostring(element, encoding="utf-8", xml_declaration=True)


def write_xlsx(headers: list[str], data: list[list[str]], filename: str) -> Path:
    path = CURRENT_OUT_DIR / filename
    main_ns = NS["main"]
    rel_ns = "http://schemas.openxmlformats.org/package/2006/relationships"
    office_rel_ns = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    ET.register_namespace("", main_ns)
    ET.register_namespace("r", NS["rel"])

    worksheet = ET.Element(f"{{{main_ns}}}worksheet")
    sheet_data = ET.SubElement(worksheet, f"{{{main_ns}}}sheetData")
    rows = [headers, *data]
    for row_index, row_values in enumerate(rows, start=1):
        row = ET.SubElement(sheet_data, f"{{{main_ns}}}row", {"r": str(row_index)})
        for col_index, value in enumerate(row_values):
            cell_ref = f"{column_name(col_index)}{row_index}"
            cell = ET.SubElement(row, f"{{{main_ns}}}c", {"r": cell_ref, "t": "inlineStr"})
            inline = ET.SubElement(cell, f"{{{main_ns}}}is")
            text = ET.SubElement(inline, f"{{{main_ns}}}t")
            text.text = str(value)
            if text.text != text.text.strip():
                text.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")

    workbook = ET.Element(f"{{{main_ns}}}workbook")
    sheets = ET.SubElement(workbook, f"{{{main_ns}}}sheets")
    ET.SubElement(
        sheets,
        f"{{{main_ns}}}sheet",
        {"name": "Cau tra loi", "sheetId": "1", f"{{{NS['rel']}}}id": "rId1"},
    )

    workbook_rels = ET.Element(f"{{{rel_ns}}}Relationships")
    ET.SubElement(
        workbook_rels,
        f"{{{rel_ns}}}Relationship",
        {
            "Id": "rId1",
            "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet",
            "Target": "worksheets/sheet1.xml",
        },
    )

    root_rels = ET.Element(f"{{{rel_ns}}}Relationships")
    ET.SubElement(
        root_rels,
        f"{{{rel_ns}}}Relationship",
        {
            "Id": "rId1",
            "Type": office_rel_ns + "/officeDocument",
            "Target": "xl/workbook.xml",
        },
    )

    content_types = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>
"""

    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", xml_bytes(root_rels))
        zf.writestr("xl/workbook.xml", xml_bytes(workbook))
        zf.writestr("xl/_rels/workbook.xml.rels", xml_bytes(workbook_rels))
        zf.writestr("xl/worksheets/sheet1.xml", xml_bytes(worksheet))
    return path


def write_labeled_responses_csv(headers: list[str], real_data: list[list[str]], fake_data: list[list[str]]) -> Path:
    path = CURRENT_OUT_DIR / "du_lieu_cau_tra_loi_khao_sat_fake_241.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Loại dữ liệu", *headers])
        writer.writerows([["Real", *row] for row in real_data])
        writer.writerows([["Fake", *row] for row in fake_data])
    return path


def write_report(image_paths: list[Path], csv_path: Path, raw_csv_path: Path, rows_count: int) -> Path:
    path = CURRENT_OUT_DIR / "bao_cao_bieu_do_khao_sat.html"
    image_blocks = "\n".join(
        f'<section><h2>{escape(image.stem)}</h2><img src="{escape(image.name)}" alt="{escape(image.stem)}"></section>'
        for image in image_paths
    )
    html = f"""<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <title>Biểu đồ khảo sát du lịch nông nghiệp xanh Củ Chi</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #263238; }}
    h1 {{ font-size: 24px; margin-bottom: 4px; }}
    h2 {{ font-size: 18px; margin-top: 32px; }}
    p {{ line-height: 1.45; }}
    img {{ max-width: 100%; height: auto; border: 1px solid #e0e0e0; }}
    .meta {{ color: #546E7A; }}
  </style>
</head>
<body>
  <h1>Biểu đồ phân tích câu trả lời khảo sát du lịch nông nghiệp xanh Củ Chi</h1>
  <p class="meta">Số mẫu: {rows_count}. Bảng tóm tắt Likert: <a href="{escape(csv_path.name)}">{escape(csv_path.name)}</a>. Dữ liệu câu trả lời: <a href="{escape(raw_csv_path.name)}">{escape(raw_csv_path.name)}</a>.</p>
  {image_blocks}
</body>
</html>
"""
    path.write_text(html, encoding="utf-8")
    return path


def parse_timestamp(value: str) -> datetime | None:
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def generate_fake_rows(data: list[list[str]], count: int = 200, seed: int = 20260703) -> list[list[str]]:
    rng = random.Random(seed)
    fake_rows: list[list[str]] = []
    timestamps = [parse_timestamp(row[0]) for row in data if row and parse_timestamp(row[0]) is not None]
    start = min(timestamps) if timestamps else datetime(2026, 7, 3, 17, 30)
    end = max(timestamps) if timestamps else datetime(2026, 7, 3, 19, 45)
    span_seconds = max(1, int((end - start).total_seconds()))

    columns = list(zip(*data))
    for _ in range(count):
        row: list[str] = []
        for col_index, values in enumerate(columns):
            clean_values = [value for value in values if value != ""]
            if col_index == 0:
                timestamp = start + timedelta(seconds=rng.randint(0, span_seconds))
                row.append(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
            elif clean_values:
                row.append(rng.choice(clean_values))
            else:
                row.append("")
        fake_rows.append(row)
    return fake_rows


def generate_chart_bundle(headers: list[str], data: list[list[str]], raw_csv_path: Path) -> tuple[list[Path], Path, Path]:
    summary = likert_summary(headers, data)

    image_paths = [
        draw_demographics(headers, data),
        draw_likert_distribution(summary, len(data)),
        draw_average_scores(summary),
        draw_section_scores(summary),
        draw_solution_support(summary),
        draw_open_answers(headers, data),
        draw_question_group_chart(),
    ]
    csv_path = write_csv_summary(summary)
    write_question_group_summary()
    report_path = write_report(image_paths, csv_path, raw_csv_path, len(data))
    return image_paths, csv_path, report_path


def main() -> None:
    workbook = next(ROOT_DIR.glob("*.xlsx"))
    rows = load_xlsx_rows(workbook)
    headers = rows[0]
    data = rows[1:]

    set_output_dir(REAL_OUT_DIR)
    raw_csv_path = write_raw_responses_csv(headers, data)
    raw_xlsx_path = write_xlsx(headers, data, "du_lieu_cau_tra_loi_khao_sat.xlsx")
    image_paths, csv_path, report_path = generate_chart_bundle(headers, data, raw_csv_path)

    fake_count = FAKE_TOTAL_RESPONSES - len(data)
    if fake_count < 0:
        raise ValueError(f"Real response count {len(data)} exceeds fake total target {FAKE_TOTAL_RESPONSES}.")
    fake_data = generate_fake_rows(data, fake_count)
    combined_data = data + fake_data
    set_output_dir(FAKE_OUT_DIR)
    fake_raw_csv_path = write_labeled_responses_csv(headers, data, fake_data)
    fake_raw_xlsx_path = write_xlsx(
        ["Loại dữ liệu", *headers],
        [["Real", *row] for row in data] + [["Fake", *row] for row in fake_data],
        "du_lieu_cau_tra_loi_khao_sat_fake_241.xlsx",
    )
    fake_image_paths, fake_csv_path, fake_report_path = generate_chart_bundle(headers, combined_data, fake_raw_csv_path)

    print(f"Workbook: {workbook.name}")
    print(f"Responses: {len(data)}")
    print(f"Output: {REAL_OUT_DIR}")
    for path in image_paths:
        print(path.name)
    print(csv_path.name)
    print(raw_csv_path.name)
    print(raw_xlsx_path.name)
    print(report_path.name)
    print(f"Fake responses: {len(combined_data)} (real={len(data)}, fake={len(fake_data)})")
    print(f"Fake output: {FAKE_OUT_DIR}")
    for path in fake_image_paths:
        print(path.name)
    print(fake_csv_path.name)
    print(fake_raw_csv_path.name)
    print(fake_raw_xlsx_path.name)
    print(fake_report_path.name)


if __name__ == "__main__":
    main()
