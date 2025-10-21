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
    """
    # 尝试匹配 "YYYY MM" 或 "YYYY M" 格式
    pattern = r'^(\d{4})\s+(\d{1,2})'
    match = re.match(pattern, folder_name)
    
    if match:
        year = match.group(1)
        month = match.group(2).zfill(2)  # 补齐为两位数
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
        for folder in folders:
            # 遍历文件夹中的所有PDF文件
            for pdf_file in folder.rglob("*.pdf"):
                try:
                    # 构造目标文件路径
                    relative_path = pdf_file.relative_to(folder)
                    target_file = new_folder_path / folder.name / relative_path
                    
                    # 创建目标目录
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    # 复制文件
                    shutil.copy2(pdf_file, target_file)
                    pdf_count += 1
                    print(f"    复制: {pdf_file.name}")
                    
                except Exception as e:
                    print(f"    错误：复制 {pdf_file} 时出错: {e}")
        
        print(f"  共复制 {pdf_count} 个PDF文件")
    
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
