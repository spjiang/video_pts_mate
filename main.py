# python 3.9
# example command:
# python main.py ./video/1047_1722233708.mp4 ./video/1048_1722233722.mp4 ./video/result.json
# param1: ./video/1047_1722233708.mp4 视频 1
# param2: ./video/1048_1722233722.mp4 视频 2
# param3: ./video/result.json 结果文件
# Process finished with exit code 0
import os
# os.environ['FFMPEG_BINARY'] = '/Users/jiangshengping/miniconda3/envs/lydcap/bin/ffmpeg'
import subprocess
import sys
import json

from common.common import ConfigReader


def extract_video_json(video_list):
    video_json_list = []
    for video_path in video_list:
        # ffprobe命令和参数
        ffprobe_cmd = [
            'ffprobe',
            '-hide_banner',  # 隐藏横幅
            '-loglevel', 'error',  # 设置日志级别为错误
            '-select_streams', 'v',  # 选择视频流
            '-show_frames',  # 显示帧
            '-show_entries', 'frame=pts_time',  # 显示条目为帧的pts时间
            '-of', 'json=compact=1',  # 输出格式为紧凑的JSON
            video_path  # 输入文件
        ]
        # 将ffprobe命令的输出重定向到文件
        video_json_path = video_path + '.json'
        with open(video_json_path, 'w') as outfile:
            try:
                # subprocess.run() 运行命令，check=True 捕获异常，stdout=subprocess.DEVNULL 不打印输出到控制台
                result = subprocess.run(ffprobe_cmd, stdout=outfile, stderr=subprocess.STDOUT, check=True)
                video_json_list.append(video_json_path)
            except subprocess.CalledProcessError as e:
                print(f"{video_path}:Ffprobe command execution failed: {e}")
                return video_json_list, 1
    return video_json_list, 0


def findSlavePtsRgtIdx(master_pts, slave_pts_times):
    master_pts = master_pts * 1000000
    for slave_pts_idx, slave_pts in enumerate(slave_pts_times):
        slave_pts = slave_pts * 1000000
        if slave_pts == master_pts or slave_pts > master_pts:
            return slave_pts_idx
    return -1


def valid_frame_time():
    # 判断帧时间是否递增
    for video_idx, data_obj in enumerate(result['params']):
        frames_time = []
        for frame in data_obj['frames']:
            if 'pts_time' not in frame.keys():
                print(f"Frame {frame} does not have pts_times")
                return 1
            else:
                frames_time.append(float(frame['pts_time']))
        # 判断是否是递增的
        is_increasing = True
        for i in range(0, len(frames_time) - 1):
            if frames_time[i] > frames_time[i + 1]:
                is_increasing = False
                break
        if is_increasing == False:
            print("Frames are not increasing")
            return 1
        else:
            result['params'][video_idx]['pts_times'] = frames_time
            # 清空原始frames
            result['params'][video_idx]['pts_num'] = len(frames_time)

    file_order = []
    # 初始化最小pts_num的索引和值
    min_pts_num = float('inf')
    min_index = -1

    # 遍历params列表，找到pts_num最小的元素
    for idx, item in enumerate(result['params']):
        if item['pts_num'] < min_pts_num:
            min_pts_num = item['pts_num']
            min_index = idx

    # 将所有is_master设置为False
    for item in result['params']:
        item['is_master'] = False

    # 将最小pts_num对应的is_master设置为True
    if min_index != -1:
        result['params'][min_index]['is_master'] = True
        file_order.append(result['params'][min_index]['file_name'])

    master_pts_times = []
    slave_filename_list = []
    for idx, item in enumerate(result['params']):
        if item['is_master'] == True:
            master_pts_times = result['params'][idx]['pts_times']
            continue
        if item['is_master'] == False:
            slave_filename_list.append(result['params'][idx]['file_name'])

    result_mate_pts = []
    for master_pts_idx, master_pts in enumerate(master_pts_times):
        mate_pts_list = [master_pts]
        for slave_filename in slave_filename_list:
            slave_pts_times = []
            for pts_obj in result['params']:
                if slave_filename == pts_obj['file_name']:
                    slave_pts_times = pts_obj['pts_times']
            if len(slave_pts_times) == 0:
                print("No pts_times")
                continue
            # 特殊处理第一个 pts_time
            if master_pts_idx == 0:
                file_order.append(slave_filename)
                mate_pts_list.append(slave_pts_times[0])
                continue

            rgtIdx = findSlavePtsRgtIdx(master_pts, slave_pts_times)
            if rgtIdx == -1:
                # 找不到大于master_pts的元素,使用最后一个元素
                mate_pts_list.append(slave_pts_times[len(slave_pts_times) - 1])
                continue

            # 找到大于master_pts的第一个元素
            pts_right = slave_pts_times[rgtIdx]
            pts_left = slave_pts_times[rgtIdx - 1]
            right_step = pts_right * 1000000 - master_pts * 1000000
            left_step = master_pts * 1000000 - pts_left * 1000000
            if right_step == 0:
                mate_pts_list.append(pts_right)
                continue
            if right_step < left_step:
                mate_pts_list.append(pts_right)
                continue
            if left_step < right_step:
                mate_pts_list.append(pts_left)
                continue
        result_mate_pts.append(mate_pts_list)

    result['result']['mate_pts'] = result_mate_pts
    result['result']['file_order'] = file_order
    for idx, item in enumerate(result['params']):
        result['params'][idx].pop('pts_times', None)
    with open(result_path, 'w') as outfile:
        json.dump(result, outfile)


if __name__ == '__main__':
    # 示例：创建 ConfigReader 对象并打印配置内容
    config_reader = ConfigReader()
    video_list = []
    # 视频数量
    video_num = 2
    # 判断命令行参数个数 视频 1，视频 2，结果文件 3
    if len(sys.argv) == 4:
        for i in range(1, len(sys.argv) - 1):
            video_list.append(sys.argv[i])
        json_list, err_code = extract_video_json(video_list)
        if err_code == 1:
            print(" JSON extraction failed")
            quit(1)

        result_path = sys.argv[3]
        # 读取json文件
        result = {
            'params': [],
            'result': {
                'file_order': [],
                'mate_pts': []
            }
        }
        for i in range(0, len(json_list)):
            with open(json_list[i], 'r', encoding='utf-8') as file:
                data = json.load(file)
                file_name = os.path.splitext(os.path.basename(json_list[i]))[0]
                param_dict = {
                    "file_name": file_name,
                    "frames": data['frames'],
                    "pts_times": [],
                    "is_master": False,
                    "pts_num": 0,
                }
                result['params'].append(param_dict)
            if i == video_num:
                break

        valid_frame_time()
        quit(0)
    else:
        print("Please input two video files")
        quit(1)
