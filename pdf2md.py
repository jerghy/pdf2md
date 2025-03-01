import pdfplumber
import re

def get_heading_level(font_size, base_size=11):
    """根据字体大小判断标题级别"""
    if font_size >= base_size + 8:  # 特大字号
        return 1
    elif font_size >= base_size + 6:
        return 2
    elif font_size >= base_size + 4:
        return 3
    elif font_size >= base_size + 2:
        return 4
    return 0  # 不是标题

def pdf_to_markdown(pdf_path, output_path):
    with pdfplumber.open(pdf_path) as pdf:
        markdown_text = ""
        page_num = 0
        current_paragraph = ""
        base_font_size = 11  # 基准字体大小，可能需要根据PDF调整
        
        for page in pdf.pages:
            words = page.extract_words(keep_blank_chars=True, x_tolerance=3, y_tolerance=3)
            
            current_y = None
            for word in words:
                # 获取文字的样式信息
                font_size = word.get('size', 11)
                font_name = word.get('fontname', '').lower()
                
                # 判断是否是新的一行
                if current_y is not None and abs(word['top'] - current_y) > 3:
                    if current_paragraph:
                        markdown_text += current_paragraph.strip() + "\n\n"
                        current_paragraph = ""
                
                current_y = word['top']
                text = word['text']
                
                # 处理标题
                heading_level = get_heading_level(font_size, base_font_size)
                if heading_level > 0:
                    if current_paragraph:
                        markdown_text += current_paragraph.strip() + "\n\n"
                        current_paragraph = ""
                    markdown_text += "#" * heading_level + " " + text + "\n\n"
                    continue
                
                # 处理文本格式
                if 'bold' in font_name:
                    text = f"**{text}**"
                elif 'italic' in font_name:
                    text = f"*{text}*"
                elif 'underline' in font_name:  # 注意：pdfplumber可能无法直接检测下划线
                    text = f"=={text}=="
                
                # 添加适当的空格
                if current_paragraph and not current_paragraph.endswith(' '):
                    current_paragraph += ' '
                current_paragraph += text
            
            # 处理页末段落
            if current_paragraph:
                markdown_text += current_paragraph.strip() + "\n\n"
                current_paragraph = ""
            
            page_num += 1
            print(f"处理第{page_num}页")
        
        # 保存为 markdown 文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)

if __name__ == "__main__":
    pdf_path = "高考专题复习集锦+语文+PDF版含解析.pdf"
    output_path = "output.md"
    pdf_to_markdown(pdf_path, output_path)
