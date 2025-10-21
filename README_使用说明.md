# 文件整理工具使用说明

## 功能说明

这个脚本可以：
1. 扫描指定目录下的所有文件夹
2. 识别前13位相同的文件夹并分组
3. 从文件夹名提取日期信息
   - 支持格式1：`2022 7` -> `2022-07`（带空格）
   - 支持格式2：`202210` -> `2022-10`（连续数字）
4. 创建新文件夹，命名格式：`日期-前13位字符`
5. 将相同组内所有文件夹中的**所有文件**（PDF、OFD等）**直接复制**到新文件夹根目录
6. 自动去重，避免重复复制同名文件

## 使用方法

### 方式1：交互式运行

直接运行脚本，按提示输入路径：

```bash
python organize_pdfs.py
```

### 方式2：修改脚本直接运行

编辑 `organize_pdfs.py` 文件，在最后添加：

```python
# 直接指定路径运行
if __name__ == "__main__":
    source = r"E:\University\graduate"  # 源目录
    target = None  # 目标目录（None表示在源目录创建）
    organize_pdfs(source, target)
```

## 示例

### 示例1：带空格的日期格式（含多种文件类型和去重）

#### 输入文件结构：
```
E:\University\graduate\
├── 2022 7A   537eee/
│   ├── file1.pdf
│   ├── file2.ofd
│   ├── document.docx
│   └── report.pdf      ← 同名文件1
└── 2022 7A   537证附件汇总/
    ├── file3.pdf
    ├── receipt.ofd
    ├── report.pdf      ← 同名文件2（会被跳过）
    └── subfolder/
        └── file4.pdf
```

#### 输出文件结构：
```
E:\University\graduate\
├── 2022-07-2022 7A   537/
│   ├── file1.pdf
│   ├── file2.ofd
│   ├── document.docx
│   ├── file3.pdf
│   ├── receipt.ofd
│   ├── file4.pdf
│   └── report.pdf     ← 只复制一次
```

#### 运行时输出：
```
✓ 复制: file1.pdf (来自: 2022 7A   537eee)
✓ 复制: file2.ofd (来自: 2022 7A   537eee)
✓ 复制: document.docx (来自: 2022 7A   537eee)
✓ 复制: report.pdf (来自: 2022 7A   537eee)
✓ 复制: file3.pdf (来自: 2022 7A   537证附件汇总)
✓ 复制: receipt.ofd (来自: 2022 7A   537证附件汇总)
⊘ 跳过重复文件: report.pdf (来自: 2022 7A   537证附件汇总)
✓ 复制: file4.pdf (来自: 2022 7A   537证附件汇总)
⊘ 跳过 1 个重复文件
✓ 本组共复制 7 个文件
```

### 示例2：连续数字日期格式

#### 输入文件结构：
```
E:\University\graduate\
├── 202210A  3535 银行电子回单/
│   ├── receipt1.pdf
│   ├── receipt2.ofd
│   └── statement.xlsx
└── 202210A  3535abc/
    ├── receipt3.pdf
    └── invoice.ofd
```

#### 输出文件结构：
```
E:\University\graduate\
├── 2022-10-202210A  3535/
│   ├── receipt1.pdf
│   ├── receipt2.ofd
│   ├── statement.xlsx
│   ├── receipt3.pdf
│   └── invoice.ofd
```

## 注意事项

1. ✅ 脚本**复制所有文件**（包括PDF、OFD等所有格式），不复制文件夹结构
2. ✅ 所有文件会被复制到新文件夹的**根目录**
3. ✅ 脚本会递归查找所有子目录中的文件
4. ✅ **自动去重**：同名文件只复制一次（避免重复）
5. ✅ 原始文件不会被删除或移动
6. ⚠️ 如果无法从文件夹名提取日期，新文件夹会以"未识别日期-"开头
7. 💡 支持所有文件类型：`.pdf`、`.PDF`、`.ofd`、`.OFD`、`.docx`、`.xlsx` 等
8. 💡 在Windows系统上运行时，路径可以使用 `\` 或 `/`

## 去重说明

如果多个文件夹中存在**同名**文件，脚本会：
- ✅ 只复制第一次遇到的文件
- ⊘ 跳过后续的同名文件
- 📊 统计并显示跳过的重复文件数量

**示例：**
```
文件夹A/report.pdf  ← 复制
文件夹B/report.pdf  ← 跳过（重复）
文件夹C/data.ofd    ← 复制
文件夹D/data.ofd    ← 跳过（重复）
```

## 支持的文件类型

脚本会复制**所有类型**的文件，包括但不限于：
- 📄 PDF文件：`.pdf`、`.PDF`
- 📑 OFD文件：`.ofd`、`.OFD`
- 📝 Office文档：`.docx`、`.xlsx`、`.pptx`
- 🖼️ 图片文件：`.jpg`、`.png`、`.gif`
- 📦 压缩文件：`.zip`、`.rar`
- 🎵 其他任何格式的文件

## 依赖

- Python 3.6+
- 标准库（无需额外安装）
