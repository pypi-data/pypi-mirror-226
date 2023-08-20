import numpy as np
import pandas as pd
import os
import warnings

def list_Excel_sheetNames(file_path):

    # 检测文件路径是否存在
    if not os.path.exists(file_path):
        warnings.warn(f"File path '{file_path}' does not exist.")
        exit(1)

    try:
        excel_file = pd.ExcelFile(file_path)

        # 获取表格的名称列表
        sheet_names = excel_file.sheet_names
        return sheet_names

    except Exception as e:
        print(f"An error occurred: {e}")


def list_matplotlib_support_font():
    # 查询当前系统所有字体
    from matplotlib.font_manager import FontManager
    import subprocess

    mpl_fonts = set(f.name for f in FontManager().ttflist)

    print('all font list get from matplotlib.font_manager:')
    for f in sorted(mpl_fonts):
        print('\t' + f)