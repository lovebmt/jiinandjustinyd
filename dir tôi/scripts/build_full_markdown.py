from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[2]
MY_DIR = ROOT / "dir tôi"
MARKDOWN_DIR = MY_DIR / "markdown"
ASSET_DIR = ROOT / "assets" / "figures"
OUT_FILE = ROOT / "luan_van_full.md"

ASSET_DIR.mkdir(parents=True, exist_ok=True)

FIGURES = {
    "hinh_1_1": "hinh_1_1_khung_phan_tich.png",
    "bieudo_2_1": "bieudo_2_1_luong_khach_doanh_thu.png",
    "bieudo_2_2": "bieudo_2_2_muc_do_gstc.png",
    "so_do_2_1": "so_do_2_1_fishbone_nguyen_nhan.png",
    "hinh_3_1": "hinh_3_1_cu_chi_green_agri_tourism_hub.png",
    "bieudo_3_1": "bieudo_3_1_lo_trinh_2026_2030.png",
}

for filename in FIGURES.values():
    src = MY_DIR / "figures" / filename
    dst = ASSET_DIR / filename
    if src.exists():
        shutil.copy2(src, dst)


SECTIONS = [
    "00_mo_dau/00_mo_dau.md",
    "00_mo_dau/1_1_ly_do_chon_de_tai.md",
    "00_mo_dau/1_2_tinh_hinh_nghien_cuu_trong_va_ngoai_nuoc.md",
    "00_mo_dau/1_3_muc_tieu_nghien_cuu.md",
    "00_mo_dau/1_4_doi_tuong_va_pham_vi_nghien_cuu.md",
    "00_mo_dau/1_5_cau_hoi_nghien_cuu.md",
    "00_mo_dau/1_6_phuong_phap_nghien_cuu.md",
    "00_mo_dau/1_7_y_nghia_khoa_hoc_va_thuc_tien.md",
    "00_mo_dau/1_8_cau_truc_khoa_luan.md",
    "01_chuong_1/00_chuong_1_co_so_ly_luan_va_khung_ly_thuyet.md",
    "01_chuong_1/1_1_cac_khai_niem_co_ban.md",
    "01_chuong_1/1_2_dac_diem_va_tieu_chi_danh_gia_du_lich_nong_nghiep_theo_huong_du_lich_xanh.md",
    "01_chuong_1/1_3_cac_mo_hinh_thanh_cong_tren_the_gioi_va_viet_nam.md",
    "01_chuong_1/1_3_1_mo_hinh_agriturismo_y.md",
    "01_chuong_1/1_3_2_mo_hinh_green_tourism_nhat_ban.md",
    "01_chuong_1/1_3_3_mo_hinh_otop_gan_du_lich_cong_dong_thai_lan.md",
    "01_chuong_1/1_3_4_mo_hinh_farm_stay_regenerative_agritourism_my_california_new_zealand.md",
    "01_chuong_1/1_3_5_mo_hinh_lang_rau_tra_que_quang_nam.md",
    "01_chuong_1/1_3_6_mo_hinh_du_lich_cong_dong_thieng_lieng_can_gio_tp_hcm.md",
    "01_chuong_1/1_3_7_mo_hinh_vuon_trai_cay_va_du_lich_sinh_thai_cac_tinh_dong_bang_song_cuu_long.md",
    "01_chuong_1/1_3_8_mo_hinh_du_lich_nong_nghiep_cong_nghe_cao_da_lat_lam_dong.md",
    "01_chuong_1/1_4_so_sanh_cac_mo_hinh.md",
    "01_chuong_1/1_5_mo_hinh_de_xuat_phu_hop_cho_xa_cu_chi.md",
    "01_chuong_1/1_6_cac_ly_thuyet_va_khung_phan_tich_lien_quan.md",
    "01_chuong_1/1_7_khung_ly_thuyet_nghien_cuu_va_khoang_trong_nghien_cuu.md",
    "FIGURE:hinh_1_1",
    "01_chuong_1/1_8_bai_hoc_kinh_nghiem_rut_ra_cho_xa_cu_chi.md",
    "02_chuong_2/00_chuong_2_thuc_trang.md",
    "02_chuong_2/2_1_tong_quan_ve_xa_cu_chi.md",
    "02_chuong_2/2_2_thuc_trang_phat_trien_du_lich_nong_nghiep.md",
    "FIGURE:bieudo_2_1",
    "02_chuong_2/2_3_danh_gia_muc_do_phat_trien_theo_huong_du_lich_xanh.md",
    "FIGURE:bieudo_2_2",
    "02_chuong_2/2_4_phan_tich_swot.md",
    "02_chuong_2/2_5_danh_gia_tong_quat_diem_manh_diem_yeu.md",
    "02_chuong_2/2_6_phan_tich_sau_nguyen_nhan_goc_re_cua_cac_diem_yeu.md",
    "FIGURE:so_do_2_1",
    "02_chuong_2/99_tai_lieu_tham_khao.md",
    "03_chuong_3/00_chuong_3_giai_phap.md",
    "03_chuong_3/3_1_quan_diem_dinh_huong_va_muc_tieu_phat_trien.md",
    "03_chuong_3/3_2_giai_phap_chung_tu_phia_nha_nuoc_va_chinh_quyen_dia_phuong.md",
    "03_chuong_3/3_3_giai_phap_cu_the_tu_goc_nhin_quan_tri_dich_vu_du_lich_va_lu_hanh.md",
    "03_chuong_3/3_3_1_giai_phap_ve_quy_hoach_va_quan_ly_nha_nuoc.md",
    "03_chuong_3/3_3_2_giai_phap_ve_ha_tang_va_bao_ve_moi_truong.md",
    "03_chuong_3/3_3_3_giai_phap_ve_phat_trien_san_pham_va_dich_vu_du_lich.md",
    "03_chuong_3/3_3_4_giai_phap_ve_nguon_nhan_luc_va_nang_cao_nhan_thuc_cong_dong.md",
    "03_chuong_3/3_3_5_giai_phap_ve_marketing_lien_ket_va_xuc_tien_du_lich.md",
    "03_chuong_3/3_3_6_giai_phap_ve_quan_tri_dich_vu_va_chat_luong_trai_nghiem_khach_hang.md",
    "FIGURE:hinh_3_1",
    "03_chuong_3/3_4_lo_trinh_thuc_hien_va_co_che_phoi_hop.md",
    "FIGURE:bieudo_3_1",
    "03_chuong_3/3_5_cac_dieu_kien_bao_dam_thuc_hien_giai_phap.md",
    "03_chuong_3/99_tai_lieu_tham_khao.md",
]


