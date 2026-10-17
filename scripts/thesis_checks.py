#!/usr/bin/env python3
"""Read-only structural inventory; visual inspection remains necessary."""
import argparse
import json
import re
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def normalize_class(value, year='2024', major='导游'):
    """Extract the student's class number; never substitute a sample number."""
    text = re.sub(r'\s+', '', value)
    match = re.search(r'([0-9]+|[一二三四五六七八九十两零〇]+)班', text)
    if not match:
        if re.fullmatch(r'[0-9]+|[一二三四五六七八九十两零〇]+', text):
            numeral = text
        else:
            raise ValueError('无法确定班号，请保留原值并核对')
    else:
        numeral = match.group(1)
    if numeral.isdigit():
        number = int(numeral)
    else:
        digits = dict(zip('零一二三四五六七八九', range(10)))
        digits.update({'两': 2, '〇': 0})
        if '十' in numeral:
            if numeral.count('十') != 1:
                raise ValueError('班号超出支持范围')
            a, b = numeral.split('十')
            number = (digits[a] if a else 1) * 10 + (digits[b] if b else 0)
        elif len(numeral) == 1:
            number = digits[numeral]
        else:
            raise ValueError('班号写法不明确')
    if not 1 <= number <= 99:
        raise ValueError('班号应为1至99，请核对')
    return f'{year}{major}（专科）{number}班'

def text_of(node):
    return ''.join(node.xpath('.//w:t/text()', namespaces=NS))

def inspect(path):
    with ZipFile(path) as z:
        root = E.fromstring(z.read('word/document.xml'))
    body = root.find('w:body', NS)
    cover, after_cover = [], False
    for node in body:
        if not after_cover:
            cover.append(node)
        if node.find('w:pPr/w:sectPr', NS) is not None:
            after_cover = True
    report = {'file': str(Path(path).resolve()), 'cover_boundary_found': after_cover,
              'cover_tables': [], 'paragraphs': [], 'review_notes': []}
    if after_cover:
        report['cover_tables'] = [[[text_of(c) for c in row.findall('w:tc', NS)]
                                  for row in table.findall('w:tr', NS)]
                                 for table in cover if table.tag.endswith('}tbl')]
    for p in body.findall('w:p', NS):
        t = text_of(p)
        if (t.startswith('关键词') or t.lower().startswith('keywords') or
                t == '参考文献' or t.startswith('Research on ')):
            pb = p.find('w:pPr/w:pageBreakBefore', NS)
            report['paragraphs'].append({'text': t, 'explicit_page_break_before':
                pb is not None and pb.get('{'+NS['w']+'}val', 'true') not in ('0', 'false'),
                'runs': [{'text': text_of(r), 'properties':
                         E.tostring(r.find('w:rPr', NS), encoding='unicode')
                         if r.find('w:rPr', NS) is not None else 'inherited'}
                         for r in p.findall('w:r', NS)]})
    all_text = text_of(body)
    if re.search(r'\{\{[^{}]+\}\}', all_text):
        report['review_notes'].append('存在未填充占位符')
    if 'Error: Reference source not found' in all_text or '错误!未找到引用源' in all_text:
        report['review_notes'].append('存在失效引用的可见缓存文本')
    report['limitations'] = '仅结构清单；未解析继承样式或全部域；不证明分页、字体渲染或引用真实性。'
    return report

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('docx', nargs='?')
    ap.add_argument('--class-value')
    ap.add_argument('--year', default='2024')
    ap.add_argument('--major', default='导游')
    args = ap.parse_args()
    if args.class_value is not None:
        print(normalize_class(args.class_value, args.year, args.major))
    elif args.docx:
        print(json.dumps(inspect(args.docx), ensure_ascii=False, indent=2))
    else:
        ap.error('请提供DOCX或--class-value')

if __name__ == '__main__':
    main()
