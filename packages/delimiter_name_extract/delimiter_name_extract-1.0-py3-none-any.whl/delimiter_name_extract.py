import re


def delimiter_name_extract(filename, delimiters=['[]', '【】'], mode='all'):
    valid_modes = ['all', 'num']  # 可接受的 mode 值
    if mode not in valid_modes:
        raise ValueError(f"无效的模式。请选择以下模式之一：{', '.join(valid_modes)}")

    if mode == 'num':
        pattern = r'\d+'
    else:
        pattern = r'\w+'

    for delim in delimiters:
        match = re.search(
            rf'{re.escape(delim[0])}({pattern}){re.escape(delim[1])}', filename)
        if match:
            return match.group(1)

    return None
