import cv2
import argparse
from utils import *
import mediapipe as mp
from body_angle import BodyPartAngle
from exercise_types import TypeOfExercise

# 创建一个ArgumentParser对象
ap = argparse.ArgumentParser()
# 添加一个参数，用于指定要进行的活动类型
ap.add_argument(
    "-t", "--exercise_type", type=str, help="Type of activity to do", required=True
)
# 添加一个参数，用于指定视频源
ap.add_argument(
    "-vs", "--video_source", type=str, help="Type of activity to do", required=False
)
# 解析参数
args = vars(ap.parse_args())

# 解析参数
args = vars(ap.parse_args())

# 导入绘图工具
mp_drawing = mp.solutions.drawing_utils
# 导入姿态估计工具
mp_pose = mp.solutions.pose

# 如果参数中指定了视频源，则打开该视频源
if args["video_source"] is not None:
    cap = cv2.VideoCapture("Exercise_Videos/" + args["video_source"])
else:
    cap = cv2.VideoCapture(0)  # 否则打开摄像头

# 设置视频宽度为800
cap.set(3, 800)
# 设置视频高度为480
cap.set(4, 480)
# 设置媒体管道
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    counter = 0  # 运动
    status = True  # 移动状态
    while cap.isOpened():
        ret, frame = cap.read()
        # result_screen = np.zeros((250, 400, 3), np.uint8)

        # 将帧重新调整大小
        frame = cv2.resize(frame, (800, 480), interpolation=cv2.INTER_AREA)
        # 将帧重新着色为RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        # 检测
        results = pose.process(frame)
        # 重新着色回BGR
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        try:
            # 获取地标
            landmarks = results.pose_landmarks.landmark
            # 计算运动
            counter, status = TypeOfExercise(landmarks).calculate_exercise(
                args["exercise_type"], counter, status
            )
        except:
            pass

        # 显示分数表
        frame = score_table(args["exercise_type"], frame, counter, status)

        # 渲染检测（用于地标）
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(174, 139, 45), thickness=2, circle_radius=2),
        )

        # 显示视频
        cv2.imshow("Video", frame)
        # 按下q键退出
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    # 释放媒体管道
    cap.release()
    # 关闭所有窗口
    cv2.destroyAllWindows()
