import numpy as np
from PIL import Image
from PIL import ImageFilter
import math
                                    
im = Image.open('./test.jpg')               # 读取的图像数据格式为BGRBGRBGR

img = np.array(im)   
B = np.expand_dims(img[:,:,0], axis=2)
G = np.expand_dims(img[:,:,1], axis=2)
R = np.expand_dims(img[:,:,2], axis=2)
img = np.concatenate((R, G, B), axis = 2) # 将图像转换为 RGBRGBRGB
# np.savetxt("./for_test_origin.txt",img.reshape(-1, img.shape[2]),fmt="%d")
# 注释后是0.29%

import numpy as np
import cv2
# from copy import deepcopy
from PIL import Image

filter_by_principle = True


# #####################中值滤波###########################
# def median_Blur(img, filiter_size = 3):  #当输入的图像为彩色图像
#     image_copy = np.array(img, copy = True).astype(np.uint8)
#     processed = np.zeros_like(image_copy)
#     middle = int(filiter_size / 2)
#     r = np.zeros(filiter_size * filiter_size)
#     g = np.zeros(filiter_size * filiter_size)
#     b = np.zeros(filiter_size * filiter_size)
    
#     for i in range(middle, image_copy.shape[0] - middle):
#         for j in range(middle, image_copy.shape[1] - middle):
#             count = 0
#             #依次取出模板中对应的像素值
#             for m in range(i - middle, i + middle +1):
#                 for n in range(j - middle, j + middle + 1):
#                     r[count] = image_copy[m][n][0]
#                     g[count] = image_copy[m][n][1]
#                     b[count] = image_copy[m][n][2]
#                     count += 1
#             if i+1 == 334 and j+1 == 3:
#                 print("到达目标位置。")
            
#             r.sort()
#             g.sort()
#             b.sort()
#             processed[i][j][0] = b[int(filiter_size*filiter_size/2)]
#             processed[i][j][1] = g[int(filiter_size*filiter_size/2)]
#             processed[i][j][2] = r[int(filiter_size*filiter_size/2)]
#     # processed = np.clip(processed, 0, 255).astype(np.uint8)
#     return processed






# median_blur= median_Blur(img, 3)

# om = im.filter(ImageFilter.RankFilter(3, 4))
# omg = np.array(om)
# R = np.expand_dims(omg[:,:,0], axis=2)
# G = np.expand_dims(omg[:,:,1], axis=2)
# B = np.expand_dims(omg[:,:,2], axis=2)
# blur_filter = np.concatenate((B, G, R), axis = 2) 

# compare = median_blur == blur_filter
# print("result diffs between opencv and c of median_blur_filter:{}, percentage：{:.2f}%"\
#     .format(np.sum(compare == False), np.sum(compare == False)*100/median_blur.size))

# np.savetxt("./my_test_r.txt", median_blur[:,:,0].reshape(median_blur.shape[0], median_blur.shape[1]), fmt="%d")
# np.savetxt("./my_test_g.txt", median_blur[:,:,1].reshape(median_blur.shape[0], median_blur.shape[1]), fmt="%d")
# np.savetxt("./my_test_b.txt", median_blur[:,:,2].reshape(median_blur.shape[0], median_blur.shape[1]), fmt="%d")

if filter_by_principle == True:

    test_one_pos = True   # 检查一个点
    test_for_all = False  # 检查全局


    # 下面写一些手动滤波操作用于验证滤波操作

    kernel_size = 5

    kernel = np.ones((kernel_size,kernel_size))

    kernel = kernel / kernel_size**2 # 均值滤波权重值

    # kernel = np.array([[0.00500788, 0.01729958, 0.02615146, 0.01729958, 0.00500788],
    #    [0.01729958, 0.05976089, 0.09033947, 0.05976089, 0.01729958],
    #    [0.02615146, 0.09033947, 0.13656459, 0.09033947, 0.02615146],
    #    [0.01729958, 0.05976089, 0.09033947, 0.05976089, 0.01729958],
    #    [0.00500788, 0.01729958, 0.02615146, 0.01729958, 0.00500788]])

    origin = R # 滤波的数据

    if test_one_pos == True:

        # 在byondcompar上的行列数
        pos_x = 4
        pos_y = 5

        temp = np.ones((kernel_size,kernel_size))
        res = 0

        for i in range(pos_x-1-int(kernel_size/2),pos_x+int(kernel_size/2)):
            for j in range(pos_y-1-int(kernel_size/2),pos_y+int(kernel_size/2)):
                temp[i-(pos_x-1-int(kernel_size/2))][j-(pos_y-1-int(kernel_size/2))] = origin[i][j]
                res += origin[i][j] * kernel[i-(pos_x-1-int(kernel_size/2))][j-(pos_y-1-int(kernel_size/2))]


        print("原数据为：\n")
        for i in range(0,kernel_size):
            for j in range(0,kernel_size ):
                print("{}\t".format(temp[i][j]))
            print("\n")

        print("kernel为：\n")
        for i in range(0,kernel_size):
            for j in range(0,kernel_size):
                print("{}  ".format(kernel[i][j]))
            print("\n")

        print("滤波结果为：sum = {}\n".format(res))

    if test_for_all == True:

        result = np.copy(origin.astype('float32'))
        

        middle = int(kernel_size/2)

        # 卷积时对外层不做处理
        for i in range(middle,origin.shape[0]-middle):
            for j in range(middle,origin.shape[1]-middle):
                
                res = 0

                for x in range(i-middle,i+middle+1):
                    for y in range(j-middle,j+middle+1):
                        
                        res += origin[x][y] * kernel[x-(i-middle)][y-(j-middle)]
                    

                # 这里可以添加取整的方法
                res = math.floor(res+0.5) # 这里是四舍五入

                result[i][j] = res
        
        # np.savetxt("./filter_by_principle_after_floor.txt", result[:,:].reshape(result.shape[0], result.shape[1]), fmt="%d")
        # np.savetxt("./filter_by_principle.txt", result[:,:].reshape(result.shape[0], result.shape[1]), fmt="%.2f")
        # np.savetxt("./origin_data.txt", origin[:,:].reshape(origin.shape[0], origin.shape[1]), fmt="%d")
        
        om = cv2.GaussianBlur(R, (5, 5), 1.1,1.1)                 #高斯滤波   cv2.GaussianBlur(src, ksize, sigmaX, sigmaY, borderType)
        omg = np.array(om)
        # R = np.expand_dims(omg[:,:,0], axis=2)
        # G = np.expand_dims(omg[:,:,1], axis=2)
        # B = np.expand_dims(omg[:,:,2], axis=2)
        # blur_filter = np.concatenate((B, G, R), axis = 2)                       # BGRBGRBGR==>RGBRGBRGB
        blur_filter = omg
        # np.savetxt("./opencv_result.txt", omg[:,:].reshape(omg.shape[0], omg.shape[1]), fmt="%d")

        result = np.array(result)
        result = result.reshape(1904,1080)
        compare = result == blur_filter
        print("result diffs between opencv and c of gaussian_filter:{}, percentage：{:.2f}%"\
        .format(np.sum(compare == False), np.sum(compare == False)*100/result.size))
    