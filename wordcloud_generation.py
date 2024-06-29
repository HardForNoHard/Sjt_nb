import jieba
import wordcloud
import imageio
import re
import os

output_dir = 'results\\词云'
def generate_wordcloud(input_file):
    try:
        with open(input_file, encoding='utf-8') as f:
            text = f.read()
        if not text:
            print("No text found in the input file.")
            return
        data = re.findall('.*?([\u4e00-\u9fa5]+).*',text)
        jieba_list = jieba.lcut(str(data))
        jieba_str = ''.join(jieba_list)

        img = imageio.v2.imread("python.png")
        wc = wordcloud.WordCloud(
            width=1000,
            height=700,
            background_color='white',
            font_path='仿宋_GB2312.ttf',
            scale=15,
            mask=img,
        )
        wc.generate(jieba_str)
        wc.to_file(os.path.join(output_dir,'wordcloud.png'))
        print(f"词云图已保存到{os.path.join(output_dir,'wordcloud.png')}中\n")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python wordcloud_generation.py <input_file> ")
        sys.exit(1)
    input_file = sys.argv[1]

    generate_wordcloud(input_file)
