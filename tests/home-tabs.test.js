const assert = require("assert");
const fs = require("fs");

const html = fs.readFileSync("index.html", "utf8");

assert(html.includes('role="tablist"'), "homepage must expose a tablist");
assert(html.includes('data-tab-target="report"'), "homepage must include Báo cáo tab control");
assert(html.includes('data-tab-target="survey"'), "homepage must include Khảo sát tab control");
assert(html.includes('data-tab-target="fakeSurvey"'), "homepage must include Khảo sát Fake tab control");
assert(html.includes("Xem báo cáo"), "report tab must be labeled Xem báo cáo");
assert(html.includes("Xem khảo sát"), "survey tab must be labeled Xem khảo sát");
assert(html.includes("Khảo sát Fake"), "fake survey tab must be labeled Khảo sát Fake");
assert(!html.includes("Mở Markdown"), "homepage must not show Mở Markdown button");
assert(!html.includes("Tải lại"), "homepage must not show Tải lại button");
assert(!html.includes("window.print()"), "homepage must not show print action");
assert(!html.includes(">In<"), "homepage must not show In button");
assert(!html.includes("Chạy local server"), "homepage must not show local server instruction box");
assert(!html.includes("python3 -m http.server"), "homepage must not show local server command");
assert(!html.includes("local-command"), "homepage must not include local server instruction class");
assert(html.includes('id="reportPanel"'), "homepage must include report panel");
assert(html.includes('id="surveyPanel"'), "homepage must include survey panel");
assert(html.includes('id="fakeSurveyPanel"'), "homepage must include fake survey panel");

[
  "01_phan_phoi_mau_khao_sat.png",
  "02_phan_phoi_likert_q8_q38.png",
  "03_diem_trung_binh_theo_cau_hoi.png",
  "04_so_sanh_theo_nhom_noi_dung.png",
  "05_muc_ung_ho_giai_phap_de_xuat.png",
  "06_phan_tich_cau_hoi_mo.png",
].forEach((image) => {
  assert(html.includes(image), `survey panel must show ${image}`);
});

assert(
  html.includes("du_lieu_cau_tra_loi_khao_sat.csv"),
  "survey panel must load the raw response CSV"
);
assert(
  html.includes("du_lieu_cau_tra_loi_khao_sat.xlsx"),
  "survey panel must include Excel download for real responses"
);
assert(
  html.includes("du_lieu_cau_tra_loi_khao_sat_fake_241.csv"),
  "fake survey panel must load the 241-row fake response CSV"
);
assert(
  html.includes("du_lieu_cau_tra_loi_khao_sat_fake_241.xlsx"),
  "fake survey panel must include Excel download for fake responses"
);
assert(html.includes("Tải Excel"), "survey panels must expose Excel download buttons");
assert(html.includes("function parseCsv"), "homepage must include CSV parser");
assert(html.includes("function activateTab"), "homepage must include tab switching behavior");
