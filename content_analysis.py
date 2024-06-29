import collections
import matplotlib.pyplot as plt
import os

output_dir = 'results\\内容分析'

def analyze_danmaku(input_file):
    """
    分析弹幕文件，返回分析结果
    :param input_file: 弹幕文件路径
    :param output_file: 分析结果文件路径
    """
    try:
        # 读取文件内容
        with open(input_file, 'r', encoding='utf-8') as f:
            danmaku_lines = f.readlines()
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    # 初始化变量进行分析
    total_danmaku_count = len(danmaku_lines)
    char_count = 0
    word_count = collections.Counter()
    longest_danmaku = ''
    shortest_danmaku = None
    time_distribution = collections.Counter()
    
    for line in danmaku_lines:
        try:
            # 按照格式解析每一行
            time_str, danmaku = line.split(' ', 1)
            time_parts = time_str.split(':')
            minute = int(time_parts[0])
            
            # 更新时间分布
            time_distribution[minute] += 1
            
            # 更新字符数
            danmaku = danmaku.strip()
            char_count += len(danmaku)
            
            # 更新最长和最短弹幕
            if len(danmaku) > len(longest_danmaku):
                longest_danmaku = danmaku
            if shortest_danmaku is None or len(danmaku) < len(shortest_danmaku):
                shortest_danmaku = danmaku
            
            # 统计词频
            words = danmaku.split()
            word_count.update(words)
        except Exception as e:
            print(f"Error processing line: {line}. Error: {e}")
            continue
    
    # 找到出现频率最高的词语
    most_common_word = word_count.most_common(1)[0] if word_count else ("无", 0)
    
    try:
        # 写入文件
        with open(os.path.join(output_dir, '内容分析.txt'), 'w', encoding='utf-8') as f:
            f.write("每分钟弹幕数量分布:\n")
            for minute, count in sorted(time_distribution.items()):
                f.write(f"第 {minute} 分钟: {count} 条弹幕\n")
            f.write(f"弹幕总数: {total_danmaku_count}\n")
            f.write(f"总字符数: {char_count}\n")
            f.write(f"平均每条弹幕字符数: {char_count / total_danmaku_count if total_danmaku_count > 0 else 0:.2f}\n")
            f.write(f"最长的弹幕: {longest_danmaku}\n")
            f.write(f"最短的弹幕: {shortest_danmaku}\n")
            f.write(f"最常见的词语: {most_common_word[0]} (出现 {most_common_word[1]} 次)\n")
            print(f"总内容分析文本已保存到{os.path.join(output_dir, 'content_analysis.txt')}中\n")
    except Exception as e:
        print(f"Error writing output file: {e}")
    
    # 生成图表并保存
    generate_plots(total_danmaku_count, char_count, time_distribution, most_common_word)

def generate_plots(total_danmaku_count, char_count, time_distribution, most_common_word):
    """
    生成分析结果的图表
    :param total_danmaku_count: 弹幕总数
    :param char_count: 字符总数
    :param time_distribution: 每分钟弹幕数量分布
    :param most_common_word: 最常见的词语
    """
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    
    # 创建保存图片的文件夹
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 弹幕数量和字符数
    plt.figure(figsize=(10, 6))
    plt.bar(['弹幕总数', '字符总数'], [total_danmaku_count, char_count], color=['blue', 'green'])
    plt.title('弹幕总数和字符总数')
    plt.ylabel('数量')
    plt.savefig(os.path.join(output_dir, 'danmaku_char_count.png'), dpi=300, bbox_inches='tight')
    print(f"弹幕和字符数已保存到{os.path.join(output_dir, 'danmaku_char_count.png')}中\n")
    
    # 每分钟弹幕数量分布
    plt.figure(figsize=(10, 6))
    minutes = list(time_distribution.keys())
    counts = list(time_distribution.values())
    plt.bar(minutes, counts, color='purple')
    plt.title('每分钟弹幕数量分布')
    plt.xlabel('分钟')
    plt.ylabel('弹幕数量')
    plt.savefig(os.path.join(output_dir, 'danmaku_distribution.png'), dpi=300, bbox_inches='tight')
    print(f"每分钟弹幕数量分布已保存到{os.path.join(output_dir, 'danmaku_distribution.png')}中\n")
    
    # 最常见的词语
    plt.figure(figsize=(10, 6))
    plt.bar([most_common_word[0]], [most_common_word[1]], color='orange')
    plt.title('最常见的词语')
    plt.ylabel('数量')
    plt.savefig(os.path.join(output_dir, 'most_common_word.png'), dpi=300, bbox_inches='tight')
    print(f"最常见的词语已保存到{os.path.join(output_dir, 'most_common_word.png')}中\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python content_analysis.py <input_file> <output_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    analyze_danmaku(input_file)
