# 命令
```bash
python main.py ./video/1047_1722233708.mp4 ./video/1048_1722233722.mp4 ./video/result.json
```
参数说明：
- 第一个参数：视频1的路径
- 第二个参数：视频2的路径
- 第三个参数：结果输出路径

# 输出结果

```json
{
    "params": [
        {
            "file_name": "1048_1722233722.mp4",
            "frames": [
                {
                    "pts_time": "0.000000"
                },
                {
                    "pts_time": "0.033333"
                },
                {
                    "pts_time": "0.033335"
                }
            ],
            "is_master": true,
            "pts_num": 3
        },
        {
            "file_name": "1047_1722233708.mp4",
            "frames": [
                {
                    "pts_time": "0.000000"
                },
                {
                    "pts_time": "0.033333"
                },
                {
                    "pts_time": "0.033336"
                },
                {
                    "pts_time": "0.033337"
                }
            ],
            "is_master": false,
            "pts_num": 4
        }
    ],
    "result": {
        "file_order": [
            "1048_1722233722.mp4",
            "1047_1722233708.mp4"
        ],
        "mate_pts": [
            [
                0,
                0
            ],
            [
                0.033333,
                0.033333
            ]
        ]
    }
}
```
```json
{
    "params": [
        {
            // 视频名称
            "file_name": "1048_1722233722.mp4",
            // 视频帧信息
            "frames": [
                {
                    "pts_time": "0.000000"
                },
                {
                    "pts_time": "0.033333"
                },
                {
                    "pts_time": "0.033335"
                }
            ],
            // 是否是主视频，数量少为主视频
            "is_master": true,
            // 视频帧数量
            "pts_num": 3
        },
        {
            // 视频名称
            "file_name": "1047_1722233708.mp4",
            // 视频帧信息
            "frames": [
                {
                    "pts_time": "0.000000"
                },
                {
                    "pts_time": "0.033333"
                },
                {
                    "pts_time": "0.033336"
                },
                {
                    "pts_time": "0.033337"
                }
            ],
            // 是否是主视频，数量多为参考视频
            "is_master": false,
            "pts_num": 4
        }
    ],
    // 匹配结果级别
    "result": {
        // 匹配结果 视频文件名排序，针对 mate_pts 排序
        "file_order": [
            "1048_1722233722.mp4",
            "1047_1722233708.mp4"
        ],
        // 匹配结果，视频文件名排序，针对 mate_pts 排序
        "mate_pts": [
            [
                0,
                0
            ],
            [
                0.033333,
                0.033333
            ]
        ]
    }
}
```