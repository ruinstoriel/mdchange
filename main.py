import re
import os
import requests



def remove_duplicates_ordered(lst):
    return list(dict.fromkeys(lst))
def context_handle(markdown_text):
  pattern = r'^(?!.*#).*$'

  matches = re.findall(pattern, markdown_text,re.MULTILINE)
  d = dict()
  block = False
  for context in matches:
    #print(f"开始处理 {context}")
    if(context.strip()==""):
       continue
    elif(context.strip().startswith("```") and not block):
       block = not block
       if(context.strip() in d):
          continue
       d[context.strip()]=""
       markdown_text = markdown_text.replace(context, "  - " + context)
    elif(context.strip().startswith("```") and block):
      block = not block
      if(context.strip() in d):
          continue
      d[context.strip()]=""
      markdown_text = markdown_text.replace(context, "  " + context)
    elif(block):
      if(context.strip() in d):
          continue
      d[context.strip()]=""
      markdown_text = markdown_text.replace(context, "  " + context)
    elif(context.strip().startswith("-")):
       if(context.strip() in d):
          continue
       d[context.strip()]=""
       markdown_text = markdown_text.replace(context, "  " + context)
    else:
       if(context.strip() in d):
          continue
       d[context.strip()]=""
       markdown_text = markdown_text.replace(context, "  - " + context)
  return markdown_text


def download_image(url, save_dir):
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join(save_dir, os.path.basename(url))
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    return None

def imageHandle(markdown_text):
    # 定义图片保存目录
  image_dir = "F:/log/assets"
  os.makedirs(image_dir, exist_ok=True)

  # 正则表达式匹配 Markdown 文件中的图片链接 ![alt text](image_url)
  pattern = r'!\[([^\]]*)\]\((https?://[^\)]+)\)'



  # 查找所有匹配的图片链接
  matches = re.findall(pattern, markdown_text)

  # 替换在线图片为本地图片路径
  for alt_text, url in matches:
    local_image_path = download_image(url, image_dir)
    if local_image_path:
        # 将 Markdown 中的链接替换为本地路径
        markdown_text = markdown_text.replace(url, local_image_path)
  markdown_text = markdown_text.replace(image_dir, "../assets")
  return markdown_text

folder_path = 'input'
for root, dirs, files in os.walk(folder_path):
    for filename in files:
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
          markdown_text = file.read()
        markdown_text = context_handle(markdown_text)
        markdown_text = imageHandle(markdown_text)
        # 写回到 markdown 文件
        output_path = os.path.join('output', filename)
        with open(output_path, 'w', encoding='utf-8') as file:
          file.write(markdown_text)







