import re

# 去除noise里面的字符
def remove_noise(text):
    # noise = r'[\s+*【】\[\]\“]'    # 
    noise = r'[\s]'                 # '\s'表示空格、换行
    return re.sub(noise, '', q_to_b(text))

# 去除中文标点符号、英文标点符号、表情
def remove_symbol(text):
    punctuation_cn = ("[\u0060|\u0021-\u002c|\u002e-\u002f|\u003a-\u003f|"
                  "\u2200-\u22ff|\uFB00-\uFFFD|\u2E80-\u33FF]")
    result = re.sub(punctuation_cn, '', text)
    result = re.sub(r'[\s+\.\!\/_,$%^*(+\"\'\[\]▁~]', '', result)
    result = re.sub('[😂😃😄😍😊😁🌟👍♡ơ₃ฅ💋╰╯mั●๑❤]', '', result)
    return result

# modified
def q_to_b(q_str):
    """全角转半角"""
    b_str = ""
    for uchar in q_str:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif 65374 >= inside_code >= 65281:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248
        elif inside_code == ord('。'):
            inside_code = ord('.')
        elif inside_code == ord('、'):
            inside_code = ord(',')

        punctuation_en = u',.!?[]()%#@&'
        if chr(inside_code) not in punctuation_en:
            b_str += chr(inside_code)
        else:
            b_str += (chr(inside_code) + ' ')
    return b_str


def b_to_q(b_str):
    """半角转全角"""
    q_str = ""
    for uchar in b_str:
        inside_code = ord(uchar)
        if inside_code == 32:  # 半角空格直接转化
            inside_code = 12288
        elif 126 >= inside_code >= 32:  # 半角字符（除空格）根据关系转化
            inside_code += 65248
        q_str += chr(inside_code)
    return q_str
# 原文：https://blog.csdn.net/JYZ4MFC/article/details/81297626 
