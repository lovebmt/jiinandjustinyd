from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon


BASE_DIR = Path(__file__).resolve().parents[1]
FIG_DIR = BASE_DIR / "figures"
MD_DIR = BASE_DIR / "markdown" / "04_hinh_bieu_do"

FIG_DIR.mkdir(parents=True, exist_ok=True)
MD_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False


def wrap(text, width=24):
    return "\n".join(textwrap.wrap(text, width=width, break_long_words=False))


def clean(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")


def box(ax, xy, w, h, text, fc="#F7FBF7", ec="#2E7D32", size=10,
        weight="normal", radius=0.018, lw=1.2):
    x, y = xy
    patch = FancyBboxPatch(
        (x - w / 2, y - h / 2),
        w,
        h,
        boxstyle=f"round,pad=0.012,rounding_size={radius}",
        linewidth=lw,
        edgecolor=ec,
        facecolor=fc,
        transform=ax.transAxes,
    )
    ax.add_patch(patch)
    ax.text(
        x,
        y,
        text,
        ha="center",
        va="center",
        fontsize=size,
        fontweight=weight,
        transform=ax.transAxes,
    )
    return patch


def arrow(ax, start, end, color="#1B5E20", lw=1.5, mutation=13):
    arr = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=mutation,
        linewidth=lw,
        color=color,
        transform=ax.transAxes,
    )
    ax.add_patch(arr)


def save(fig, filename):
    path = FIG_DIR / filename
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def draw_hinh_1_1():
    fig, ax = plt.subplots(figsize=(14, 8.4))
    clean(ax)

    ax.text(
        0.5,
        0.965,
        "Hình 1.1. Khung phân tích phát triển du lịch nông nghiệp xanh tại xã Củ Chi",
        ha="center",
        va="top",
        fontsize=14,
        fontweight="bold",
        transform=ax.transAxes,
    )

    box(ax, (0.5, 0.81), 0.84, 0.055, "CƠ SỞ PHÂN TÍCH", fc="#FAFAFA", ec="#757575", size=10.5, weight="bold")
    input_items = [
        (0.14, "Lý thuyết\nphát triển bền vững", "#E3F2FD", "#1565C0"),
        (0.32, "Tiêu chí GSTC\nvề du lịch xanh", "#E8F5E9", "#2E7D32"),
        (0.50, "SWOT, PESTLE\nRoot Cause", "#FFF3E0", "#EF6C00"),
        (0.68, "Chuỗi giá trị\ndu lịch", "#F3E5F5", "#7B1FA2"),
        (0.86, "Quản trị dịch vụ\ntrải nghiệm", "#E0F7FA", "#00838F"),
    ]
    for x, text, fc, ec in input_items:
        box(ax, (x, 0.70), 0.16, 0.105, text, fc=fc, ec=ec, size=8.9, weight="bold")

    arrow(ax, (0.5, 0.64), (0.5, 0.57), color="#455A64", lw=1.6)
    box(
        ax,
        (0.5, 0.49),
        0.36,
        0.12,
        "ĐÁNH GIÁ THỰC TRẠNG\nDU LỊCH NÔNG NGHIỆP XANH\nTẠI XÃ CỦ CHI",
        fc="#DFF3E3",
        ec="#1B5E20",
        size=10.2,
        weight="bold",
    )

    arrow(ax, (0.5, 0.43), (0.5, 0.36), color="#455A64", lw=1.6)
    output_items = [
        (0.23, "Tiềm năng\nvà lợi thế", "#E8F5E9", "#2E7D32"),
        (0.50, "Hạn chế\nvà nguyên nhân", "#FBE9E7", "#D84315"),
        (0.77, "Giải pháp SMART\nđến năm 2030", "#EAF2FF", "#0D47A1"),
    ]
    for x, text, fc, ec in output_items:
        box(ax, (x, 0.29), 0.22, 0.11, text, fc=fc, ec=ec, size=9.6, weight="bold")

    box(
        ax,
        (0.5, 0.13),
        0.78,
        0.075,
        "Logic nghiên cứu: Cơ sở lý luận → Đánh giá thực trạng → Nhận diện nguyên nhân → Đề xuất mô hình và lộ trình",
        fc="#FAFAFA",
        ec="#757575",
        size=8.9,
    )

    ax.text(
        0.5,
        0.035,
        "Nguồn: Tác giả xây dựng, 2026.",
        ha="center",
        fontsize=10,
        style="italic",
        transform=ax.transAxes,
    )

    return save(fig, "hinh_1_1_khung_phan_tich.png")


