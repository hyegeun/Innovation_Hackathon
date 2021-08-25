import cv2
import os
import argparse
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('--back_img', default = 'festival')
opt = parser.parse_args()

#배경사진 왓?
def back_img(img):
    if img =='festival':
        hwlist = back_img1
        return hwlist

    elif img == 'a':
        hwlist = back_img2
        return hwlist

    elif img == 'b':
        hwlist = back_img3
        return hwlist

    elif img == 'v':
        hwlist = back_img4
        return hwlist

def img_resize(width, imgpath):
    person = Image.open(imgpath)
    w, h = person.size
    ratio = width / w
    h = int(ratio * h)
    person = person.resize((int(width), int(h)))
    person.save(imgpath)


back_img1 = [[1200, 0, 1000], [800, 0, 600], [700, 0, 1000]]
back_img2 = [[500, 0, 500]]
back_img3 = []
back_img4 = []

#배경사진
background = cv2.imread('flaskapp/static/images/back_img/%s.jpg' %opt.back_img, 1)
backh = background.shape[0]
hwlist = back_img(opt.back_img)

#사람 사진이 있는 파일
fdir = 'AI/imgconv/process'
fpath = os.listdir(fdir)
filenum = len(fpath) - 1

#사람 사진 하나씩 합성 
for i, name in enumerate(fpath):
    num = filenum - i
    imgpath = ('%s/%s' %(fdir, name))

    img_resize(hwlist[num][0], imgpath)

    person = cv2.imread(imgpath, 1)
    h, w, c = person.shape
    height = backh - hwlist[num][1] - h
    width = hwlist[num][2] - int(w/2)
    
    roi = background[height:height+h, width:width+w]      #배경이미지의 변경할(사람사진을 넣을) 영역
    mask = cv2.cvtColor(person, cv2.COLOR_BGR2GRAY)       #사람사진 흑백처리
    
    #이미지 이진화 => 배경은 검정. 사람은 흰색
    mask[mask[:]==255]=0
    mask[mask[:]>0]=255
    mask_inv = cv2.bitwise_not(mask)                      #mask반전.  => 배경은 흰색. 글자는 검정
    daum = cv2.bitwise_and(person, person, mask=mask)     #마스크와 사람사진 칼라이미지 and하면 사람만 추출됨
    back = cv2.bitwise_and(roi, roi, mask=mask_inv)       #roi와 mask_inv와 and하면 roi에 사람만 검정색으로 됨
    dst = cv2.add(daum, back)                             #사람사진과 사람모양이 뚤린 배경을 합침
    background[height:height+h, width:width+w] = dst      #roi를 제자리에 넣음

    os.remove('%s/%s' %(fdir, name))                                    #사용한 이미지 삭제

#이미지 저장
cv2.imwrite('AI/cartoongan/test_img/test.png', background) 