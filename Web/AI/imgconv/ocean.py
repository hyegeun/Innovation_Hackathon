import cv2
import os
from PIL import Image
import random

#배경사진
background = cv2.imread('flaskapp/static/images/back_img/ocean.jpg', 1)
backh = background.shape[0]  #배경사진 height
backw = background.shape[1]  #배경사진 width

#배경에 들어가는 사람들 face 크기(face height)
facesize = [100, 110, 120, 130]

#사람 사진이 있는 파일 접근
fdir = 'AI/imgconv/process'
fpath = os.listdir(fdir)
filenum = len(fpath)       #사람 수 -1
prosize = facesize[-filenum:]

#사람 face 정보
facedir = 'AI/yolov5/result/exp2'
facepath = os.listdir(facedir)
faceinfo = []

#사람들 face 위치 정보를 faceinfo에 리스트로 저장(x, y, w, h)
for tfile in facepath:
    f = open("%s//%s.txt" %(facedir, tfile[:-4]), 'r')
    fread = f.read()
    face_position = fread.split(" ")
    face_position = face_position[-4:]
    faceinfo.append(face_position)
    os.remove()

#받은 faceinfo를 float형으로 다시 변환시켜줌 
for i in range(4):
    for j in range(4):
        faceinfo[i][j] = float(faceinfo[i][j])

#사진 합성의 첫 시작 좌표
height = 0
width = backw

#사람 사진 하나씩 합성 
for i, name in enumerate(fpath):
    imgpath = ('%s/%s' %(fdir, name))

    person = cv2.imread(imgpath, 1)       #사람 사진 불러옴
    h, w, c = person.shape                #사람 사진 height, width
    faceheight = int(faceinfo[i][3] * h)  #face height 구함 

    ratio = prosize[i] / faceheight      #넣어야할 size와의 비율
    personheight = int(ratio * h)         #사람사진 height 변경
    personwidth = int(ratio * w)          #사람사진 width 변경

    #사람사진 크기 조절
    person = cv2.resize(person, (personwidth, personheight), interpolation = cv2.INTER_LINEAR)
    
    #첫 합성이면 맨 오른쪽에 붙여서 넣어줌 
    if i==0:
        width = width - personwidth
        prewidth = personwidth
    else:
        posw = int(prewidth * faceinfo[i-1][0])   #지금 사람 이전 사람사진의 face left 좌표
        wleft = width - personwidth
        #width가 음수가 되어서는 안됨. 에러남 
        if wleft < 0:
            wleft = 0
        wright = width - personwidth + posw       
        width = random.randrange(wleft, wright)   #범위는 width - w 부터 width - w + posw 까지
        prewidth = personwidth

    #바다 사진에서의 기본 높이 조절
    height = backh - personheight

    roi = background[height:height+personheight, width:width+personwidth]       #배경이미지의 변경할(사람사진을 넣을) 영역
    mask = cv2.cvtColor(person, cv2.COLOR_BGR2GRAY)                             #사람사진 흑백처리

    #이미지 이진화 => 배경은 검정. 사람은 흰색
    mask[mask[:]==255]=0
    mask[mask[:]>0]=255
    mask_inv = cv2.bitwise_not(mask)                                            #mask반전.  => 배경은 흰색. 글자는 검정
    daum = cv2.bitwise_and(person, person, mask=mask)                           #마스크와 사람사진 칼라이미지 and하면 사람만 추출됨
    back = cv2.bitwise_and(roi, roi, mask=mask_inv)                             #roi와 mask_inv와 and하면 roi에 사람만 검정색으로 됨
    dst = cv2.add(daum, back)                                                   #사람사진과 사람모양이 뚤린 배경을 합침
    background[height:height+personheight, width:width+personwidth] = dst       #roi를 제자리에 넣음
    os.remove(imgpath)

#이미지 저장
if !(os.path.isdir('AI/cartoongan/test_img')):
    os.mkdir('AI/cartoongan/test_img')
cv2.imwrite('AI/cartoongan/test_img/result_ocean.png', background) 