def draw_bieudo_2_1():
    years = ["2022", "2023", "2024", "6T/2025"]
    visitors = np.array([45, 68, 95, 55])  # nghìn lượt
    revenue = np.array([85, 132, 210, 135])  # tỷ VND
    x = np.arange(len(years))

    fig, ax1 = plt.subplots(figsize=(12.8, 7.2))
    bars = ax1.bar(x, visitors, width=0.52, color="#2E7D32", label="Lượng khách")
    ax1.set_ylabel("Lượng khách du lịch nông nghiệp (nghìn lượt)", fontsize=10.5)
    ax1.set_ylim(0, 115)
    ax1.set_xticks(x)
    ax1.set_xticklabels(years, fontsize=10.5)
    ax1.grid(axis="y", linestyle="--", alpha=0.35)

    ax2 = ax1.twinx()
    ax2.plot(x, revenue, color="#1565C0", marker="o", linewidth=2.6, label="Doanh thu")
    ax2.set_ylabel("Doanh thu ước tính (tỷ VND)", fontsize=10.5)
    ax2.set_ylim(0, 250)

    for bar, value in zip(bars, visitors):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 3,
            f"{value:.0f}",
            ha="center",
            fontsize=10,
            color="#1B5E20",
            fontweight="bold",
        )
    for xi, value in zip(x, revenue):
        ax2.text(
            xi,
            value + 8,
            f"{value:.0f}",
            ha="center",
            fontsize=10,
            color="#0D47A1",
            fontweight="bold",
        )

    legend_items = [
        Line2D([0], [0], color="#2E7D32", lw=8, label="Lượng khách (nghìn lượt)"),
        Line2D([0], [0], color="#1565C0", lw=2.6, marker="o", label="Doanh thu (tỷ VND)"),
    ]
    ax1.legend(handles=legend_items, loc="upper left", frameon=False)

    fig.suptitle(
        "Biểu đồ 2.1. Lượng khách và doanh thu du lịch nông nghiệp tại Củ Chi giai đoạn 2022-6T/2025",
        fontsize=13.2,
        fontweight="bold",
        y=0.98,
    )
    ax1.text(
        0.5,
        -0.16,
        "Nguồn: Tổng hợp từ Sở Du lịch TP.HCM (2025), UBND huyện Củ Chi (2025) và khảo sát sơ cấp của tác giả.",
        ha="center",
        fontsize=9.4,
        style="italic",
        transform=ax1.transAxes,
    )

    fig.tight_layout(rect=[0, 0.02, 1, 0.94])
    return save(fig, "bieudo_2_1_luong_khach_doanh_thu.png")


def draw_bieudo_2_2():
    labels = [
        "Quản lý bền vững",
        "Lợi ích kinh tế - xã hội",
        "Bảo tồn văn hóa",
        "Bảo vệ môi trường",
    ]
    values = [2.8, 3.2, 3.5, 2.4]
    colors = ["#FFA726", "#66BB6A", "#43A047", "#EF5350"]

    fig, ax = plt.subplots(figsize=(12.2, 6.6))
    y = np.arange(len(labels))
    bars = ax.barh(y, values, color=colors, height=0.56)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=10.6)
    ax.invert_yaxis()
    ax.set_xlim(0, 5)
    ax.set_xlabel("Mức độ đạt theo thang điểm 1-5", fontsize=10.5)
    ax.grid(axis="x", linestyle="--", alpha=0.35)
    ax.axvline(4.0, color="#0D47A1", linestyle="--", linewidth=1.4)
    ax.text(4.03, -0.62, "Mức mục tiêu tốt", color="#0D47A1", fontsize=9.5)

    for bar, value in zip(bars, values):
        ax.text(
            value + 0.06,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.1f}",
            va="center",
            fontsize=10.5,
            fontweight="bold",
        )

    fig.suptitle(
        "Biểu đồ 2.2. Mức độ đạt tiêu chí du lịch xanh theo GSTC tại Củ Chi",
        fontsize=13.2,
        fontweight="bold",
        y=0.97,
    )
    ax.text(
        0.5,
        -0.17,
        "Nguồn: Khảo sát sơ cấp 150-200 mẫu, 2025.",
        ha="center",
        fontsize=9.8,
        style="italic",
        transform=ax.transAxes,
    )

    fig.tight_layout(rect=[0, 0.04, 1, 0.92])
    return save(fig, "bieudo_2_2_muc_do_gstc.png")


