import sys
from pathlib import Path
import re
from docx.oxml.ns import qn
from extract_id import extract_all_info
from docx import Document

template_path = r"..\Template\Certificate of No Criminal Record.docx"
template_file = Document(template_path)
ocr_file = r"..\raw_data\text_processed.txt"
with open(ocr_file, "r", encoding="utf-8") as f:
    text = f.read()
data = extract_all_info(text)



#字体设置
def set_run_font(run, font_name="Times New Roman"):
    run.font.name = font_name
    r = run._element.rPr
    r.rFonts.set(qn("w:ascii"), font_name)
    r.rFonts.set(qn("w:hAnsi"), font_name)
    r.rFonts.set(qn("w:eastAsia"), font_name)


def replace_placeholders_in_paragraph(paragraph, mapping):
    full_text = "".join(run.text for run in paragraph.runs)

    if not any(f"{{{{{k}}}}}" in full_text for k in mapping.keys()):
        return

    def replacement(match):
        key = match.group(1)
        return mapping.get(key, match.group(0))

    #替换成key对应的value值，如果key不存在则保留{{key}}
    new_text = re.sub(r"\{\{(.*?)}}", replacement, full_text)

    # 清空原 runs
    for run in paragraph.runs:
        run.text = ""

    # 按 value 拆分并重建


    sorted_values = sorted(
    [str(v) for v in mapping.values() if v is not None],
    key=len,
    reverse=True
    )    #value按长度排序
    pattern = "(" + "|".join(map(re.escape, sorted_values)) + ")"
    parts = re.split(pattern, new_text)

    for part in parts:
        run = paragraph.add_run(part)
        if part in mapping.values():   # 替换内容 → 加粗
            run.bold = True

        # 不论是否加粗，统一设定字体：
        set_run_font(run)



def process_document(temp, data ):
    for paragraph in temp.paragraphs:
        replace_placeholders_in_paragraph(paragraph, data)

    for table in temp.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    replace_placeholders_in_paragraph(paragraph, data)


    
process_document(temp = template_file, data = data)

# 获取当前 Python 文件所在目录
base_dir = Path(__file__).resolve().parent

# 创建 clients 文件夹路径
clients_dir = base_dir.parent / "clients"

# 如果不存在，则创建
clients_dir.mkdir(parents=True, exist_ok=True)

# 保存 Word 文件
output_path = clients_dir / "No Criminal Record.docx"

template_file.save(output_path)




