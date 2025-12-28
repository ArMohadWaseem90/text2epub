# TXT 转 EPUB

我下载了一些中文 TXT 小说，需要转成 EPUB 传到 reMarkable 2 里。  
用 Calibre 转 EPUB 对我来说太慢，所以写了这个 Python 脚本。

## 安装

```bash
python -m venv .venv

# Windows：
#   .venv\Scripts\activate
# macOS/Linux：
#   source .venv/bin/activate

pip install -r requirements.txt
````

## 用法

不加参数：将当前目录下所有 `.txt` 文件批量转成 EPUB

```bash
python t2e.py
```

指定文件：只转换单个文件

```bash
python t2e.py input.txt
```

## 说明

有些 TXT 下载后会出现乱码，一般是编码问题。
脚本会自动检测文件编码并尽量正确转换。

```
```
