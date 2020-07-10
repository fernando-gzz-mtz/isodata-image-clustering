

#Author: Fernando Gonzalez Martinez
#Instituto Tecnologico y de Estudios Superiores de Monterrey

import cv2 as cv
import numpy as np
import random
import copy

def RGBDist(src, neigh, thr):
    #remember opencv opens images as GBR
    #dist = G + B + R
    flag = False
    src = src.astype('float64')
    neigh = neigh.astype('float64')
    dist = abs(src[0]-neigh[0])+abs(src[1]-neigh[1])+abs(src[2]-neigh[2])
    if dist < thr:
        flag = True
    return flag


def orderLabels(num1, num2):
    #print(num1, type(num1), num2, type(num2))
    num1 = int(num1)
    num2 = int(num2)
    if num1 > num2:
        return num2, num1
    else:
        return num1, num2


def isodata(RGBim, thr):
    c = 0
    sz = RGBim.shape
    label = 1
    imlabeled = np.zeros([sz[0],sz[1]])
    labels = [1]
    left = False
    up = False

    imlabeled[0,0] = 1 

    print(labels)

    for x in range(0,sz[0]):
        for y in range(0,sz[1]):
            if not(x == 0 and y == 0):
                c = c + 1
                if (x - 1 >= 0) and (x - 1 < sz[0]):
                    up = RGBDist(RGBim[x,y,:], RGBim[x-1,y,:], thr)

                if (y - 1 >= 0) and (y - 1 < sz[1]):
                    left = RGBDist(RGBim[x,y,:], RGBim[x,y-1,:], thr)

                if left == True and up == True:
                    low,high = orderLabels(imlabeled[x-1,y],imlabeled[x,y-1])
                    labels[high-1] = low
                    imlabeled[x,y] = low
                    #print('both')

                elif left == True:
                    imlabeled[x,y] = imlabeled[x,y-1]
                    #print('left')

                elif up == True:
                    imlabeled[x,y] = imlabeled[x-1,y]
                    #print('up')

                elif up == False and left == False:
                    label = label + 1
                    imlabeled[x,y] = label
                    labels.append(label)
                    #print('none')


    return [imlabeled, labels]


f = cv.imread('book.jpg')

#cv.imshow('Color', f)
dim = (128,128)

resized = cv.resize(f, dim)
isoim,labels = isodata(resized,75)
colors = dict()

labels = set()
for x in range(0,dim[0]):
    for y in range(0,dim[1]):
        labels.add(isoim[x,y])


for i in labels:
    colors[i] = np.random.choice(range(256), size=3).astype(np.uint8)

isoimage = copy.copy(resized)

for x in range(0,dim[0]):
    for y in range(0,dim[1]):
        #print(isoim[x,y], colors[int(isoim[x,y])]
        isoimage[x,y,:] = colors[int(isoim[x,y])]
        #print(isoimage[x,y,:])

cv.imshow('resized',resized)
cv.imshow('isoim',isoim)
cv.imshow('isoimage',isoimage)
cv.waitKey(0)
cv.destroyAllWindows()