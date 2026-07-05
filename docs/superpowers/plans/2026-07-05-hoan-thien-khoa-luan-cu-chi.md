# Hoan Thien Khoa Luan Cu Chi Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hoan thien ban khoa luan de co du trang bia, muc luc, danh muc, hinh/bieu do, ket luan va tai lieu tham khao truoc khi nop.

**Architecture:** Lay `docs/JTyd_6570.docx` lam ban Word hien tai can hoan thien. Dung mau bia tu `docs/Do an-Khoa luan tot nghiep/[CA NHAN] Trang bia, lot bia_DA_KLTN.docx`, chen 6 hinh co san trong `assets/figures/`, va doi chieu voi nguon Markdown `luan_van_full.md` khi can kiem noi dung.

**Tech Stack:** Microsoft Word/docx, `textutil`, `unzip`, Markdown sources, PNG figure assets.

## Global Constraints

- Khong dung bo mau `docs/Thuc tap tot nghiep/` vi day la khoa luan/do an tot nghiep, khong phai thuc tap tot nghiep.
- Giu nguyen noi dung hoc thuat da co, chi bo sung cac phan thieu va sua loi dinh dang/chinh ta lien quan.
- Ban Word hien tai `docs/JTyd_6570.docx` chua co media nhung co cac nhan "Hinh/Bieu do"; can chen hinh that vao Word.
- Tieu de `TÀI LIỆU THAM HẢO` trong Word hien tai phai sua thanh `TÀI LIỆU THAM KHẢO`.

---

### Task 1: Xac nhan file lam viec va thu tu phan bat buoc

**Files:**
- Read: `docs/JTyd_6570.docx`
- Read: `docs/Do an-Khoa luan tot nghiep/[CA NHAN] Trang bia, lot bia_DA_KLTN.docx`
- Read: `luan_van_full.md`
- Produce: checklist xac nhan trong ghi chu lam viec hoac final handoff

**Interfaces:**
- Consumes: cac file Word/Markdown hien co.
- Produces: thu tu phan can co trong ban nop.

- [ ] **Step 1: Kiem tra Word co hinh chua**

Run:

```bash
unzip -l 'docs/JTyd_6570.docx' | rg 'word/media'
```

Expected: hien tai khong co ket qua, nghia la chua chen hinh vao file Word.

- [ ] **Step 2: Kiem tra cac phan dau/cuoi trong Word**

Run:

```bash
textutil -convert txt -stdout 'docs/JTyd_6570.docx' | rg -n 'MỤC LỤC|DANH MỤC|Kết luận|TÀI LIỆU THAM|viết tắt'
```

Expected current status: co `Kết luận`, co `TÀI LIỆU THAM HẢO` sai chinh ta/placeholder, chua thay `MỤC LỤC`, `DANH MỤC BẢNG`, `DANH MỤC HÌNH`, `DANH MỤC TỪ VIẾT TẮT`.

- [ ] **Step 3: Chot thu tu phan can co**

Required order:

```text
1. Trang bìa chính - bìa màu cứng theo file mẫu
2. Trang phụ bìa theo file mẫu
3. Lời cam đoan hoặc lời cảm ơn nếu trường/GVHD yêu cầu
4. Mục lục
5. Danh mục bảng
6. Danh mục hình
7. Danh mục từ viết tắt
8. Mở đầu
9. Chương 1
10. Chương 2
11. Chương 3
12. Kết luận
13. Tài liệu tham khảo
14. Phụ lục
```

### Task 2: Chen trang bia chinh va trang phu bia tu mau khoa luan

**Files:**
- Read: `docs/Do an-Khoa luan tot nghiep/[CA NHAN] Trang bia, lot bia_DA_KLTN.docx`
- Modify: `docs/JTyd_6570.docx`

**Interfaces:**
- Consumes: mau bia ca nhan DA/KLTN.
- Produces: Word co 2 trang bia truoc phan `MỞ ĐẦU`.

- [ ] **Step 1: Mo file mau bia ca nhan**

Use file:

```text
docs/Do an-Khoa luan tot nghiep/[CA NHAN] Trang bia, lot bia_DA_KLTN.docx
```

- [ ] **Step 2: Dien thong tin de tai vao 2 trang bia**

Use title:

```text
ĐÁNH GIÁ THỰC TRẠNG PHÁT TRIỂN DU LỊCH NÔNG NGHIỆP THEO HƯỚNG DU LỊCH XANH TẠI XÃ CỦ CHI, TP.HCM
```