CAPTIONS = {
    "hinh_1_1": (
        "Hình 1.1. Khung phân tích phát triển du lịch nông nghiệp xanh tại xã Củ Chi",
        "Nguồn: Tác giả xây dựng, 2026.",
    ),
    "bieudo_2_1": (
        "Biểu đồ 2.1. Lượng khách và doanh thu du lịch nông nghiệp tại Củ Chi giai đoạn 2022-6T/2025",
        "Nguồn: Tổng hợp từ Sở Du lịch TP.HCM (2025), UBND huyện Củ Chi (2025) và khảo sát sơ cấp của tác giả.",
    ),
    "bieudo_2_2": (
        "Biểu đồ 2.2. Mức độ đạt tiêu chí du lịch xanh theo GSTC tại Củ Chi",
        "Nguồn: Khảo sát sơ cấp 150-200 mẫu, 2025.",
    ),
    "so_do_2_1": (
        "Sơ đồ 2.1. Nguyên nhân gốc rễ khiến du lịch nông nghiệp xanh chưa phát triển tương xứng",
        "Nguồn: Tác giả tổng hợp từ phân tích Root Cause tại Chương 2, 2026.",
    ),
    "hinh_3_1": (
        "Hình 3.1. Mô hình phát triển Củ Chi Green Agri-Tourism Hub",
        "Nguồn: Tác giả đề xuất, 2026.",
    ),
    "bieudo_3_1": (
        "Biểu đồ 3.1. Lộ trình phát triển du lịch nông nghiệp xanh Củ Chi giai đoạn 2026-2030",
        "Nguồn: Tác giả tổng hợp từ mục tiêu và lộ trình Chương 3, 2026.",
    ),
}


def read_section(relative_path: str) -> str:
    path = MARKDOWN_DIR / relative_path
    if not path.exists():
        return f"\n> Thiếu file: `{relative_path}`\n"
    return path.read_text(encoding="utf-8").strip()


def figure_block(key: str) -> str:
    filename = FIGURES[key]
    caption, source = CAPTIONS[key]
    return f"""### {caption}

![{caption}](assets/figures/{filename})

*{source}*
"""


parts = [
    Path("cover.md").read_text(encoding="utf-8").strip(),
    "\n---\n",
    "# Nội dung bài luận",
    "\n> Bản Markdown tổng hợp từ các file đã tách trong `dir tôi/markdown/`, kèm 6 hình/biểu đồ minh họa đã tạo.\n",
]

for item in SECTIONS:
    if item.startswith("FIGURE:"):
        parts.append(figure_block(item.split(":", 1)[1]))
    else:
        parts.append(read_section(item))

OUT_FILE.write_text("\n\n---\n\n".join(parts).strip() + "\n", encoding="utf-8")
print(f"Đã tạo {OUT_FILE.relative_to(ROOT)}")
print(f"Đã copy {len(list(ASSET_DIR.glob('*.png')))} ảnh vào {ASSET_DIR.relative_to(ROOT)}")
