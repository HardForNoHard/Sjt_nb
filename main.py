import json
import subprocess
import sys
import os
from datetime import datetime

def load_config():
    with open('config.json', encoding='utf-8') as f:
        return json.load(f)

def run_script(script_name, args):
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    result = subprocess.run([sys.executable, script_path] + args)
    if result.returncode != 0:
        print(f"Error running {script_name} with arguments {args}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <bvid> <date>")
        sys.exit(1)
    
    bvid = sys.argv[1]
    date = sys.argv[2]

    # 验证日期格式
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        sys.exit(1)

    config = load_config()
    headers_file = config['headers_file']
    output_file = config['output_file']
    steps = config['steps']
    scripts = {
        'fetch_danmaku': 'fetch_danmaku.py',
        'user_behavior_analysis': 'user_behavior_analysis.py',
        'sentiment_analysis': 'sentiment_analysis.py',
        'wordcloud_generation': 'wordcloud_generation.py',
        'content_analysis': 'content_analysis.py',
    }

    for step in steps:
        if step == 'fetch_danmaku':
            run_script(scripts[step], [bvid, date, headers_file, output_file])
        else:
            run_script(scripts[step], [output_file])