def draw_so_do_2_1():
    fig, ax = plt.subplots(figsize=(14, 8.8))
    clean(ax)
    ax.text(
        0.5,
        0.965,
        "Sơ đồ 2.1. Nguyên nhân gốc rễ khiến du lịch nông nghiệp xanh chưa phát triển tương xứng",
        ha="center",
        va="top",
        fontsize=13.6,
        fontweight="bold",
        transform=ax.transAxes,
    )

    box(
        ax,
        (0.78, 0.50),
        0.31,
        0.19,
        "KẾT QUẢ VẤN ĐỀ\n\nDu lịch nông nghiệp xanh\nchưa phát triển tương xứng\nvới tiềm năng Củ Chi",
        fc="#FBE9E7",
        ec="#D84315",
        size=9.3,
        weight="bold",
    )

    causes = [
        (0.28, 0.80, "Quy hoạch và chính sách", "Quy hoạch xanh chưa cụ thể\nCơ chế ưu đãi còn chung", "#E3F2FD", "#1565C0", 0.64),
        (0.28, 0.64, "Hạ tầng và đầu tư", "Thiếu xử lý nước thải\nThiếu vốn dài hạn, PPP", "#E8F5E9", "#2E7D32", 0.57),
        (0.28, 0.48, "Nhân lực và nhận thức", "Thiếu kỹ năng dịch vụ\nTư duy khai thác ngắn hạn", "#FFF3E0", "#EF6C00", 0.50),
        (0.28, 0.32, "Liên kết chuỗi và marketing", "Hộ kinh doanh rời rạc\nThiếu thương hiệu riêng", "#F3E5F5", "#7B1FA2", 0.43),
        (0.28, 0.16, "Môi trường và quản lý xanh", "Rác thải, nước thải phổ biến\nThiếu giám sát theo GSTC", "#FBE9E7", "#D84315", 0.36),
    ]

    for x, y, title, detail, fc, ec, target_y in causes:
        box(ax, (x, y), 0.39, 0.105, f"{title}\n{detail}", fc=fc, ec=ec, size=8.4, weight="bold")
        arrow(ax, (x + 0.205, y), (0.615, target_y), color=ec, lw=1.2, mutation=10)

    ax.text(
        0.5,
        0.045,
        "Nguồn: Tác giả tổng hợp từ phân tích Root Cause tại Chương 2, 2026.",
        ha="center",
        fontsize=9.8,
        style="italic",
        transform=ax.transAxes,
    )

    return save(fig, "so_do_2_1_fishbone_nguyen_nhan.png")


