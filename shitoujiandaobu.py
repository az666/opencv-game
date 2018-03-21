# coding=utf-8
# -*- coding: cp936 -*-
###资源网址：http://blog.csdn.net/u013480370/article/details/38389089 这位大哥的时python2.7，不适用于现在的3.0+
# 并不能用，经过我以下的修改，可以了。本人博客：wenzheng.club
import cv2
import numpy
import time
import random
import os
def judge():
    # 构造一个3×3的结构元素
    # return 0 stone ,1 jiandao, 2 bu
    img = cv2.imread("wif.jpg", 0)
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
    dilate = cv2.dilate(img, element)
    erode = cv2.erode(img, element)
    # 将两幅图像相减获得边，第一个参数是膨胀后的图像，第二个参数是腐蚀后的图像
    result = cv2.absdiff(dilate, erode);
    # 上面得到的结果是灰度图，将其二值化以便更清楚的观察结果
    retval, result = cv2.threshold(result, 40, 255, cv2.THRESH_BINARY);
    # 反色，即对二值图每个像素取反
    result = cv2.bitwise_not(result);
    """
python-opencv图像的位操作：图像与运算cv2.bitwise_and，图像或运算cv2.bitwise_or，图像非运算cv2.bitwise_not与图像异或运算cv2.bitwise_xor。

1）图像与运算-cv2.bitwise_and(src1, src2, dst=None, mask = None)

2）图像或运算-cv2.bitwise_or(src1, src2, dst=None, mask = None)

3）图像非运算-cv2.bitwise_not(src1, src2, dst=None, mask = None)

图像非运算的效果：一个二值图，将黑色转为白色，白色转为黑色。
    """
    result = cv2.medianBlur(result, 23)
    #cv2.imshow("test",result)
    """
这里介绍非线性过滤器——中值滤波器。
由于中值滤波器对消除椒盐现象特别有用。所以我们使用第二篇教程中椒盐函数先对图像进行处理，将处理结果作为示例图片。
调用中值滤波器的方法与调用其他滤波器的方法类似，如下：
result = cv2.medianBlur(image,5)  
函数返回处理结果，第一个参数是待处理图像，
第二个参数是孔径的尺寸，一个大于1的奇数。
比如这里是5，中值滤波器就会使用5×5的范围来计算。即对像素的中心值及其5×5邻域组成了一个数值集，对其进行处理计算，当前像素被其中值替换掉。
    """
    a = []
    posi = []
    width = []
    count = 0
    area = 0
    #这个大神的计算方法，我一时也解析不出来，应该是依靠手势面积来计算的
    for i in range(result.shape[1]):
        for j in range(result.shape[0]):
            if (result[j][i] == 0):
                area += 1
    for i in range(result.shape[1]):
        if (result[5 * result.shape[0] // 16][i] == 0 and result[5 * result.shape[0] // 16][i - 1] != 0):
            count += 1
            width.append(0)
            posi.append(i)
        if (result[5 * result.shape[0] // 16][i] == 0):
            width[count-1]+= 1    # 如果在这里报错，是因为背景问题，请让手的背景尽量整洁
    #这里是调试用的代码可以注释掉
    print ('the pic width is ',result.shape[1],'\n')
    for i in range(count): 
        print ('the ',i,'th',' ','is')
        print ('width ',width[i] )
        print ('posi ',posi[i],'\n')
    print (count,'\n')
    print ('area is ',area,'\n')
    cv2.line(result,(0,5*result.shape[0]//16),(214,5*result.shape[0]//16),(0,0,0))
    cv2.namedWindow("fcuk") 
    cv2.imshow("fcuk",result) 
    cv2.waitKey(0) 
    #这里是调试用的代码可以注释掉
    # 判定时间
    width_length = 0
    width_jiandao = True
    for i in range(count):
        if width[i] > 45:
            # print 'bu1';
            return 2;
        if width[i] <= 20 or width[i] >= 40:
            width_jiandao = False
        width_length += width[i]
    if width_jiandao == True and count == 2:
        return 1;
    if (area < 8500):
        print ('shi tou')
        return 0;
    print("width_leng", width_length)
    if (width_length < 35):
        # 这个时候说明照片是偏下的，所以需要重新测定。
        a = []
        posi = []
        width = []
        count = 0
        for i in range(result.shape[1]):
            if (result[11 * result.shape[0] // 16][i] == 0 and result[11 * result.shape[0] // 16][i - 1] != 0):
                count += 1
                width.append(0)
                posi.append(i)
            if (result[11 * result.shape[0] // 16][i] == 0):
                width[count - 1] += 1
        """ 
        print 'the pic width is ',result.shape[1],'\n' 
        for i in range(count): 
            print 'the ',i,'th',' ','is'; 
            print 'width ',width[i] 
            print 'posi ',posi[i],'\n' 
        print count,'\n' 
        print 'area is ',area,'\n' 
        """
    width_length = 0
    width_jiandao = True
    for i in range(count):
        if width[i] > 45:
            print ('bu1')
            return 2;
        if width[i] <= 20 or width[i] >= 40:
            width_jiandao = False
        width_length += width[i]
    if width_jiandao == True and count == 2:
        return 1;
    if (area > 14000 or count >= 3):
        print ('bu2')
        return 2;
    if (width_length < 110):
        print ('jian dao')
        return 1;
    else:
        print('bu3')
        return 2;
def game():
    fuck = []
    fuck.append("石头")
    fuck.append("剪刀")
    fuck.append("布")
    capture = cv2.VideoCapture(0)
    cv2.namedWindow("camera", 1)
    start_time = time.time()
    print("给你5秒的时间把手放到方框的位置\n")
    while (1):
        ha, img = capture.read()
        end_time = time.time()
        cv2.rectangle(img, (426, 0), (640, 250), (170, 170, 0))
        cv2.putText(img, str(int((5 - (end_time - start_time)))), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        cv2.imshow("camera", img)
        if (end_time - start_time > 5):
            break
        if (cv2.waitKey(30) >= 0):
            break
    ha, img = capture.read()
    capture.release()
    cv2.imshow("camera", img)
    img = img[0:210, 426:640]
    cv2.imwrite("wif.jpg", img)
    p1 = judge()
    pc = random.randint(0, 2)
    # print p1,' ',pc,'\n'
    print("你出的是", fuck[p1], " 电脑出的是", fuck[pc], "\n")
    cv2.destroyAllWindows()
    if (p1 == pc):
        print("平局\n")
        return 0
    if ((p1 == 0 and pc == 1) or (p1 == 1 and pc == 2) or (p1 == 2 and pc == 0)):
        print('你赢了\n')
        return 1
    else:
        print('你输了\n')
        return -1
def main():
    you_win = 0
    pc_win = 0
    print("这是通过摄像头来玩的剪刀石头布的游戏，请输入回车开始游戏\n")
    #s = raw_input()
    while (1):
        print("比分(玩家：电脑) ", you_win, ":", pc_win, '\n')
        #s = raw_input()
        os.system('cls')
        ans = game()
        if (ans == 1):
            you_win += 1
        elif (ans == -1):
            pc_win += 1
        print("为了减少误判，请尽可能将手占据尽可能大的框框")

main()
#judge()
# #############################################################################