Keep the template fields:

```text
TRƯỜNG ĐẠI HỌC CÔNG NGHỆ TP.HCM
VIỆN/CƠ SỞ ĐÀO TẠO theo đúng yêu cầu của sinh viên/GVHD
KHÓA LUẬN TỐT NGHIỆP
Ngành
Chuyên ngành
Giảng viên hướng dẫn
Sinh viên thực hiện
MSSV
Lớp
TP. Hồ Chí Minh, 2026
```

- [ ] **Step 3: Dat trang bia chinh va phu bia truoc `MỞ ĐẦU`**

Expected: `MỞ ĐẦU` khong con la trang dau tien cua file Word.

### Task 3: Bo sung muc luc va cac danh muc

**Files:**
- Modify: `docs/JTyd_6570.docx`
- Read: `luan_van_full.md`

**Interfaces:**
- Consumes: heading va caption trong Word/Markdown.
- Produces: front matter day du truoc `MỞ ĐẦU`.

- [ ] **Step 1: Tao `MỤC LỤC` bang heading cua Word**

Expected: Muc luc gom `MỞ ĐẦU`, `CHƯƠNG 1`, `CHƯƠNG 2`, `CHƯƠNG 3`, `Kết luận`, `TÀI LIỆU THAM KHẢO`, `PHỤ LỤC`.

- [ ] **Step 2: Tao `DANH MỤC BẢNG`**

Include captions dang co trong Word, vi du:

```text
Bảng 1.3.2. Tóm tắt bài học chính từ 8 mô hình và khả năng áp dụng tại xã Củ Chi
Bảng 1.4. Hệ thống chỉ số đánh giá du lịch nông nghiệp xanh tại xã Củ Chi
Bảng 2.2.1. Cơ cấu mẫu khảo sát theo giới tính
Bảng 2.2.2. Cơ cấu mẫu khảo sát theo độ tuổi
Bảng 2.2.3. Cơ cấu mẫu khảo sát theo nghề nghiệp
Bảng 2.3.1. Kết quả đánh giá các tiêu chí về môi trường
Bảng 2.3.2. Kết quả đánh giá thực trạng phát triển trên phương diện kinh tế
Bảng 2.3.3. Kết quả đánh giá thực trạng phát triển trên phương diện xã hội - văn hóa
Bảng 2.3.4. Kết quả đánh giá thực trạng phát triển trên phương diện quản trị
```

- [ ] **Step 3: Tao `DANH MỤC HÌNH`**

Include hinh/bieu do can chen:

```text
Hình 1.1. Khung phân tích phát triển du lịch nông nghiệp xanh tại xã Củ Chi
Hình 2.1. Bản đồ vị trí xã Củ Chi trong TP. Hồ Chí Minh
Biểu đồ 2.1. Cơ cấu giới tính
Biểu đồ 2.2.2. Cơ cấu độ tuổi
Biểu đồ 2.2.3. Cơ cấu nghề nghiệp
Hình 2.2.1. Điểm trung bình các tiêu chí thuộc trụ cột môi trường
Biểu đồ 2.3.2. Điểm trung bình các tiêu chí kinh tế
Biểu đồ 2.3.3. Điểm trung bình các tiêu chí xã hội - văn hóa
Biểu đồ 2.3.4. Điểm trung bình các tiêu chí quản trị
```

- [ ] **Step 4: Tao `DANH MỤC TỪ VIẾT TẮT`**

Minimum list to include:

```text
AR/VR: Thực tế tăng cường / Thực tế ảo
GSTC: Global Sustainable Tourism Council
OCOP: One Commune One Product
PPP: Public-Private Partnership
SERVQUAL: Service Quality
SWOT: Strengths, Weaknesses, Opportunities, Threats
TP.HCM: Thành phố Hồ Chí Minh
UBND: Ủy ban nhân dân
UNWTO: United Nations World Tourism Organization
VietGAP: Vietnamese Good Agricultural Practices
```

### Task 4: Chen hinh va bieu do vao Word

**Files:**
- Read: `assets/figures/*.png`
- Modify: `docs/JTyd_6570.docx`

**Interfaces:**
- Consumes: PNG assets da co.
- Produces: Word co hinh that va caption dung vi tri.

- [ ] **Step 1: Chen 6 hinh/bieu do co san**

Use these files:

