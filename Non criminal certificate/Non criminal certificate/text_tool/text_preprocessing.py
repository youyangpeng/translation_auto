import sys
import re



def processing (raw_text, processed_text):

    with open (raw_text, "r", encoding = "utf8") as f:
        text = f.read()
        text = re.sub("[:：]","",text)
        text = re.sub(r"\s+", "", text)
 
       
        parts = re.split("(被查询人|国籍|证件名称|证件号码|在|至|期间)", text) 
        


    with open (processed_text, "w", encoding = "utf8") as full_text: 
          
      for i in range(1, len(parts), 2):
          if i + 1 < len(parts):
              key = parts[i]
              value = parts[i+1].strip()
              full_text.write(f"{key}: {value}")
              full_text.write ("\n")
     



if __name__ == "__main__":
   raw_text = r"..\raw_data\raw_data.txt"
   processed_text = r"..\raw_data\text_processed.txt"
   processing (raw_text, processed_text)






