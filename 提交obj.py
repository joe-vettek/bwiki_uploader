from docx import Document

# 读取 txt 文件
with open(r"C:\Users\Admin\Downloads\MMD\雪精灵_by_卡拉彼丘_84cbce648c58fcd51c6082a10615749d\Yvette_105.mtl", 'r',encoding='utf-8') as f:
    text = f.read()

p=r'C:\Users\Admin\Desktop\各2.docx'


# 创建一个新的 Document 对象
doc = Document()


# 添加文本到文档
doc.add_paragraph(text)

# 保存文档为 odt 文件
doc.save('file.docx')
