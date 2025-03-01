import pdfplumber
import re

def pdf_to_markdown(pdf_path, output_path):
    # 打开 PDF 文件
    with pdfplumber.open(pdf_path) as pdf:
        markdown_text = ""
        page_num=0
        # 遍历每一页
        for page in pdf.pages:
            # 提取文本
            text = page.extract_text()
            
            # 基本的文本处理
            # 1. 处理标题 (假设大写的行是标题)
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # 如果整行都是大写，认为是标题
                if line.isupper():
                    markdown_text += f"# {line.title()}\n\n"
                else:
                    # 普通段落
                    markdown_text += f"{line}\n\n"
            page_num+=1
            print(f"处理第{page_num}页")
        # 保存为 markdown 文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)

if __name__ == "__main__":
    # 使用示例
    pdf_path = "高考专题复习集锦+语文+PDF版含解析.pdf"
    output_path = "output.md"
    pdf_to_markdown(pdf_path, output_path)