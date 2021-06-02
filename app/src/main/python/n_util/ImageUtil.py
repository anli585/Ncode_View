# coding=utf-8
import cv2
import math
import numpy as np
from math import *
from PIL import Image, ImageStat
from n_util.PointUtil import PointClass
from n_util.RotateUtil import RotateClass


class ImageClass():

    def test_util(self, a, b, c):
        return PointClass().count_test(a, b, c)

    '''亮化图片'''
    def contrast_and_brightness(self, alpha, beta, img):
        blank = np.zeros(img.shape, img.dtype)
        dst = cv2.addWeighted(img, alpha, blank, 1 - alpha, beta)
        return dst

    '''获取定位点坐标信息'''
    def get_location_point(self, image, locationPointW, locationPointH, closeItera):
        # 检测定位点信息
        locationPlist = []
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=closeItera)
        gray = cv2.cvtColor(opening, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        sourceImage = opening.copy()
        for i in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[i])
            if w >= locationPointW[0] and h >= locationPointH[0] and w <= locationPointW[1] and h <= locationPointH[1]:
                locationPlist.append([x, y, w, h])
                cv2.rectangle(sourceImage, (x, y), (x + w, y + h), (255, 0, 255), 1)
        if locationPlist:
            locationPlist.sort(reverse=False)
        return locationPlist, sourceImage

    '''过滤有效数据区'''
    def filter_point(self, locationPlist):
        nList = []
        NList = []
        # 过滤有效数据区
        for i in range(len(locationPlist)):
            lp = locationPlist[i]
            for j in range(i + 1, len(locationPlist)):
                rp = locationPlist[j]
                if ((rp[0] - lp[0]) > 100 and (rp[0] - lp[0]) < 320 and (rp[1] - lp[1]) > 100 and (
                        rp[1] - lp[1]) < 320):
                    nList.append([lp, rp])
        if nList:
            for i in range(len(nList)):
                if i > 0:
                    prev = nList[i - 1][0]
                    curr = nList[i][0]
                    if prev == curr:
                        if str(prev) not in str(NList):
                            NList.append(nList[i - 1])
                    else:
                        if str(curr) not in str(NList):
                            NList.append(nList[i])
            if len(NList) == 0:
                NList = nList
        return NList


    '''切割N码'''
    def cut_n_code(self, image, locationPointW, locationPointH, closeItera, isOk):
        # try:
        # 检测定位点信息
        locationPlist, sourceImage = self.get_location_point(image, locationPointW, locationPointH, closeItera)
        NList = self.filter_point(locationPlist)
        # 如果未确定点阵区域，重新调整迭代次数
        if len(NList) == 0:
            locationPlist, sourceImage = self.get_location_point(image, locationPointW, locationPointH, 4)
            NList = self.filter_point(locationPlist)
        # 验证有效数据区
        for item in NList:
            dataAreaList = []
            minx = item[0][0] - 3
            maxx = item[1][0] + item[1][2] + 2
            miny = item[0][1] - 3
            maxy = item[1][1] + item[1][3] + 2
            if isOk:
                subImage = image.copy()
            else:
                subImage = image.copy()[miny: maxy, minx: maxx]
            # 检测有效点阵
            # pContours, opening, opening_point = self.check_location_point(subImage.copy(), 1.0, 1)
            gray = cv2.cvtColor(subImage, cv2.COLOR_BGR2GRAY)
            pContours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # 点阵宽高集合，计算平均点阵宽高
            widthList = []
            heightList = []
            returnContours = []
            for i in range(len(pContours)):
                x, y, w, h = cv2.boundingRect(pContours[i])
                if w < locationPointW[1] and h < locationPointH[1]:
                    widthList.append(w)
                    heightList.append(h)
            avgW = np.mean(widthList)
            avgH = np.mean(heightList)
            for i in range(len(pContours)):
                x, y, w, h = cv2.boundingRect(pContours[i])
                if w < locationPointW[1] and h < locationPointH[1]:
                    if (w >= avgW - 2) and (h >= avgH - 2):
                        dataAreaList.append([x, y, w, h])
                        returnContours.append(pContours[i])
                        # cv2.rectangle(subImage, (x, y), (x + w, y + h), (255, 255, 0), 1)
            dataAreaList.sort(reverse=False)
            # 计算定位点坐标
            locationPlist = self.count_location_point_coor(NList, isOk)
            # 判断点阵是否与预测一致（48/-1 数据点阵+6位定位点阵）
            if len(dataAreaList) >= 46 and len(dataAreaList) <= 54:
                return subImage, locationPlist, dataAreaList, returnContours
            else:
                continue
        return subImage, locationPlist, None, None
        # except Exception as ex:
        #     return None, None, None, None
			
    '''获取图片亮度'''
    def image_brightness(self, img):
        image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        stat = ImageStat.Stat(image)
        r, g, b = stat.rms
        return math.sqrt(0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2))

    '''----------------------------------------------------------------------------------'''
    '''检测轮廓'''
    def detecte(self, image):
        try:
            '''提取所有轮廓'''
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, gray = cv2.threshold(gray, 0, 1, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
            contours, hierachy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            return contours, hierachy
        except Exception as ex:
            return None, None

    '''检测图片中定位点'''
    def check_location_point(self, image, alpha, beta, closeItera):
        try:
            image = self.contrast_and_brightness(alpha, beta, image.copy())
            dst = cv2.fastNlMeansDenoisingColored(image, None, 3, 3, 7, 2)
            dst[dst > 160] = 255
            contours, hierarchy = self.detecte(dst)
            cv2.drawContours(dst, contours, -1, (0, 0, 0), 3)
            dst[dst > 5] = 255
            kernel = np.ones((3, 3), np.uint8)
            opening = cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernel, iterations=closeItera)
            gray = cv2.cvtColor(opening, cv2.COLOR_BGR2GRAY)
            opening_point = cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernel, iterations=(closeItera-3))
            contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            return contours, opening, opening_point
        except Exception as ex:
            return None, None, None

    '''根据图像缩放进行定位点坐标区域计算'''
    def count_location_point_coor(self, locationPlist, isOk):
        newLocationPlist = []
        if locationPlist:
            locationPlist.sort(reverse=False)
            x_value = locationPlist[0][0][0]
            y_value = locationPlist[0][0][1]
            if isOk:
                x_value = locationPlist[0][0][0] - 10
                y_value = locationPlist[0][0][1] - 10
            for item in locationPlist[0]:
                x, y, w, h = item
                # 相对计算，将x->0、y->0
                newLocationPlist.append([x - x_value, y - y_value, w, h])
        return newLocationPlist

    '''过滤顶点坐标区域信息'''
    def filter_location_point(self, locationArealist, dataAreaPointList):
        try:
            if locationArealist is None or  dataAreaPointList is None:
                return None, None
            locationArealist.sort(reverse=False)
            dataAreaPointList.sort(reverse=False)
            leftTopPoint, rightBottomPoint = [],[]
            if len(locationArealist) == 2:
                x1, y1, w1, h1 = locationArealist[0]
                x2, y2, w2, h2 = locationArealist[1]
            for dataPoint in dataAreaPointList:
                x, y, w, h = dataPoint
                if (x >= x1 and x <= x1 + w1) and (y >= y1 and y <= y1 + h1):
                    leftTopPoint.append(dataPoint)
                if (x >= x2 and x <= x2 + w2) and (y >= y2 and y <= y2 + h2):
                    rightBottomPoint.append(dataPoint)
            if len(leftTopPoint) == 3:
                leftTopPoint.sort(reverse=False)
                rightBottomPoint.sort(reverse=False)
                return leftTopPoint, rightBottomPoint
            return None, None
        except Exception as ex:
            return None, None

    '''查找数据点阵, 排除定位点'''
    def find_data_point(self, image, contours, locationPlist):
        try:
            imageW, imageH = image.shape[1], image.shape[0]
            dataPointList = []
            leftTopPoint, rightBottomPoint = [], []
            if len(contours) > 0:
                x1, y1, w1, h1 = locationPlist[0]
                x2, y2, w2, h2 = locationPlist[1]
                for i in range(len(contours)):
                    x, y, w, h = cv2.boundingRect(contours[i])
                    if w < imageW/5 and  h< imageH/5:
                        if not ((x > x1 and x < (x1 + w1) and y > y1 and y < (y1 + h1)) or (x > x2 and x < (x2 + w2) and y > y2 and y < (y2 + h2))):
                            dataPointList.append([x, y, w, h])
                        if (x > x1 and x < (x1 + w1) and y > y1 and y < (y1 + h1)):
                            leftTopPoint.append([x, y, w, h])
                        if (x > x2 and x < (x2 + w2) and y > y2 and y < (y2 + h2)):
                            rightBottomPoint.append([x, y, w, h])
            dataPointList.sort(reverse=False)
            return contours, dataPointList, leftTopPoint, rightBottomPoint
        except Exception as ex:
            return None, None, None, None

    '''图像矫正'''
    def image_correct(self, image, alpha, closeItera):
        imageBrightness = self.image_brightness(image)
        beta = -160
        if imageBrightness < 200:
            beta = -50
        # 图像开闭运算
        contours, opening, opening_point = self.check_location_point(image.copy(), alpha, beta, closeItera)
        if contours is None:
            return None, None
        # 检测定位点区域
        locationPlist = []
        for i in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[i])
            if w >= 20 and h >= 20 and w <= 40 and h <= 40:
                locationPlist.append([x, y, w, h])
        if len(locationPlist) == 0:
            return None, None
        locationPlist.sort(reverse=False)
        # 检测符合定位点区域坐标内的，所有点阵轮廓
        gray_point = cv2.cvtColor(opening_point, cv2.COLOR_BGR2GRAY)
        pcontours, phierarchy = cv2.findContours(gray_point, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # 过滤并比较定位区域的点阵信息（选择两线段间接近直角的三个点阵）
        insideAngleList = []
        for item in locationPlist:
            pointList = []
            x1, y1, w1, h1 = item
            for i in range(len(pcontours)):
                x, y, w, h = cv2.boundingRect(pcontours[i])
                if (x >= x1 - 3 and x <= x1 + w1 + 3) and (y >= y1 - 3 and y <= y1 + h1 + 3):
                    pointList.append([x, y, w, h])
            if len(pointList) == 3:
                pointList.sort(reverse=False)
                # 校验三个点是否组成直角三角形
                rec = PointClass().handle_point(pointList)
                # 计算顶点两边夹角
                if rec:
                    insideAngle = PointClass().get_angle(rec)
                    insideAngleList.append([insideAngle, rec])
            else:
                continue
        if len(insideAngleList) < 1:
            return opening_point, image
        # 选择最接近90度夹角的三个定点
        tempPoint = []
        minV = 0
        for i in range(len(insideAngleList)):
            if i > 0:
                if abs(insideAngleList[i][0] - 90) < minV:
                    tempPoint = insideAngleList[i]
            else:
                minV = abs(insideAngleList[i][0] - 90)
                tempPoint = insideAngleList[i]
        # 若是倒立，则旋转
        # 计算倾斜角度
        angle = RotateClass().quadrant(tempPoint[1])
        if abs(angle) > 2.5 and tempPoint[1] is not None:
            # 旋转图片
            rotate = RotateClass().do_rotate_image(tempPoint[1], opening_point.copy(), angle)
            rotateSource = RotateClass().do_rotate_image(tempPoint[1], image, angle)
            return rotate, rotateSource
        return opening_point, image