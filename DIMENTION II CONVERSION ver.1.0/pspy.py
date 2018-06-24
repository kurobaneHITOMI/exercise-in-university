import numpy as np
import skimage.filters.rank as sfr
from skimage.morphology import disk
from skimage import img_as_ubyte
import cv2

class normal_fliter(object):
    
    #最大值滤波
    def max_filter(img,n):
        img = sfr.maximum(img, disk(n))
        return(img_as_ubyte(img))
        
        
    #最小值滤波
    def min_filter(img,n):
        img = sfr.minimum(img, disk(n))
        return(img_as_ubyte(img))
        
        
    #锐化
    def sharpen_filter(img,n):
        if n == 1:
            img = cv2.filter2D(img,-1,np.array([[-1,0,-1],[0,5,0],[-1,0,-1]]))
        if n == 2:
            img = cv2.filter2D(img,-1,np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]]))
        return(img_as_ubyte(img))


    #同态滤波
    def homo_filter(img,filt):
        img1 = img.astype('float')
        img1 = np.log(img1)
        img2 = cv2.filter2D(img1,-1,filt)
        img2 = np.exp(img2)
        return(img_as_ubyte(img2))
        
        
    #二值化
    def thresholding(img,bias):
        img[np.where(img > (255-bias))] = 255
        img[np.where(img < (255-bias))] = 0
        return(img_as_ubyte(img))
    
    
    #油画
    def oil_painting(img,smoothness):
        if smoothness not in range(1,9):
            print('parametre smoothness error')
            return False
        else:
            a = 256/2**smoothness
            img1 = cv2.filter2D(img,-1,1/8*np.ones((3,3)))
            img1 = img1//a * a + a/2
            img1 = img1.astype('int')
        return(img_as_ubyte(img1))

    
    #对比度和亮度
    def contrast_and_brightness(img,a,b):
        img = img.astype('int16')
        img = img * a + b
        img = np.clip(img,0,255)
        img = img.astype('uint8')
        return(img)

class mixed_model(object):
    
    
    # 不透明度
    def Transparent(img_1, img_2, alpha):
        img = img_1 * alpha + img_2 * (1-alpha)
        return(img_as_ubyte(img))


    # 正片叠底
    def Multiply (img_1, img_2):
        img = img_1 * img_2
        return(img_as_ubyte(img))


    # 颜色加深 
    def Color_burn (img_1, img_2):
        img = 1 - (1 - img_2) / (img_1 + 0.001)

        mask_1 = img  < 0 
        mask_2 = img  > 1

        img = img * (1-mask_1)
        img = img * (1-mask_2) + mask_2
        return(img_as_ubyte(img))


    # 颜色减淡
    def Color_dodge(img_1, img_2):
        img = img_2 / (1.0 - img_1 + 0.001)
        mask_2 = img  > 1
        img = img * (1-mask_2) + mask_2          
        return(img_as_ubyte(img)) 


    # 线性加深 
    def Linear_burn(img_1, img_2):
        img = img_1 + img_2 - 1
        mask_1 = img  < 0 
        img = img * (1-mask_1)
        return(img_as_ubyte(img))


    # 线性减淡
    def Linear_dodge(img_1, img_2):
        img = img_1 + img_2
        mask_2 = img  > 1
        img = img * (1-mask_2) + mask_2
        return(img_as_ubyte(img))


    # 变亮
    def Lighten(img_1, img_2):
        img = img_1 - img_2
        mask = img > 0
        img = img_1 * mask + img_2 * (1-mask) 
        return(img_as_ubyte(img))


    # 变暗
    def Dark(img_1, img_2):
        img = img_1 - img_2
        mask = img < 0
        img = img_1 * mask + img_2 * (1-mask)
        return(img_as_ubyte(img))


    # 滤色
    def Screen(img_1, img_2):
        img = 1- (1-img_1)*(1-img_2)
        return(img_as_ubyte(img))


    # 叠加
    def Overlay(img_1, img_2):
        mask = img_2 < 0.5
        img = 2 * img_1 * img_2 * mask + (1-mask) * (1- 2 * (1-img_1)*(1-img_2))
        return(img_as_ubyte(img))


    # 柔光
    def Soft_light(img_1, img_2):
        mask = img_1 < 0.5
        T1 = (2 * img_1 -1)*(img_2 - img_2 * img_2) + img_2
        T2 = (2 * img_1 -1)*(np.sqrt(img_2) - img_2) + img_2
        img = T1 * mask + T2 * (1-mask)
        return(img_as_ubyte(img))


    # 强光
    def Hard_light(img_1, img_2):
        mask = img_1 < 0.5
        T1 = 2 * img_1 * img_2
        T2 = 1 - 2 * (1 - img_1) * (1 - img_2)
        img = T1 * mask + T2 * (1-mask)
        return(img_as_ubyte(img))


    # 亮光
    def Vivid_light(img_1, img_2):
        mask = img_1 < 0.5
        T1 = 1 - (1 - img_2)/(2 * img_1 + 0.001)
        T2 = img_2 / (2*(1-img_1) + 0.001)
        mask_1 = T1 < 0
        mask_2 = T2 > 1
        T1 = T1 * (1-mask_1)
        T2 = T2 * (1-mask_2) + mask_2
        img = T1 * mask  + T2 * (1 - mask) 
        return(img_as_ubyte(img))


    # 点光
    def Pin_light(img_1, img_2):
        mask_1 = img_2 < (img_1 * 2 -1)
        mask_2 = img_2 > 2 * img_1
        T1 = 2 * img_1 -1 
        T2 = img_2
        T3 = 2 * img_1 
        img = T1 * mask_1 + T2 * (1 - mask_1) * (1 - mask_2) + T3 * mask_2
        return(img_as_ubyte(img))


    # 线性光
    def Linear_light(img_1, img_2):
        img = img_2 + img_1 * 2 - 1
        mask_1 = img < 0
        mask_2 = img > 1
        img = img * (1-mask_1)
        img = img * (1-mask_2) + mask_2
        return(img_as_ubyte(img))


    # 实色混合
    def Hard_mix(img_1, img_2):
        img = img_1 + img_2 
        mask = img_1 + img_2 > 1 
        img = img * (1-mask) + mask 
        img = img * mask
        return(img_as_ubyte(img))
    
    #反相
    def invertion(img):
        img = 255 - img
        return(img_as_ubyte(img))