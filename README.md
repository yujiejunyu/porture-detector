# 🏋️ Posture Detector — 健身动作姿态检测与计数

基于 **MediaPipe Pose** 的人体姿态估计项目，通过摄像头或视频实时检测人体关键点，自动识别并计数 **引体向上、俯卧撑、仰卧起坐、深蹲、行走** 五种常见健身动作，并在画面中实时显示动作类型、完成次数与当前状态。

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Pose-orange)

---

## ✨ 功能特性

- 🧍 **人体姿态估计**：基于 MediaPipe Pose 检测 33 个人体关键点，实时绘制骨架连线
- 📊 **动作自动计数**：内置 5 种健身动作的计数算法（基于关节角度 / 关键点位置判断）
- 🎥 **双模式输入**：支持读取本地视频文件，也支持调用电脑摄像头实时检测
- 📈 **实时反馈**：画面叠加显示当前动作名称、完成次数（Counter）与状态（Status）
- 🖥️ **轻量易用**：命令行启动，零配置文件

## 📁 支持的练习动作

| 动作 | 参数值 | 判断原理 | 演示效果 |
| --- | --- | --- | --- |
| 引体向上 | `pull-up` | 鼻子与肩部平均高度的相对位置 | ![pull-up](output/output%20pull-up.gif) |
| 俯卧撑 | `push-up` | 手臂夹角变化（<70° 计一次） | ![push-up](output/output%20push-up.gif) |
| 仰卧起坐 | `sit-up` | 腹部夹角变化（<55° 计一次） | ![sit-up](output/output%20sit-up.gif) |
| 深蹲 | `squat` | 腿部夹角变化（<70° 计一次） | ![squat](output/output%20squat.gif) |
| 行走 | `walk` | 左右膝盖的 x 坐标交替关系 | ![walk](output/output%20walking%20exercise.gif) |

## 📋 环境要求

- Python 3.7+
- 摄像头（使用实时检测模式时）

## 🛠️ 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/yujiejunyu/porture-detector.git
cd porture-detector

# 2. （推荐）创建虚拟环境
python -m venv venv
# Windows:  venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
```

依赖列表：`opencv-python`、`mediapipe`、`numpy`、`pandas`

## 🚀 使用方法

### 模式一：检测本地视频（`-vs` 指定视频源）

视频文件需放在 `Exercise_Videos/` 目录下：

```bash
# 引体向上
python main.py -t pull-up -vs pull-up.mp4

# 俯卧撑
python main.py -t push-up -vs push-up.mp4

# 仰卧起坐
python main.py -t sit-up -vs sit-up.mp4

# 深蹲
python main.py -t squat -vs squat.mp4

# 行走
python main.py -t walk -vs walk.mp4
```

### 模式二：调用摄像头实时检测（不传 `-vs`）

```bash
python main.py -t pull-up   # 或 push-up / sit-up / squat / walk
```

### 参数说明

| 参数 | 简写 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| `--exercise_type` | `-t` | ✅ 是 | 动作类型：`pull-up` / `push-up` / `sit-up` / `squat` / `walk` |
| `--video_source` | `-vs` | ❌ 否 | 视频文件名（位于 `Exercise_Videos/`）；不传则使用摄像头 |

### 操作提示

- 按键盘 `q` 键退出程序
- 计数规则：完成一次完整动作（如俯卧撑下压至手臂夹角 <70°，再恢复至 >160°）计数 +1

## 📂 项目结构

```
porture-detector/
├── main.py               # 主程序入口：参数解析、视频/摄像头循环、画面渲染
├── body_angle.py         # BodyPartAngle 类：计算手臂/腿部/颈部/腹部等部位角度
├── exercise_types.py     # TypeOfExercise 类：5 种动作的计数算法
├── utils.py              # 工具函数：角度计算、关键点检测、计分表绘制
├── requirements.txt      # 依赖清单
├── Exercise_videos/      # 示例动作视频（pull-up / push-up / sit-up / squat / walk）
└── output/               # 各动作的演示输出 GIF
```

## ⚙️ 工作原理

1. **姿态检测**：`main.py` 逐帧读取视频/摄像头画面，使用 MediaPipe Pose 模型检测人体关键点
2. **角度计算**：`body_angle.py` 根据关键点坐标计算各部位关节角度（手臂、腿部、腹部等）
3. **动作计数**：`exercise_types.py` 针对不同动作，通过关节角度或关键点位置的变化阈值判断一次完整的动作循环，完成一次计数 +1
4. **实时渲染**：在画面上绘制骨架关键点与连线，并叠加显示动作类型、计数与状态

## 📝 注意事项

- 检测时需要保证身体完整出现在画面中，且光线充足、背景尽量简洁，以提高识别准确率
- 示例视频路径中的文件名需与实际文件完全一致（含扩展名）
- 不同动作的计数阈值（如 70°、160°、55°）可在 `exercise_types.py` 中根据个人体感调整

## 📄 License

本项目基于开源学习项目改造，暂未指定开源许可证。如有需要请与作者联系。
