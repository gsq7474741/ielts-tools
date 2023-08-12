#!/usr/bin/python

import fitz

pdf_document = "G:\BaiduNetdiskDownload\雅思复习计划（趴趴雅思原创）\复习计划配套电子资料\听力\雅思王听力真题语料库  趴趴雅思整理\王陆语料库剑14版_ocr.pdf"
doc = fitz.open(pdf_document)
print ("number of pages: %i" % doc.page_count)
print(doc.metadata)

page1 = doc.load_page(45)
page1text = page1.get_text("text")
print(page1text)