def draw_hinh_3_1():
    fig, ax = plt.subplots(figsize=(14, 9.0))
    clean(ax)
    ax.text(
        0.5,
        0.965,
        'Hình 3.1. Mô hình phát triển "Củ Chi Green Agri-Tourism Hub"',
        ha="center",
        va="top",
        fontsize=13.8,
        fontweight="bold",
        transform=ax.transAxes,
    )

    layers = [
        (
            0.76,
            "VÒNG LÕI: DI SẢN VÀ TRẢI NGHIỆM NÔNG NGHIỆP",
            "#E8F5E9",
            "#2E7D32",
            [
                ("Địa đạo Củ Chi\nkể chuyện AR/VR", "#FFF3E0", "#EF6C00"),
                ("Nông trại\ntrải nghiệm", "#E8F5E9", "#2E7D32"),
                ("Canh tác hữu cơ\ngiáo dục xanh", "#E8F5E9", "#2E7D32"),
            ],
        ),
        (
            0.52,
            "VÒNG GIỮA: DỊCH VỤ HỖ TRỢ VÀ SẢN PHẨM ĐỊA PHƯƠNG",
            "#FFF8E1",
            "#F9A825",
            [
                ("Homestay xanh", "#FFFDE7", "#F9A825"),
                ("Ẩm thực địa phương", "#FFFDE7", "#F9A825"),
                ("OCOP\nworkshop sản phẩm", "#F3E5F5", "#7B1FA2"),
            ],
        ),
        (
            0.28,
            "VÒNG NGOÀI: QUẢN TRỊ, LIÊN KẾT VÀ NỀN TẢNG SỐ",
            "#EAF2FF",
            "#0D47A1",
            [
                ("Chính quyền\nquy hoạch, GSTC", "#E3F2FD", "#1565C0"),
                ("Doanh nghiệp\nlữ hành", "#E0F7FA", "#00838F"),
                ("Cộng đồng\nhộ dân, HTX", "#F1F8E9", "#558B2F"),
                ("Green Hub số\nđặt chỗ, QR, dữ liệu", "#EAF2FF", "#0D47A1"),
            ],
        ),
    ]

    for y, title, layer_fc, layer_ec, items in layers:
        box(ax, (0.5, y + 0.075), 0.84, 0.055, title, fc=layer_fc, ec=layer_ec, size=9.4, weight="bold")
        xs = np.linspace(0.19, 0.81, len(items))
        for x, (text, fc, ec) in zip(xs, items):
            box(ax, (x, y - 0.02), 0.18, 0.085, text, fc=fc, ec=ec, size=8.4, weight="bold")

    arrow(ax, (0.5, 0.66), (0.5, 0.60), color="#455A64", lw=1.4, mutation=11)
    arrow(ax, (0.5, 0.42), (0.5, 0.36), color="#455A64", lw=1.4, mutation=11)
    box(
        ax,
        (0.5, 0.11),
        0.78,
        0.08,
        "Kết quả kỳ vọng: tăng thu nhập cộng đồng | giảm rác thải nhựa | đa dạng sản phẩm | xây dựng thương hiệu xanh đến 2030",
        fc="#FAFAFA",
        ec="#616161",
        size=8.6,
        weight="bold",
    )

    ax.text(
        0.5,
        0.035,
        "Nguồn: Tác giả đề xuất, 2026.",
        ha="center",
        fontsize=9.8,
        style="italic",
        transform=ax.transAxes,
    )

    return save(fig, "hinh_3_1_cu_chi_green_agri_tourism_hub.png")


def draw_bieudo_3_1():
    fig, ax = plt.subplots(figsize=(14, 8.6))
    clean(ax)
    ax.text(
        0.5,
        0.965,
        "Biểu đồ 3.1. Lộ trình phát triển du lịch nông nghiệp xanh Củ Chi giai đoạn 2026-2030",
        ha="center",
        va="top",
        fontsize=13.6,
        fontweight="bold",
        transform=ax.transAxes,
    )

    years = ["2026", "2027", "2028", "2029", "2030"]
    notes = [
        "Hoàn thiện quy hoạch\nthành lập Ban quản lý",
        "Hạ tầng xanh\nrác thải nhựa giảm 50%",
        "5-7 mô hình thí điểm\n300 người được đào tạo",
        "Mở rộng Green Farm\nHomestay xanh, OCOP",
        "Thương hiệu xanh\n300.000 khách/năm\n800-1.000 tỷ VND",
    ]
    xs = np.linspace(0.10, 0.90, len(years))
    yline = 0.55
    ax.plot([xs[0], xs[-1]], [yline, yline], color="#2E7D32", linewidth=3.0, transform=ax.transAxes)

    for idx, (x, year, note) in enumerate(zip(xs, years, notes)):
        ax.add_patch(Circle((x, yline), 0.038, facecolor="#DFF3E3", edgecolor="#1B5E20", linewidth=1.5, transform=ax.transAxes))
        ax.text(x, yline, year, ha="center", va="center", fontsize=10.2, fontweight="bold", transform=ax.transAxes)
        if idx % 2 == 0:
            by = 0.79
            arrow(ax, (x, yline + 0.04), (x, by - 0.08), color="#2E7D32", lw=1.25, mutation=10)
        else:
            by = 0.33
            arrow(ax, (x, yline - 0.04), (x, by + 0.08), color="#2E7D32", lw=1.25, mutation=10)
        box(ax, (x, by), 0.17, 0.13, note, fc="#F7FBF7", ec="#2E7D32", size=8.35)

    box(
        ax,
        (0.5, 0.13),
        0.74,
        0.065,
        "Mục tiêu theo dõi: hài lòng du khách >85% | số hộ đạt chuẩn xanh >70% | khách tăng 2-3 lần so với hiện nay",
        fc="#EAF2FF",
        ec="#0D47A1",
        size=8.5,
        weight="bold",
    )
    ax.text(
        0.5,
        0.035,
        "Nguồn: Tác giả tổng hợp từ mục tiêu và lộ trình Chương 3, 2026.",
        ha="center",
        fontsize=9.8,
        style="italic",
        transform=ax.transAxes,
    )

    return save(fig, "bieudo_3_1_lo_trinh_2026_2030.png")


