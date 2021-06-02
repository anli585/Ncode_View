# coding=utf-8
import cv2
import math
from math import *

class RotateClass:
    '''计算实际旋转角度'''
    def quadrant(self, point):
        endAngle = 0
        try:
            # 直角顶点
            x0 = point[2][0]
            y0 = point[2][1]
            if point[0][0] < point[1][0]:
                x1 = point[0][0]
                y1 = point[0][1]
                x2 = point[1][0]
                y2 = point[1][1]
            else:
                x1 = point[1][0]
                y1 = point[1][1]
                x2 = point[0][0]
                y2 = point[0][1]
            rightAngle = -45
            xDis = x2 - x1
            yDis = y2 - y1
            angle = math.atan2(yDis,xDis)
            angle = angle / math.pi *180
            # 第一种情况 倒立  顶点坐标x,y最大
            if (x0 + 5 > x1 and y0 + 5 > y1) and (x0 + 5 > x2 and y0 + 5 > y2):
                endAngle = angle - 135
                return endAngle

            # 第二种情况 向左 顶点y最小 x最大
            if (x0 + 5 > x1 and y0 - 5 < y1) and (x0 + 5 > x2 and y0 - 5 < y2):
                diff = abs(rightAngle) + abs(angle)
                endAngle = diff
                return endAngle

            # 第三种情况 向右 顶点x最小 y最大
            if (x0 - 5 < x1 and y0 + 5 > y1) and (x0 - 5 < x2 and y0 + 2 > y2):
                diff = rightAngle - abs(angle)
                endAngle = diff
                return endAngle

            # 第四种情况 向右上 顶点x中间 y最大
            if ((x0 + 5 >= x1 and x0 - 5 <= x2) or (x0 - 5 <= x1 and x0 + 5 >= x2)) and (y0 + 5 >= y2 and y0 + 5 >= y1):
                if angle < 0:
                    diff = abs(rightAngle) - abs(angle)
                else:
                    diff = abs(rightAngle) + abs(angle)
                endAngle = diff - 180
                return endAngle

            # 第五种情况 向右下 顶点x最小 y中间
            if (x0 - 5 <= x1 and x0 - 5 <= x2) and ((y0 + 5 >= y1 and y0 - 5 <= y2) or (y0 + 5 >= y2 and y0 - 5 <= y1)):
                diff = abs(rightAngle) - abs(angle)
                if angle < 0:
                    endAngle = diff
                else:
                    endAngle = abs(diff) - 90
                return endAngle

            # 第六种情况 向左上 顶点x最大 y中间
            if (x0 + 5 >= x1 and x0 + 5 >= x2) and ((y0 + 5 >= y1 and y0 - 5 <= y2) or (y0 + 5 >= y2 and y0 - 5 <= y1)):
                diff = abs(rightAngle) - abs(angle)
                if angle < rightAngle:
                    endAngle = 180 + diff
                else:
                    endAngle = 90 - diff
                return endAngle

            # 第六种情况 向左下 顶点x中间 y最小
            if ((x0 + 5 >= x1 and x0 - 5 <= x2) or (x0 - 5 <= x1 and x0 + 5 >= x2) and (y0 - 5 <= y2 and y0 - 5 <= y1)):
                diff = abs(rightAngle) - abs(angle)
                if (angle <= 0) :
                    endAngle =  diff
                else:
                    endAngle = 90 - diff
                return endAngle

            # 第七种情况 正立 顶点x最小 y最小
            if (x0 - 5 < x1 and y0 - 5 < y1) and (x0 - 5 < x2 and y0 - 5 < y2):
                endAngle = angle + abs(angle)
                return endAngle
            return endAngle
        except Exception as ex:
            return endAngle

    '''旋转图片'''
    def do_rotate_image(self, point, img, degree):
        matrixRatio = 2.0
        if img is None:
            return None
        # 旋转中心为图像中心
        h, w = img.shape[:2]
        x0 = point[2][0]
        y0 = point[2][1]
        x = round((x0 / w) * 100, 2)
        y = round((y0 / h) * 100, 2)
        if x < 10 or y < 10:
            matrixRatio = 4.0
        heightNew = int(w * fabs(sin(radians(degree))) + h * fabs(cos(radians(degree))))
        widthNew = int(h * fabs(sin(radians(degree))) + w * fabs(cos(radians(degree))))
        # 计算二维旋转的仿射变换矩阵
        rotateMatrix = cv2.getRotationMatrix2D((w / 2, h / 2), degree, 1)
        # 计算防止旋转被切边
        rotateMatrix[0, 2] += (widthNew - w) / 2
        rotateMatrix[1, 2] += (heightNew - h) / 2
        # 仿射变换，背景色填充为白色*2-int(w/1.5)  *2-int(h/1.5)
        rotate = cv2.warpAffine(img, rotateMatrix, (widthNew, heightNew), borderValue=(255, 255, 255), flags=cv2.INTER_LINEAR)
        return rotate

