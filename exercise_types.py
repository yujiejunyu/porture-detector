import numpy as np
from body_angle import BodyPartAngle
from utils import *


class TypeOfExercise(BodyPartAngle):
    def __init__(self, landmarks):
        super().__init__(landmarks)

    # 计算俯卧撑
    def push_up(self, counter, status):
        # 获取左臂角度
        left_arm_angle = self.angle_of_the_left_arm()
        # 获取右臂角度
        right_arm_angle = self.angle_of_the_left_arm()
        # 计算平均臂角度
        avg_arm_angle = (left_arm_angle + right_arm_angle) // 2

        # 如果状态为真
        if status:
            # 如果平均臂角度小于70
            if avg_arm_angle < 70:
                # 计数器加1
                counter += 1
                # 状态设为假
                status = False
        # 如果状态为假
        else:
            # 如果平均臂角度大于160
            if avg_arm_angle > 160:
                # 状态设为真
                status = True

        # 返回计数器和状态
        return [counter, status]

    # 计算引体向上
    def pull_up(self, counter, status):
        # 获取鼻子坐标
        nose = detection_body_part(self.landmarks, "NOSE")
        # 获取左肘坐标
        left_elbow = detection_body_part(self.landmarks, "LEFT_ELBOW")
        # 获取右肘坐标
        right_elbow = detection_body_part(self.landmarks, "RIGHT_ELBOW")
        # 计算肩部平均y坐标
        avg_shoulder_y = (left_elbow[1] + right_elbow[1]) / 2

        # 如果状态为True
        if status:
            # 如果鼻子y坐标大于肩部平均y坐标
            if nose[1] > avg_shoulder_y:
                # 计数器加1
                counter += 1
                # 状态设为False
                status = False

        # 如果状态为False
        else:
            # 如果鼻子y坐标小于肩部平均y坐标
            if nose[1] < avg_shoulder_y:
                # 状态设为True
                status = True

        # 返回计数器和状态
        return [counter, status]

    # 计算深蹲
    def squat(self, counter, status):
        # 获取左腿角度
        left_leg_angle = self.angle_of_the_right_leg()
        # 获取右腿角度
        right_leg_angle = self.angle_of_the_left_leg()
        # 计算平均腿角度
        avg_leg_angle = (left_leg_angle + right_leg_angle) // 2

        # 如果状态为True
        if status:
            # 如果平均腿角度小于70
            if avg_leg_angle < 70:
                # 计数器加1
                counter += 1
                # 状态设为False
                status = False
        # 如果状态为False
        else:
            # 如果平均腿角度大于160
            if avg_leg_angle > 160:
                # 状态设为True
                status = True

        # 返回计数器和状态
        return [counter, status]

    # 计算行走
    def walk(self, counter, status):
        # 检测右膝盖
        right_knee = detection_body_part(self.landmarks, "RIGHT_KNEE")
        # 检测左膝盖
        left_knee = detection_body_part(self.landmarks, "LEFT_KNEE")

        # 如果状态为True
        if status:
            # 如果左膝盖的x坐标大于右膝盖的x坐标
            if left_knee[0] > right_knee[0]:
                # 计数器加1
                counter += 1
                # 状态变为False
                status = False

        # 如果状态为False
        else:
            # 如果左膝盖的x坐标小于右膝盖的x坐标
            if left_knee[0] < right_knee[0]:
                # 计数器加1
                counter += 1
                # 状态变为True
                status = True

        # 返回计数器和状态
        return [counter, status]

    # 计算仰卧起坐
    def sit_up(self, counter, status):
        # 获取腹部角度
        angle = self.angle_of_the_abdomen()
        # 如果状态为True
        if status:
            # 如果角度小于55
            if angle < 55:
                # 计数器加1
                counter += 1
                # 状态设为False
                status = False
        # 如果状态为False
        else:
            # 如果角度大于105
            if angle > 105:
                # 状态设为True
                status = True

        # 返回计数器和状态
        return [counter, status]

    # 计算指定类型的运动
    def calculate_exercise(self, exercise_type, counter, status):
        # 根据传入的运动类型，调用相应的运动函数
        if exercise_type == "push-up":
            # 调用俯卧撑函数
            counter, status = TypeOfExercise(self.landmarks).push_up(
                counter, status)
        elif exercise_type == "pull-up":
            # 调用引体向上函数
            counter, status = TypeOfExercise(self.landmarks).pull_up(
                counter, status)
        elif exercise_type == "squat":
            # 调用深蹲函数
            counter, status = TypeOfExercise(self.landmarks).squat(
                counter, status)
        elif exercise_type == "walk":
            # 调用步行函数
            counter, status = TypeOfExercise(self.landmarks).walk(
                counter, status)
        elif exercise_type == "sit-up":
            # 调用仰卧起坐函数
            counter, status = TypeOfExercise(self.landmarks).sit_up(
                counter, status)

        # 返回计数器和状态
        return [counter, status]
