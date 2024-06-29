import os
from snownlp import SnowNLP
import matplotlib.pyplot as plt

output_dir = 'results\\用户情感分析'

def analyze_sentiment(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    results = []
    sentiments = []
    times = []
    for line in lines:
        time, content = line.split(' ', 1)
        blob = SnowNLP(content)
        sentiment = blob.sentiments
        sentiments.append(sentiment)
        times.append(time)
        results.append(f'{time} {content.strip()} Sentiment: {sentiment:.2f}')
    results.sort()
    output_text_file = os.path.join(output_dir,'sentiment.txt')
    output_image_file = os.path.join(output_dir,'sentiment.png')

    # 保存情感分析结果到文本文件
    with open(output_text_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))

    print(f"情感分析结果已保存到 {output_text_file}中\n")
    
    plt.rcParams['font.sans-serif'] = ['SimHei'] # 用微软雅黑显示中文
    plt.rcParams['font.size'] = 10  # 字体大小
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    plt.figure(figsize=(12, 6))
    plt.plot(times, sentiments, marker='o', linestyle='-', color='b')
    plt.xlabel('时间 (分钟:秒)')
    plt.ylabel('情感极性')
    plt.title('弹幕情感分析')
    plt.xticks(rotation=90, ticks=range(0, len(times), max(1, len(times) // 10)))
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_image_file)

    print(f"情感分析图表已保存到 {output_image_file}中\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("用法: python sentiment_analysis.py <输入文件>")
        sys.exit(1)

    input_file = sys.argv[1]
    analyze_sentiment(input_file)