```text
assets/figures/hinh_1_1_khung_phan_tich.png
assets/figures/bieudo_2_1_luong_khach_doanh_thu.png
assets/figures/bieudo_2_2_muc_do_gstc.png
assets/figures/so_do_2_1_fishbone_nguyen_nhan.png
assets/figures/hinh_3_1_cu_chi_green_agri_tourism_hub.png
assets/figures/bieudo_3_1_lo_trinh_2026_2030.png
```

- [ ] **Step 2: Xu ly cac placeholder chua co file**

Current Word mentions:

```text
Hình 2.1. Bản đồ vị trí xã Củ Chi trong TP. Hồ Chí Minh (chèn bản đồ)
Biểu đồ 2.1: Biểu đồ tròn hoặc cột về cơ cấu giới tính. VẼ BIỂU ĐỒ
Biểu đồ 2.2.2: Biểu đồ cột.
Biểu đồ 2.2.3: Biểu đồ cột.
Hình 2.2.1. Điểm trung bình các tiêu chí thuộc trụ cột môi trường
Biểu đồ 2.3.2. Điểm trung bình các tiêu chí kinh tế
Biểu đồ 2.3.3. Điểm trung bình các tiêu chí xã hội - văn hóa
Biểu đồ 2.3.4. Điểm trung bình các tiêu chí quản trị
```

For each item, either insert a generated chart/map from the survey data or remove the placeholder wording after confirming with the actual content.

- [ ] **Step 3: Verify Word now contains media**

Run:

```bash
unzip -l 'docs/JTyd_6570.docx' | rg 'word/media'
```

Expected: multiple `word/media/image*.png` or `word/media/image*.jpeg` entries.

### Task 5: Hoan thien ket luan va tai lieu tham khao

**Files:**
- Modify: `docs/JTyd_6570.docx`
- Read: `dir tôi/markdown/02_chuong_2/99_tai_lieu_tham_khao.md`
- Read: `dir tôi/markdown/03_chuong_3/99_tai_lieu_tham_khao.md`

**Interfaces:**
- Consumes: references da co trong Markdown va noi dung 3 chuong.
- Produces: ket luan va tai lieu tham khao khong con placeholder.

- [ ] **Step 1: Viet `Kết luận` thanh 3-5 doan**

Conclusion must cover:

```text
Ket qua chinh cua nghien cuu
Dong gop ve ly luan/thuc tien
Giai phap trong tam cho xa Cu Chi
Han che nghien cuu
Huong nghien cuu/ung dung tiep theo
```

- [ ] **Step 2: Sua heading tai lieu tham khao**

Change:

```text
TÀI LIỆU THAM HẢO
```

to:

```text
TÀI LIỆU THAM KHẢO
```

- [ ] **Step 3: Hop nhat references thanh mot danh muc**

Use APA-style entries already present in:

```text
dir tôi/markdown/02_chuong_2/99_tai_lieu_tham_khao.md
dir tôi/markdown/03_chuong_3/99_tai_lieu_tham_khao.md
```

Expected: khong con dong `….………..` o phan tai lieu tham khao.

### Task 6: Ra soat dinh dang va ban nop

**Files:**
- Modify: `docs/JTyd_6570.docx`
- Produce: final submitted docx, recommended name `docs/JTyd_6570_hoan_thien.docx`

**Interfaces:**
- Consumes: Word da bo sung front matter, hinh, ket luan, references.
- Produces: ban nop cuoi cung.

- [ ] **Step 1: Kiem tra cac phan bat buoc bang text search**

Run:

```bash
textutil -convert txt -stdout 'docs/JTyd_6570.docx' | rg -n 'MỤC LỤC|DANH MỤC BẢNG|DANH MỤC HÌNH|DANH MỤC TỪ VIẾT TẮT|MỞ ĐẦU|CHƯƠNG 1|CHƯƠNG 2|CHƯƠNG 3|Kết luận|TÀI LIỆU THAM KHẢO|PHỤ LỤC'
```

Expected: all required headings appear.

- [ ] **Step 2: Kiem tra khong con placeholder**

Run:

```bash
textutil -convert txt -stdout 'docs/JTyd_6570.docx' | rg -n 'chèn|VẼ BIỂU ĐỒ|….|……|THAM HẢO'
```

Expected: no remaining placeholder or misspelled heading.

- [ ] **Step 3: Cap nhat muc luc/danh muc trong Word**

In Microsoft Word: Select all (`Cmd+A`) -> Update fields (`Fn+F9` or right click `Update Field`) -> update entire table.

- [ ] **Step 4: Luu ban nop**

Save as:

```text
docs/JTyd_6570_hoan_thien.docx
```
