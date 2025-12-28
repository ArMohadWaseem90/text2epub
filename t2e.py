# -*- coding: utf-8 -*-
import re
import os
import random
import argparse
import chardet
from tqdm import tqdm
from ebooklib import epub

def split_text(text, max_length=1024):
    sentence_list = re.findall(r'.+?[。！？!?.]', text, flags=re.DOTALL)
    short_text_list = []
    short_text = ""
    for s in sentence_list:
        if len(short_text) + len(s) <= max_length:
            short_text += s
        else:
            if short_text:
                short_text_list.append(short_text)
            short_text = s
    if short_text:
        short_text_list.append(short_text)
    return short_text_list

def text_to_epub(text_list, filename, language_code='en', title="Title"):
    book = epub.EpubBook()
    book.set_identifier(str(random.randint(100000, 999999)))
    book.set_title(title)
    book.set_language(language_code)

    chapters = []
    for i, segment in enumerate(text_list, 1):
        segment = segment.replace("\n", "<br>")
        c = epub.EpubHtml(title="", file_name=f'chap_{i}.xhtml', lang=language_code)
        c.content = segment
        book.add_item(c)
        chapters.append(c)

    book.spine = ['nav'] + chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(filename, book, {})

def process_one_file(filename: str, test: bool):
    if not os.path.isfile(filename):
        print(f"Skip (not a file): {filename}")
        return

    base_filename, _ = os.path.splitext(filename)
    new_filename_epub = base_filename + "_translated.epub"
    new_filename_txt = base_filename + "_converted_utf8.txt"

    with open(filename, 'rb') as f:
        raw_data = f.read()

    detected = chardet.detect(raw_data)
    file_encoding = detected.get('encoding') or 'utf-8'
    print(f"\n==> {filename}")
    print(f"Detected file encoding: {file_encoding}")

    text = raw_data.decode(file_encoding, errors='replace')
    title = os.path.basename(filename)

    # 输出统一 utf-8 的 txt（把 \n 变成 <br>）
    text_br = text.replace('\n', '<br>')
    with open(new_filename_txt, 'w', encoding='utf-8') as outfile:
        outfile.write(text_br)

    # 分段
    text_segments = split_text(text)
    if test:
        text_segments = text_segments[:3]

    processed_segments = []
    with tqdm(total=len(text_segments), desc=f"Segments ({os.path.basename(filename)})") as pbar:
        for seg in text_segments:
            processed_segments.append(seg)
            pbar.update(1)

    text_to_epub(processed_segments, new_filename_epub, "zh", title)

    print(f"EPUB file created: {new_filename_epub}")
    print(f"UTF-8 TXT file created: {new_filename_txt}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", help="Input .txt file (optional). If omitted, process all *.txt in current dir.")
    parser.add_argument("--test", help="Only process the first 3 segments (per file)", action="store_true")
    args = parser.parse_args()

    if args.filename:
        process_one_file(args.filename, args.test)
        return

    # 没传 filename：处理当前目录所有 *.txt
    files = sorted([f for f in os.listdir(".") if f.lower().endswith(".txt") and os.path.isfile(f)])
    if not files:
        print("No *.txt files found in current directory.")
        return

    for f in files:
        process_one_file(f, args.test)

if __name__ == "__main__":
    main()
