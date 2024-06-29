
from collections import defaultdict
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

output_dir = 'results\\用户行为分析'
def read_danmu_file(file_path):
    """
    读取弹幕文件，解析并返回时间戳和内容的列表。
    假定每一行的格式为“小时:分钟 用户名：内容”
    """
    danmu_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(' ', 1)  # 限制分割次数为1
                if len(parts) < 2:
                    print(f"Skipping malformed line: {line}")
                    continue
                time_str, content = parts
                try:
                    hours, minutes = map(int, time_str.split(':'))
                    timestamp = hours * 3600 + minutes * 60
                    danmu_data.append((timestamp, content))
                except ValueError as e:
                    print(f"Error processing line: {line}, Error: {str(e)}")
                    continue
    return danmu_data

def aggregate_timestamps(danmu_data, interval_minutes=5):
    """
    聚合时间戳，按指定的分钟间隔。
    """
    aggregated_data = defaultdict(int)
    base_time = datetime.min.replace(hour=0, minute=0, second=0)
    for timestamp, content in danmu_data:
        # 聚合到最近的时间间隔
        current_time = base_time + timedelta(seconds=timestamp)
        aggregated_minute = (current_time.minute // interval_minutes) * interval_minutes
        aggregated_time = current_time.replace(minute=aggregated_minute, second=0)
        aggregated_data[aggregated_time] += 1
    return aggregated_data

def generate_visualizations(time_distribution):
    plt.rcParams['font.sans-serif'] = ['SimHei'] # 用微软雅黑显示中文
    plt.rcParams['font.size'] = 10  # 字体大小
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

    """
    生成时间分布的可视化图表，优化横轴标签显示。
    """
    timestamps_sorted = sorted(time_distribution.items())
    timestamps, counts = zip(*timestamps_sorted)
    times = [ts.strftime('%H:%M') for ts in timestamps]

    plt.figure(figsize=(12, 6))
    plt.plot(times, counts, marker='o', linestyle='-', color='b')
    plt.xlabel('时间 (HH:MM)')
    plt.ylabel('弹幕数量')
    plt.title('弹幕时间分布')
    plt.xticks(rotation=90, ticks=range(0, len(times), max(1, len(times) // 10)))  # 显示10个横轴标签
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'user_behavior_analysis.png'), dpi=300, bbox_inches='tight')
    print(f"用户行为分析图表已保存到{os.path.join(output_dir, 'user_behavior_analysis.png')}中\n")
def main(danmu_file):
    danmu_data = read_danmu_file(danmu_file)
    time_distribution = aggregate_timestamps(danmu_data, interval_minutes=5)  # 每5分钟聚合一次
    generate_visualizations(time_distribution)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python user_behavior_analysis.py <danmu_file>")
        sys.exit(1)
    main(sys.argv[1])