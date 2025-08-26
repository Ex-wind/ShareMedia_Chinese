import os
import re
from pypinyin import pinyin, Style

# 源文件夹与输出文件
EXWIND_SOURCE_DIR = r"C:\Users\lcy30\OneDrive\桌面\V"  # 音频文件夹
EXWIND_OUT_DIR = r"C:\Users\lcy30\OneDrive\桌面\EXWIND 工具\ShareMedia"  # 输出txt档案文件夹
EXWIND_OUT_FILE = os.path.join(EXWIND_OUT_DIR, "xxx.txt")  # 输出txt文件名 注意自己复制进ShareMedia 这个不能直接替换 

# 在这里修改做这名称
EXWIND_PREFIX = "EX_"

os.makedirs(EXWIND_OUT_DIR, exist_ok=True)

EXWIND_lines = []

for EXWIND_file in os.listdir(EXWIND_SOURCE_DIR):
    EXWIND_full = os.path.join(EXWIND_SOURCE_DIR, EXWIND_file)
    if not os.path.isfile(EXWIND_full):
        continue

    name_no_ext, ext = os.path.splitext(EXWIND_file)
    ext_lower = ext.lower()
    if ext_lower not in (".mp3", ".ogg"):
        continue

    title = name_no_ext  

    m = re.match(r'^【([^】]+)】\s*(.*)$', name_no_ext)
    if not m:
        rest_name = name_no_ext.lstrip()
        first_char = rest_name[:1] if rest_name else ""
        initial = pinyin(first_char, style=Style.FIRST_LETTER)[0][0].upper() if first_char else ""
        title = f"({EXWIND_PREFIX}{initial}) {rest_name}" if initial else f"({EXWIND_PREFIX}) {rest_name}"
    else:
        EXWIND_tag = m.group(1)
        EXWIND_rest = m.group(2)
        rest_stripped = EXWIND_rest.lstrip()
        first_char = rest_stripped[:1] if rest_stripped else ""
        initial = pinyin(first_char, style=Style.FIRST_LETTER)[0][0].upper() if first_char else ""
        title = f"({EXWIND_tag}{initial}) {rest_stripped}" if initial else f"({EXWIND_tag}) {rest_stripped}"

    EXWIND_line = f'LSM:Register("sound", "{title}", [[Interface\\Addons\\SharedMedia_Exwind\\sound\\{EXWIND_file}]])'
    EXWIND_lines.append(EXWIND_line)

EXWIND_lines.sort()

with open(EXWIND_OUT_FILE, "w", encoding="utf-8") as f:
    for line in EXWIND_lines:
        f.write(line + "\n")
