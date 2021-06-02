# coding=utf-8
import cv2
import math
import numpy as np
from math import *

class PointClass():

    def count_test(self, a, b, c):
        return str((a + b) - c)



    '''二维数组按照下标为1排序'''
    def sort_task(self, elem):
        return elem[1]

    '''图片轮廓检测'''
    def find_contours(self, image):
        try:
            # 图像灰度化处理
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 0,0
            gaus = cv2.GaussianBlur(gray, (7, 7), 0)  # 50, 150
            edges = cv2.Canny(gaus, 0, 10, apertureSize=3)
            contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            return contours, hierarchy
        except Exception as ex:
            return None, None

    '''计算两点距离'''
    def dis(self, p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

    '''封装三个顶点，确定直角顶点'''
    def handle_point(self, rec):
        space_v = 5
        point = []
        distance_1 = np.sqrt((rec[0][0] - rec[1][0]) ** 2 + (rec[0][1] - rec[1][1]) ** 2)
        distance_2 = np.sqrt((rec[0][0] - rec[2][0]) ** 2 + (rec[0][1] - rec[2][1]) ** 2)
        distance_3 = np.sqrt((rec[1][0] - rec[2][0]) ** 2 + (rec[1][1] - rec[2][1]) ** 2)
        if abs(distance_1 - distance_2) < 4:
            if abs(np.sqrt(np.square(distance_1) + np.square(distance_2)) - distance_3) < space_v:
                point.append([rec[1][0], rec[1][1]])
                point.append([rec[2][0], rec[2][1]])
                point.append([rec[0][0], rec[0][1]])
                return point
        elif abs(distance_1 - distance_3) < 4:
            if abs(np.sqrt(np.square(distance_1) + np.square(distance_3)) - distance_2) < space_v:
                point.append([rec[0][0], rec[0][1]])
                point.append([rec[2][0], rec[2][1]])
                point.append([rec[1][0], rec[1][1]])
                return point
        elif abs(distance_2 - distance_3) < 4:
            if abs(np.sqrt(np.square(distance_2) + np.square(distance_3)) - distance_1) < space_v:
                point.append([rec[1][0], rec[1][1]])
                point.append([rec[0][0], rec[0][1]])
                point.append([rec[2][0], rec[2][1]])
                return point
        return None

    '''查找N码范围'''
    def find_max_area(self, pointList):
        minx, maxx, miny, maxy = 0, 0, 0, 0
        if pointList:
            xPointList = pointList.copy()
            yPointList = pointList.copy()
            xPointList.sort(reverse=False)
            yPointList.sort(key=self.sort_task, reverse=False)
            minx = xPointList[0][0] - 2
            maxx = xPointList[len(xPointList) - 1][0] + 10
            miny = yPointList[0][1] - 2
            maxy = yPointList[len(yPointList) - 1][1] + 10
        return  minx, maxx, miny, maxy

    '''按列分组, 合并读取单元为两列的键值对'''
    def handle_key(self, dataPoint, avgW):
        try:
            if dataPoint:
                filterKey = []
                iList = []
                isAdd = False
                dataLen = len(dataPoint)
                # dataPoint
                minxV = 0
                for i in range(dataLen):
                    if i > 0:
                        prev = dataPoint[i - 1]
                        curr = dataPoint[i]
                        if  i < dataLen - 1:
                            after = dataPoint[i + 1]
                        else:
                            after = [-1, -1]
                        if after[0] == -1:
                            iList.append(i)
                        elif abs(curr[0] - minxV) >= avgW and (abs(curr[0] - after[0]) > 5 and abs(curr[0] - after[0])<= avgW):
                            iList.append(i)
                            minxV = after[0]
                    else:
                        minxV = dataPoint[i][0]
                iList.append(dataLen - 1)
                prevIndex = 0
                for key in iList:
                    l1 = dataPoint[prevIndex:key+1]
                    if prevIndex == 0 and len(l1) == 6:
                        filterKey.append([dataPoint[prevIndex][0], dataPoint[key][0]])
                        prevIndex = key + 1
                        isAdd = True
                    elif len(l1) == 7:
                        filterKey.append([dataPoint[prevIndex][0], dataPoint[key][0]])
                        prevIndex = key + 1
                    elif len(l1) == 6 :
                        if key + 1 >= len(dataPoint):
                            filterKey.append([dataPoint[prevIndex][0], dataPoint[len(dataPoint) - 1][0]])
                        else:
                            filterKey.append([dataPoint[prevIndex][0], dataPoint[key + 1][0]])
                        prevIndex = key + 2
                return filterKey, isAdd
            else:
                return None, False
        except Exception as ex:
            return None, False

    '''按列分组, 合并读取单元为两列的键值对(统一x轴坐标后，根据平均宽度以及点阵间距进行分组)'''
    def new_handle_key(self, dataPoint, avgW):
        if dataPoint:
            filterKey = []
            dataPointLen = len(dataPoint)
            minx = 0
            maxx = 0
            tempList = []
            isAdd = False
            for i in range(dataPointLen):
                currItem =  dataPoint[i]
                if i > 0:
                    tempList.append(1)
                    prevItem = dataPoint[i - 1]
                    if abs(currItem[0] - prevItem[0]) >= avgW:
                        if len(tempList) < 7:
                            if i == 6:
                                isAdd = True
                                maxx = prevItem[0]
                                filterKey.append([minx, maxx])
                                tempList = []
                            else:
                                minx = prevItem[0]
                        if i == dataPointLen - 1:
                            maxx = currItem[0]
                            filterKey.append([minx, maxx])
                            tempList = []
                        if len(tempList) == 7:
                            maxx = prevItem[0]
                            filterKey.append([minx, maxx])
                            tempList = []

                    elif abs(currItem[0] - prevItem[0]) > 5 and abs(currItem[0] - prevItem[0]) < avgW:
                        if maxx == 0 and i == 6:
                            isAdd = True
                        maxx = prevItem[0]
                        if [minx, maxx] not in filterKey:
                            filterKey.append([minx, maxx])
                        tempList = []
                    elif i == dataPointLen - 1:
                        maxx = currItem[0]
                        filterKey.append([minx, maxx])
                        tempList = []
            return filterKey, isAdd


    '''读取除定位点外，点阵数据'''
    def read_point_data(self, isAdd,  sectionCoorList, dataPointListCopy):
        try:
            dataList = []
            if isAdd:
                dataList.append(0)
            # 整理数据
            sectionLen = len(sectionCoorList)
            for i in range(sectionLen):
                startIndex = sectionCoorList[i][0]
                endIndex = sectionCoorList[i][1] + 5
                sectionList = []
                for point in dataPointListCopy:
                    if point[0] >= startIndex and point[0] < endIndex:
                        sectionList.append(point)
                sectionList.sort(key=self.sort_task, reverse=False)
                for item in sectionList:
                    if abs(item[0] - startIndex) < abs(item[0] - endIndex):
                        dataList.append(0)
                    else:
                        dataList.append(1)
            # 转换数据
            num = math.ceil(len(dataList) / 4)
            data = ''
            for i in range(num):
                item = dataList[i * 4:(i + 1) * 4]
                item = ''.join([str(x) for x in item])
                data = data + str(int(item, 2))
            return data
        except Exception as ex:
            return None

    class Point:
        """
        2D坐标点
        """
        def __init__(self, x, y):
            self.X = x
            self.Y = y

    class Line:
        def __init__(self, point1, point2):
            """
            初始化包含两个端点
            :param point1:
            :param point2:
            """
            self.Point1 = point1
            self.Point2 = point2

    '''计算线段夹角'''
    def get_angle(self, pointList):
        """
           计算两条线段之间的夹角
           :param line1:
           :param line2:
           :return:
        """
        x0, y0 = pointList[2]
        x1, y1 = pointList[1]
        x2, y2 = pointList[0]
        line1 = self.Line(self.Point(x0, y0), self.Point(x1, y1))
        line2 = self.Line(self.Point(x0, y0), self.Point(x2, y2))

        dx1 = line1.Point1.X - line1.Point2.X
        dy1 = line1.Point1.Y - line1.Point2.Y
        dx2 = line2.Point1.X - line2.Point2.X
        dy2 = line2.Point1.Y - line2.Point2.Y
        angle1 = math.atan2(dy1, dx1)
        angle1 = int(angle1 * 180 / math.pi)
        angle2 = math.atan2(dy2, dx2)
        angle2 = int(angle2 * 180 / math.pi)
        if angle1 * angle2 >= 0:
            insideAngle = abs(angle1 - angle2)
        else:
            insideAngle = abs(angle1) + abs(angle2)
            if insideAngle > 180:
                insideAngle = 360 - insideAngle
        insideAngle = insideAngle % 180
        return insideAngle

    '''重新计算数据点x坐标信息'''
    def re_count_datapoint(self, dataPointList):
        newDataPointList = []
        if dataPointList:
            minx = 0
            for item in dataPointList:
                x = item[0]
                newItem = item
                if abs(x - minx) < 7:
                    newItem[0] = minx
                else:
                    minx = x
                newDataPointList.append(newItem)
        dataPointList = sorted(dataPointList, key=lambda x: (x[0], x[1]))
        return dataPointList


    '''丢失点阵进行纠错，纠错最大值 竖列中丢失点阵数量不能大于2个'''
    def datapoint_correcting(self, sectionCoorList, dataPointList):
        pointList = []
        newPointList = []
        sortDataPointList = dataPointList.copy()
        sortDataPointList.sort(key=self.sort_task, reverse=False)
        miny = sortDataPointList[0][1]
        maxy = sortDataPointList[len(sortDataPointList)-1][1]
        # 按照分组坐标截取7列点阵信息
        if dataPointList:
            for item in sectionCoorList:
                minx = item[0]
                maxx = item[1]
                dataList = []
                for data in dataPointList:
                    if data[0] >= minx and data[0] <= maxx:
                        dataList.append(data)
                pointList.append(dataList)
            # print(pointList)
        # 对每组点阵进行校验，第一列长度为6、7 最后一列长度为6，其余列长度为7
        firstDataList = pointList[:1]
        endDataList = pointList[len(pointList)-1:]
        middleDataList = pointList[1:len(pointList)-1]

        # 计算第一组
        newFirstDataList = self.do_correcting(firstDataList, miny)
        if newFirstDataList:
            for item in newFirstDataList[0]:
                newPointList.append(item)

        # 计算最后一组
        newEndDataList = self.do_correcting(endDataList, miny)
        if newEndDataList:
            for item in newEndDataList[0]:
                newPointList.append(item)

        # 校验剩下5组是否正常
        newMiddleDataList = self.do_correcting(middleDataList, miny)
        if newMiddleDataList:
            for item in newMiddleDataList:
                for subItem in item:
                    newPointList.append(subItem)
        if newPointList:
            newPointList.sort(reverse=False)
            return newPointList
        return None

    '''执行纠错数据'''
    def do_correcting(self, dataList, miny):
        rightDataList = []
        newDataList, errorDataList = self.correct_high(dataList, miny)
        if errorDataList:
            rightDataList = self.correct_diff(errorDataList)
        if newDataList:
            if rightDataList:
                newDataList.append(rightDataList)
            return newDataList
        else:
            return dataList

    '''校验方案二，检查y轴坐标差值是否为连续高值，若是则从中间补入点阵'''
    def correct_diff(self, dataList):
        newDataList = dataList[0].copy()
        dataList.sort(key=self.sort_task, reverse=False)
        diffValueList = []
        for i in range(len(dataList[0])):
            currItem = dataList[0][i]
            if i > 0:
                prevItem = dataList[0][i - 1]
                val = abs(currItem[1] - prevItem[1])
                if val > 35:
                    diffValueList.append([i, prevItem, currItem, val])
        if diffValueList:
            # 计算差值的坐标是否连续
            for i in range(len(diffValueList)):
                currItem = diffValueList[i]
                if i > 0:
                    prevItem = diffValueList[i - 1]
                    diffIndex = abs(currItem[0] - prevItem[0])
                    diffVal = currItem[3] - prevItem[3]
                    if diffIndex == 1 or diffVal > 0:
                        # 判断坐标点，选择插入index
                        if currItem[1][0] >= currItem[2][0]:
                            vv = currItem[1][1] + 12
                            newDataList.append([prevItem[1][0], vv, prevItem[1][2], prevItem[1][3]])
                    elif diffVal < -10:
                        # 判断坐标点，选择插入index
                        if prevItem[1][0] >= prevItem[2][0]:
                            vv = prevItem[1][1] + 12
                            newDataList.append([currItem[1][0], vv, currItem[1][2], currItem[1][3]])
        if newDataList:
            newDataList.sort(reverse=False)
            return newDataList
        return None

    '''校验方案一，检查y轴最小坐标，检查是否上方点阵丢失'''
    def correct_high(self, dataList, miny):
        newDataList = []
        errorDataList = []
        # 校验剩下5组是否正常
        for item in dataList:
            # 计算最小的x轴
            subItem = item.copy()
            subItem.sort(reverse=False)
            minx = subItem[0][0]
            w = subItem[0][2]
            h = subItem[0][3]
            item.sort(key=self.sort_task, reverse=False)
            # 本组最小y轴大于miny，则说明缺少第一位点阵
            if abs(item[0][1] - miny) > 20:
                item.append([minx, miny, w, h ])
            if len(item) == 7:
                item.sort(reverse=False)
                newDataList.append(item)
            else:
                errorDataList.append(item)
        return newDataList, errorDataList















