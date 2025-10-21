#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件整理脚本 - 简化版
复制文件夹中的所有文件（PDF、OFD等）
直接修改下面的SOURCE_DIR路径即可运行
"""

import os
import shutil
import re
from pathlib import Path
from collections import defaultdict

# ==================== 配置区域 ====================
# 请修改这里的路径为你的实际路径
SOURCE_DIR = r"E:\University\graduate"

# 目标目录（None表示在源目录中创建新文件夹）
TARGET_DIR = None
# ==================================================


def extract_date_from_folder_name(folder_name):
    """从文件夹名中提取日期信息"""
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
        month = match2.group(2).zfill(2)
        return f"{year}-{month}"
    
    return None


def get_first_13_chars(folder_name):
    """获取文件夹名的前13位"""
    return folder_name[:13] if len(folder_name) >= 13 else folder_name


def organize_files(source_dir, target_base_dir=None):
    """整理文件（PDF、OFD等所有文件）"""
    source_path = Path(source_dir)
    
    if not source_path.exists():
        print(f"❌ 错误：源目录不存在: {source_dir}")
        return
    
    if target_base_dir is None:
        target_base_dir = source_path
    else:
        target_base_dir = Path(target_base_dir)
    
    target_base_dir.mkdir(parents=True, exist_ok=True)
    
    # 按前13位分组文件夹
    folder_groups = defaultdict(list)
    
    print(f"📂 正在扫描目录: {source_path}")
    print("=" * 70)
    
    # 遍历源目录下的所有文件夹
    for item in source_path.iterdir():
        if item.is_dir():
            first_13 = get_first_13_chars(item.name)
            folder_groups[first_13].append(item)
    
    print(f"✓ 找到 {len(folder_groups)} 组前13位相同的文件夹")
    print("=" * 70)
    
    total_files = 0
    
    # 处理每组文件夹
    for idx, (first_13, folders) in enumerate(folder_groups.items(), 1):
        print(f"\n[{idx}/{len(folder_groups)}] 处理组: '{first_13}'")
        print(f"    包含 {len(folders)} 个文件夹:")
        for folder in folders:
            print(f"      • {folder.name}")
        
        # 提取日期
        date_prefix = extract_date_from_folder_name(first_13)
        
        # 创建新文件夹名
        if date_prefix:
            new_folder_name = f"{date_prefix}-{first_13}"
        else:
            new_folder_name = f"未识别日期-{first_13}"
            print(f"    ⚠️  警告：无法从 '{first_13}' 中提取日期")
        
        # 创建新文件夹
        new_folder_path = target_base_dir / new_folder_name
        new_folder_path.mkdir(parents=True, exist_ok=True)
        print(f"    📁 新文件夹: {new_folder_name}")
        
        # 收集并复制所有文件（去重）
        file_count = 0
        copied_files = set()  # 用于记录已复制的文件名，避免重复
        skipped_count = 0  # 记录跳过的重复文件数
        
        for folder in folders:
            # 遍历文件夹中的所有文件（包括子目录）
            all_files = []
            for item in folder.rglob("*"):
                if item.is_file():  # 只处理文件，跳过目录
                    all_files.append(item)
            
            for file_path in all_files:
                try:
                    # 检查是否已复制过同名文件
                    if file_path.name in copied_files:
                        print(f"      ⊘ 跳过重复文件: {file_path.name} (来自: {folder.name})")
                        skipped_count += 1
                        continue
                    
                    # 直接复制到新文件夹根目录，不保留文件夹结构
                    target_file = new_folder_path / file_path.name
                    
                    # 复制文件
                    shutil.copy2(file_path, target_file)
                    copied_files.add(file_path.name)  # 记录已复制的文件名
                    file_count += 1
                    total_files += 1
                    print(f"      ✓ 复制: {file_path.name} (来自: {folder.name})")
                    
                except Exception as e:
                    print(f"      ❌ 错误：复制 {file_path.name} 时出错: {e}")
        
        if skipped_count > 0:
            print(f"    ⊘ 跳过 {skipped_count} 个重复文件")
        print(f"    ✓ 本组共复制 {file_count} 个文件到新文件夹根目录")
    
    print("\n" + "=" * 70)
    print(f"✅ 处理完成！共处理 {total_files} 个文件")
    print(f"📁 新文件夹位置: {target_base_dir}")
    print("=" * 70)


if __name__ == "__main__":
    print("=" * 70)
    print("               文件整理工具 - 简化版")
    print("=" * 70)
    print()
    print(f"源目录: {SOURCE_DIR}")
    print(f"目标目录: {TARGET_DIR if TARGET_DIR else '(与源目录相同)'}")
    print()
    
    # 确认是否继续
    response = input("是否开始处理？(y/n) [y]: ").strip().lower()
    if response and response != 'y':
        print("已取消操作")
    else:
        print()
        organize_files(SOURCE_DIR, TARGET_DIR)
