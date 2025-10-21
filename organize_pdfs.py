#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF文件整理脚本
将前13位相同的文件夹中的PDF文件复制到统一的新文件夹中
"""

import os
import shutil
import re
from pathlib import Path
from collections import defaultdict


def extract_date_from_folder_name(folder_name):
    """
    从文件夹名中提取日期信息
    例如："2022 7A   537eee" -> "2022-07"
         "202210A  3535" -> "2022-10"
    """
    # 尝试匹配 "YYYYMM" 格式（如：202210A）
    pattern1 = r'^(\d{4})(\d{2})'
    match1 = re.match(pattern1, folder_name)
    
    if match1:
        year = match1.group(1)
        month = match1.group(2)
        return f"{year}-{month}"
    
    # 尝试匹配 "YYYY MM" 或 "YYYY M" 格式（如：2022 7A）
    pattern2 = r'^(\d{4})\s+(\d{1,2})'
    match2 = re.match(pattern2, folder_name)
    
    if match2:
        year = match2.group(1)
        month = match2.group(2).zfill(2)  # 补齐为两位数
        return f"{year}-{month}"
    
    return None


def get_first_13_chars(folder_name):
    """获取文件夹名的前13位"""
    return folder_name[:13] if len(folder_name) >= 13 else folder_name


def organize_pdfs(source_dir, target_base_dir=None):
    """
    整理PDF文件
    
    Args:
        source_dir: 源目录路径（如：E:\University\graduate\）
        target_base_dir: 目标基础目录（默认为源目录）
    """
    source_path = Path(source_dir)
    
    if not source_path.exists():
        print(f"错误：源目录不存在: {source_dir}")
        return
    
    if target_base_dir is None:
        target_base_dir = source_path
    else:
        target_base_dir = Path(target_base_dir)
    
    # 创建目标基础目录（如果不存在）
    target_base_dir.mkdir(parents=True, exist_ok=True)
    
    # 按前13位分组文件夹
    folder_groups = defaultdict(list)
    
    print(f"正在扫描目录: {source_path}")
    print("-" * 60)
    
    # 遍历源目录下的所有文件夹
    for item in source_path.iterdir():
        if item.is_dir():
            first_13 = get_first_13_chars(item.name)
            folder_groups[first_13].append(item)
    
    print(f"找到 {len(folder_groups)} 组前13位相同的文件夹")
    print("-" * 60)
    
    # 处理每组文件夹
    for first_13, folders in folder_groups.items():
        print(f"\n处理组: '{first_13}'")
        print(f"包含 {len(folders)} 个文件夹:")
        for folder in folders:
            print(f"  - {folder.name}")
        
        # 提取日期
        date_prefix = extract_date_from_folder_name(first_13)
        
        # 创建新文件夹名
        if date_prefix:
            new_folder_name = f"{date_prefix}-{first_13}"
        else:
            new_folder_name = f"未识别日期-{first_13}"
            print(f"  警告：无法从 '{first_13}' 中提取日期")
        
        # 创建新文件夹
        new_folder_path = target_base_dir / new_folder_name
        new_folder_path.mkdir(parents=True, exist_ok=True)
        print(f"  创建新文件夹: {new_folder_name}")
        
        # 收集并复制所有PDF文件
        pdf_count = 0
        file_counter = {}  # 用于处理重名文件
        
        for folder in folders:
            # 遍历文件夹中的所有PDF文件（包括子目录）
            pdf_files = list(folder.rglob("*.pdf"))
            PDF_files = list(folder.rglob("*.PDF"))  # 大写扩展名
            all_pdfs = pdf_files + PDF_files
            
            for pdf_file in all_pdfs:
                try:
                    # 直接复制到新文件夹根目录，不保留文件夹结构
                    target_file = new_folder_path / pdf_file.name
                    
                    # 处理文件名冲突：如果文件已存在，添加序号
                    if target_file.exists():
                        base_name = pdf_file.stem
                        extension = pdf_file.suffix
                        
                        # 记录重名次数
                        if pdf_file.name not in file_counter:
                            file_counter[pdf_file.name] = 1
                        else:
                            file_counter[pdf_file.name] += 1
                        
                        counter = file_counter[pdf_file.name]
                        new_name = f"{base_name}_{counter}{extension}"
                        target_file = new_folder_path / new_name
                        print(f"    ⚠️  文件名冲突，重命名为: {new_name}")
                    
                    # 复制文件
                    shutil.copy2(pdf_file, target_file)
                    pdf_count += 1
                    print(f"    复制: {pdf_file.name} (来自: {folder.name})")
                    
                except Exception as e:
                    print(f"    错误：复制 {pdf_file.name} 时出错: {e}")
        
        print(f"  共复制 {pdf_count} 个PDF文件到新文件夹根目录")
    
    print("\n" + "=" * 60)
    print("处理完成！")


def main():
    """主函数"""
    # 默认源目录（Windows路径）
    default_source = r"E:\University\graduate"
    
    print("=" * 60)
    print("PDF文件整理工具")
    print("=" * 60)
    print()
    
    # 获取用户输入
    source_dir = input(f"请输入源目录路径 [默认: {default_source}]: ").strip()
    if not source_dir:
        source_dir = default_source
    
    target_dir = input("请输入目标目录路径 [默认: 与源目录相同]: ").strip()
    if not target_dir:
        target_dir = None
    
    print()
    print("开始处理...")
    print()
    
    # 执行整理
    organize_pdfs(source_dir, target_dir)


if __name__ == "__main__":
    main()