def write_markdown(paths):
    rel = lambda p: "../../figures/" + p.name
    md = f"""# Bộ 6 hình/biểu đồ minh họa cho đề tài Củ Chi

**Đề tài:** Đánh giá thực trạng phát triển du lịch nông nghiệp theo hướng du lịch xanh tại xã Củ Chi, TP.HCM.

File này dùng để xem nhanh 6 hình/biểu đồ cần chèn vào bài. Mỗi mục bên dưới có vị trí chèn, hình, nguồn và đoạn nhận xét gợi ý.

## Danh sách hình/biểu đồ

| STT | Tên hình/biểu đồ | Vị trí chèn |
|---|---|---|
| 1 | Hình 1.1. Khung phân tích phát triển du lịch nông nghiệp xanh tại xã Củ Chi | Chương 1, sau mục 1.7 |
| 2 | Biểu đồ 2.1. Lượng khách và doanh thu du lịch nông nghiệp tại Củ Chi giai đoạn 2022-6T/2025 | Chương 2, sau Bảng 2.1 |
| 3 | Biểu đồ 2.2. Mức độ đạt tiêu chí du lịch xanh theo GSTC tại Củ Chi | Chương 2, sau Bảng 2.2 |
| 4 | Sơ đồ 2.1. Nguyên nhân gốc rễ khiến du lịch nông nghiệp xanh chưa phát triển tương xứng | Chương 2, mục 2.6 |
| 5 | Hình 3.1. Mô hình phát triển “Củ Chi Green Agri-Tourism Hub” | Chương 3, sau phần mô hình đề xuất |
| 6 | Biểu đồ 3.1. Lộ trình phát triển du lịch nông nghiệp xanh Củ Chi giai đoạn 2026-2030 | Chương 3, sau Bảng 3.2 hoặc cuối mục 3.4 |

---

## 1. Hình 1.1. Khung phân tích phát triển du lịch nông nghiệp xanh tại xã Củ Chi

**Vị trí chèn:** Chương 1, sau mục **1.7. Khung lý thuyết nghiên cứu và khoảng trống nghiên cứu**.

![Hình 1.1]({rel(paths['hinh_1_1'])})

*Nguồn: Tác giả xây dựng, 2026.*

**Nhận xét:**  
Hình 1.1 thể hiện logic phân tích của đề tài, bắt đầu từ cơ sở lý luận về phát triển bền vững, tiêu chí GSTC, SWOT/PESTLE, chuỗi giá trị du lịch và quản trị dịch vụ. Các khung này được sử dụng để đánh giá thực trạng phát triển du lịch nông nghiệp xanh tại xã Củ Chi, từ đó nhận diện tiềm năng, hạn chế, nguyên nhân gốc rễ và đề xuất giải pháp SMART đến năm 2030.

---

## 2. Biểu đồ 2.1. Lượng khách và doanh thu du lịch nông nghiệp tại Củ Chi giai đoạn 2022-6T/2025

**Vị trí chèn:** Chương 2, ngay sau **Bảng 2.1. Thống kê lượng khách và doanh thu du lịch nông nghiệp tại Củ Chi**.

![Biểu đồ 2.1]({rel(paths['bieudo_2_1'])})

*Nguồn: Tổng hợp từ Sở Du lịch TP.HCM (2025), UBND huyện Củ Chi (2025) và khảo sát sơ cấp của tác giả.*

**Nhận xét:**  
Biểu đồ 2.1 cho thấy lượng khách và doanh thu du lịch nông nghiệp tại Củ Chi có xu hướng tăng trong giai đoạn 2022-2024. Lượng khách tăng từ 45.000 lượt năm 2022 lên 95.000 lượt năm 2024, trong khi doanh thu ước tính tăng từ 85 tỷ đồng lên 210 tỷ đồng. Số liệu 6 tháng đầu năm 2025 đạt 55.000 lượt khách và 135 tỷ đồng, cho thấy dư địa tăng trưởng còn lớn nếu địa phương phát triển sản phẩm xanh bài bản hơn.

---

## 3. Biểu đồ 2.2. Mức độ đạt tiêu chí du lịch xanh theo GSTC tại Củ Chi

**Vị trí chèn:** Chương 2, sau **Bảng 2.2. Đánh giá mức độ đạt tiêu chí du lịch xanh**.

![Biểu đồ 2.2]({rel(paths['bieudo_2_2'])})

*Nguồn: Khảo sát sơ cấp 150-200 mẫu, 2025.*

**Nhận xét:**  
Biểu đồ 2.2 cho thấy mức độ phát triển theo hướng du lịch xanh tại Củ Chi còn chưa đồng đều. Tiêu chí bảo tồn văn hóa đạt mức khá với 3,5 điểm nhờ khả năng kết hợp với di sản lịch sử Địa đạo Củ Chi. Tuy nhiên, bảo vệ môi trường chỉ đạt 2,4 điểm và quản lý bền vững đạt 2,8 điểm, phản ánh hạn chế về xử lý rác thải, nước thải, quy hoạch dài hạn và giám sát tiêu chí xanh.

---

## 4. Sơ đồ 2.1. Nguyên nhân gốc rễ khiến du lịch nông nghiệp xanh chưa phát triển tương xứng

**Vị trí chèn:** Chương 2, mục **2.6. Phân tích sâu nguyên nhân gốc rễ của các điểm yếu**.

![Sơ đồ 2.1]({rel(paths['so_do_2_1'])})

*Nguồn: Tác giả tổng hợp từ phân tích Root Cause tại Chương 2, 2026.*

**Nhận xét:**  
Sơ đồ 2.1 cho thấy các hạn chế của du lịch nông nghiệp xanh tại xã Củ Chi không xuất phát từ một nguyên nhân đơn lẻ, mà từ sự kết hợp của nhiều điểm nghẽn. Nổi bật là quy hoạch xanh chưa cụ thể, hạ tầng xử lý môi trường còn thiếu, nhân lực địa phương chưa được đào tạo chuyên nghiệp, liên kết chuỗi và marketing yếu, cùng với việc thiếu hệ thống giám sát bền vững theo tiêu chí GSTC. Đây là cơ sở để xây dựng nhóm giải pháp tương ứng ở Chương 3.

---

## 5. Hình 3.1. Mô hình phát triển “Củ Chi Green Agri-Tourism Hub”

**Vị trí chèn:** Chương 3, sau đoạn **Mô hình đề xuất: “Củ Chi Green Agri-Tourism Hub”**.

![Hình 3.1]({rel(paths['hinh_3_1'])})

*Nguồn: Tác giả đề xuất, 2026.*

**Nhận xét:**  
Hình 3.1 đề xuất mô hình phát triển du lịch nông nghiệp xanh tại xã Củ Chi theo cấu trúc trung tâm tích hợp. Vòng lõi tập trung vào Địa đạo Củ Chi, nông trại trải nghiệm và canh tác hữu cơ; vòng giữa phát triển homestay xanh, ẩm thực địa phương và sản phẩm OCOP; vòng ngoài kết nối chính quyền, doanh nghiệp lữ hành, cộng đồng và nền tảng Green Hub số. Mô hình này giúp liên kết lợi thế lịch sử với tài nguyên nông nghiệp, đồng thời tạo cơ chế quản trị và marketing thống nhất.

---

## 6. Biểu đồ 3.1. Lộ trình phát triển du lịch nông nghiệp xanh Củ Chi giai đoạn 2026-2030

**Vị trí chèn:** Chương 3, sau **Bảng 3.2. Lộ trình thực hiện chi tiết** hoặc cuối mục **3.4. Lộ trình thực hiện và cơ chế phối hợp**.

![Biểu đồ 3.1]({rel(paths['bieudo_3_1'])})

*Nguồn: Tác giả tổng hợp từ mục tiêu và lộ trình Chương 3, 2026.*

**Nhận xét:**  
Biểu đồ 3.1 thể hiện lộ trình triển khai giải pháp theo từng mốc từ năm 2026 đến năm 2030. Giai đoạn đầu tập trung hoàn thiện quy hoạch, thành lập ban quản lý, đầu tư hạ tầng xanh và đào tạo nguồn nhân lực. Đến năm 2028, mục tiêu là hình thành 5-7 mô hình thí điểm và đào tạo 300 người dân. Giai đoạn 2029-2030 tập trung mở rộng Green Farm, homestay xanh, OCOP và xây dựng thương hiệu Củ Chi Green Agri-Tourism với mục tiêu 300.000 lượt khách/năm, doanh thu 800-1.000 tỷ đồng và tỷ lệ hài lòng trên 85%.

---

## Ghi chú sử dụng

- Khi chèn vào Word, đặt hình ở giữa trang, caption và nguồn nằm bên dưới hình.
- Không cần thêm nhiều hình hơn 6 hình này, vì các hình đã bao phủ đủ: khung lý luận, thực trạng số liệu, tiêu chí xanh, nguyên nhân gốc rễ, mô hình đề xuất và lộ trình.
- Nếu sửa số liệu trong bài, chạy lại script `dir tôi/scripts/ve_6_hinh_cu_chi.py` để cập nhật toàn bộ ảnh và file Markdown này.
"""
    (MD_DIR / "00_6_hinh_bieu_do_minh_hoa.md").write_text(md, encoding="utf-8")

    index = """# Hình Biểu Đồ

Các file trong phần này:

- [Bộ 6 hình/biểu đồ minh họa cho đề tài Củ Chi](00_6_hinh_bieu_do_minh_hoa.md)
"""
    (MD_DIR / "00_INDEX.md").write_text(index, encoding="utf-8")


def update_main_index():
    index_path = BASE_DIR / "markdown" / "00_INDEX.md"
    text = index_path.read_text(encoding="utf-8")
    block = """\n## 04_hinh_bieu_do\n- [Bộ 6 hình/biểu đồ minh họa cho đề tài Củ Chi](04_hinh_bieu_do/00_6_hinh_bieu_do_minh_hoa.md)\n"""
    if "## 04_hinh_bieu_do" not in text:
        index_path.write_text(text.rstrip() + "\n" + block + "\n", encoding="utf-8")


def main():
    paths = {
        "hinh_1_1": draw_hinh_1_1(),
        "bieudo_2_1": draw_bieudo_2_1(),
        "bieudo_2_2": draw_bieudo_2_2(),
        "so_do_2_1": draw_so_do_2_1(),
        "hinh_3_1": draw_hinh_3_1(),
        "bieudo_3_1": draw_bieudo_3_1(),
    }
    write_markdown(paths)
    update_main_index()
    print("Đã tạo 6 hình/biểu đồ:")
    for path in paths.values():
        print(f"- {path.relative_to(BASE_DIR)}")
    print("- markdown/04_hinh_bieu_do/00_6_hinh_bieu_do_minh_hoa.md")


if __name__ == "__main__":
    main()
