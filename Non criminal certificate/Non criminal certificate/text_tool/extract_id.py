import sys
import re
from pypinyin import lazy_pinyin
from datetime import datetime

nationality = {"加拿大": "Canadian", 
"美国": "American",
"中国": "Chinese",
"中华人民共和国": "Chinese"

}




def extract_info(precedent,text):

    pattern = rf"(?:{precedent}):\s*([\u4e00-\u9fff0-9.\-]+)"
    segment_cn = re.findall (pattern,text, re.IGNORECASE)

    return segment_cn[0] if segment_cn else "None"



def convert_date(date):
     date = re.sub("日","",re.sub("年|月","-",date))
     for fmt in ("%Y-%m-%d", "%m-%d"):
        try:
            dt = datetime.strptime(date, fmt)
            if fmt == "%Y-%m-%d":
                return f"{dt:%B} {dt.day}, {dt.year}"
            return f"{dt:%B} {dt.day}"
        except ValueError:
            continue
        return date



def extract_all_info(text):
    info = {}
    dates= re.findall(r"\d{4}年\d{1,2}月\d{1,2}日", text)
    start = dates[0]
    end = dates[1]
    serial = re.search(r"\d{32}",text).group(0)
    name_cn= extract_info("被查询人",text)
    name_py = lazy_pinyin(name_cn)
    first = "".join (name_py[1:]).capitalize()
    last = "".join([c.capitalize() for c in name_py[0]])
    name_py = "".join (first+" "+last)
    info ["name"] = name_py
    info ["nationality"]  = nationality [extract_info("国籍",text).strip()]
    if extract_info ("证件名称",text) == "身份证":
        info ["id type"]  ="ID Card" 
    info["id number"] =  extract_info("证件号码",text)
    info["serial"] =  serial
    info["start"] = convert_date(start)
    info["end"] = convert_date(end)
   # info["number"] = number
    print(info)
    pattern = r"[○零一二三四五六七八九十]{4}年[一二三四五六七八九十]{1}月[一二三四五六七八九十]{2}日"  
    #date_cn = re.search (pattern, text).group(0)
    #info ["date"] =  date_cn
    return info


	

def main ():
    text_processed = r"..\output\ocr_processed\text_processed.txt"
    with open(text_processed, "r", encoding="utf-8") as f:
      text = f.read()
      info = extract_all_info(text)

    print(info)





if __name__ =="__main__":
     main()
