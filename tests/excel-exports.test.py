from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET


NS = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def count_sheet_rows(path: Path) -> int:
    assert path.exists(), f"Excel file must exist: {path}"
    assert path.stat().st_size > 1_000, f"Excel file is unexpectedly small: {path}"
    with zipfile.ZipFile(path) as zf:
        names = set(zf.namelist())
        assert "[Content_Types].xml" in names, "xlsx must include content types"
        assert "xl/workbook.xml" in names, "xlsx must include workbook"
        assert "xl/worksheets/sheet1.xml" in names, "xlsx must include first worksheet"
        sheet = ET.fromstring(zf.read("xl/worksheets/sheet1.xml"))
    return len(sheet.findall("main:sheetData/main:row", NS))


real_xlsx = Path("charts/khao_sat_du_lich_nong_nghiep_xanh_cu_chi/du_lieu_cau_tra_loi_khao_sat.xlsx")
fake_xlsx = Path("charts/khao_sat_fake_241/du_lieu_cau_tra_loi_khao_sat_fake_241.xlsx")

assert count_sheet_rows(real_xlsx) == 42, "real Excel must contain header + 41 responses"
assert count_sheet_rows(fake_xlsx) == 242, "fake Excel must contain header + 241 responses"
