# coding=utf-8
import base64
import cv2
import numpy as np
from math import *
from n_util.ImageUtil import ImageClass
from n_util.PointUtil import PointClass
from n_util.RotateUtil import RotateClass

'''亮化图片'''
def contrast_and_brightness(alpha, beta, img):
    blank = np.zeros(img.shape, img.dtype)
    dst = cv2.addWeighted(img, alpha, blank, 1 - alpha, beta)
    return dst

'''解析图片'''
def parse_image(image):
    try:
        # 放射变换得到倒立或者正立的图像
        rotateImage, sourceImage = ImageClass().image_correct(image, 2.0, 3)
        if rotateImage is None:
            return -2
        # 确定数据有效区（dataImage 正立或者倒立）
        dataImage, locationPlist, dataAreaList, contours = ImageClass().cut_n_code(rotateImage, [15, 25], [15, 25], 3, False)
        if dataAreaList is None:
            return -1
        # 根据点阵信息+顶点区域信息计算顶点6个点坐标信息
        leftTopPoint, rightBottomPoint = ImageClass().filter_location_point(locationPlist, dataAreaList)
        if leftTopPoint is None:
            return 0
        # 判断顶点坐标信息确定是否倒立
        # 校验顶点
        rec = PointClass().handle_point(leftTopPoint)
        if rec is None:
            return 1
        # 若是倒立，则旋转
        # 计算倾斜角度
        angle = RotateClass().quadrant(rec)
        # 开始旋转
        if abs(angle) >= 100:
            angle = angle - 0
            # 旋转
            rotate = RotateClass().do_rotate_image(rec, dataImage.copy(), angle)
            dataImage = rotate.copy()
        # 对源图像进行四周扩充，防止开运算图像粘连
        dataImage = cv2.copyMakeBorder(dataImage, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        dataImage_opening, locationPlist, dataAreaList, contours = ImageClass().cut_n_code(dataImage, [15, 25], [15, 25], 3, True)
        # 查找有效数据
        if dataAreaList is not None:
            # 分解定位点坐标和有效数据点坐标
            contours, dataPointList, leftTopPoint, rightBottomPoint = ImageClass().find_data_point(dataImage, contours, locationPlist)
            # 确定数据读取范围
            tempPoint = leftTopPoint.copy()
            tempPoint.append(rightBottomPoint[0])
            tempPoint.append(rightBottomPoint[1])
            tempPoint.append(rightBottomPoint[2])
            minx, maxx, miny, maxy = PointClass().find_max_area(tempPoint)
            # 计算点阵平均宽度
            avgW = int((maxx - minx) / 14)
            # 过滤数据点阵
            if dataPointList:
                # 重新计算点阵坐标信息，统一x轴坐标
                dataPointList = PointClass().re_count_datapoint(dataPointList)
                sectionCoorList, isAdd = PointClass().new_handle_key(dataPointList, avgW)
                # 按列分组
                if not sectionCoorList:
                    return 2
                if len(dataPointList) == 47 or len(dataPointList) == 48:
                    # 分析数据点阵
                    # 读取数据
                    data = PointClass().read_point_data(isAdd, sectionCoorList, dataPointList)
                    return data
                else:
                    newDataPointList = PointClass().datapoint_correcting(sectionCoorList, dataPointList)
                    if newDataPointList:
                        data = PointClass().read_point_data(False, sectionCoorList, newDataPointList)
                        return data
        return 3
    except Exception as ex:
        return ex

        
'''开始执行图片解析'''
def do_image_parse(imageBase64,path):
    try:
        image = cv2.imread(path)
        cv2.imwrite(imageBase64, image)
        # image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), 1)
        # height, width = image.shape[0], image.shape[1]
        # if image is None:
        #     return 'www'
        # else:
        #     return str(height)+'-'+str(width)
        # decoded_string = base64.b64decode(imageBase64)
        # image = cv2.imdecode(np.frombuffer(decoded_string, np.uint8), cv2.COLOR_RGB2BGR)
        # height, width = image.shape[0], image.shape[1]
        # image_new = cv2.resize(image, (int(width/3), int(height/3)))
        # cv2.imwrite(path, image)
        result = parse_image(image)
        return str(result)+'---------'+str(len(str(result)))
    except Exception as ex:
        return str(ex)

