import mediapipe as mp
import pandas as pd
import numpy as np
import cv2

# 导入mediapipe库，用于人体姿态估计
# 导入pandas库，用于数据处理
# 导入numpy库，用于数学计算
# 导入cv2库，用于图像处理

mp_pose = mp.solutions.pose


# 定义计算角度的函数
def calculate_angle(a, b, c):
    # 将输入的三个点转换为numpy数组
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    # 计算三个点之间的角度
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
              np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    # 如果角度大于180度，则将其转换为小于180度的角度
    if angle > 180.0:
        angle = 360 - angle

    return angle


# 定义检测身体部位的函数
def detection_body_part(landmarks, body_part_name):
    # 返回指定身体部位的位置和可见性
    return [
        landmarks[mp_pose.PoseLandmark[body_part_name].value].x,
        landmarks[mp_pose.PoseLandmark[body_part_name].value].y,
        landmarks[mp_pose.PoseLandmark[body_part_name].value].visibility
    ]


# 定义检测所有身体部位的函数
def detection_body_parts(landmarks):
    # 创建一个空的DataFrame，用于存储所有身体部位的位置和可见性
    body_parts = pd.DataFrame(columns=["body_part", "x", "y"])

    # 遍历所有身体部位
    for i, lndmrk in enumerate(mp_pose.PoseLandmark):
        # 将身体部位名称转换为字符串
        lndmrk = str(lndmrk).split(".")[1]
        # 调用detection_body_part函数，获取指定身体部位的位置和可见性
        cord = detection_body_part(landmarks, lndmrk)
        # 将身体部位的位置和可见性添加到DataFrame中
        body_parts.loc[i] = lndmrk, cord[0], cord[1]

    return body_parts


# 定义显示计分表的函数
def score_table(exercise, frame, counter, status):
    # 在图像上显示活动名称
    cv2.putText(frame, "Activity : " + exercise.replace("-", " "),
                (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2,
                cv2.LINE_AA)
    # 在图像上显示计数器
    cv2.putText(frame, "Counter : " + str(counter), (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
    # 在图像上显示状态
    cv2.putText(frame, "Status : " + str(status), (10, 135),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
    # 返回显示计分表的图像
    return frame
