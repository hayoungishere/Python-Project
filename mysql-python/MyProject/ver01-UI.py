from tkinter import *
from tkinter.filedialog import askopenfilename

import matplotlib as plt
import pymssql
import DBConn
import printM
import Search
from tkinter import ttk, messagebox
import tempfile
from PIL import Image
import numpy as np
import cv2

#Global variables....
global window, variable, fullFrame, canvas, paper

canvas,paper=None, None

IP_ADDR = '192.168.111.130'
DB_NAME = 'khyProject'
USER_NAME = 'root'
USER_PASS = '1234'

window = Tk(); window.title("스타일링 툴(ver 0.0.1")
window.geometry("800x500")
fullFrame=Frame(window); fullFrame.pack()


### Define Functions...
def sear1():
    global variable

    category=variable.get()
    obj = Search.Searching()
    obj.setTable("Cloths")

    # print(obj.getTable())
    query = "select Cloths.mainColor, Category.cname, Cloths.comment from Cloths, Category where Category.cname='" + category + "'"
    obj.setQuery(query)

    print(obj.getQuery())
def menuSearch1():
    ######## MENU 1. 검색 ########

    global variable, fullFrame

    if fullFrame != None :
        fullFrame.destroy()

    fullFrame=Frame(window); fullFrame.pack()
    frame1 = Frame(fullFrame); frame1.pack()

    itemList=['상의','하의','모자','신발','가방']

    variable = StringVar(frame1)
    variable.set(itemList[0]) #initial value

    w=OptionMenu(frame1, variable, *itemList)
    w.pack(side=LEFT)
    btn1 = Button(frame1, text="검색", command=sear1);btn1.pack(side=RIGHT)


    ####### 검색 결과 화면 ######
    frame2 = Frame(fullFrame); frame2.pack(side=TOP, expand=1)
    idx=Label(frame2, text="번호");idx.pack(side=LEFT, padx=60)
    comm=Label(frame2, text="설명");comm.pack(side=LEFT, padx=40)
    rece=Label(frame2, text="최근 착용일");rece.pack(side=LEFT, padx=50)
    image=Label(frame2, text="이미지 보기");image.pack(side=LEFT, padx=40)

    frame3 = Frame(fullFrame); frame3.pack(side=BOTTOM, expand=1)
    listIDX=Listbox(frame3); listIDX.pack(side=LEFT)
    listCOMM=Listbox(frame3); listCOMM.pack(side=LEFT)
    listRECE = Listbox(frame3); listRECE.pack(side=LEFT)
    listImage= Listbox(frame3); listImage.pack(side=LEFT)

    return
def makeEmptyRGBList():

    global fullFrame, inW, inH

    R, G, B = [], [], []  # 초기화
    for _ in range(inH):
        tmp = []
        for _ in range(inW):
            tmp.append(0)
        R.append(tmp)
    for _ in range(inH):
        tmp = []
        for _ in range(inW):
            tmp.append(0)
        G.append(tmp)
    for _ in range(inH):
        tmp = []
        for _ in range(inW):
            tmp.append(0)
        B.append(tmp)
    return R,G,B
def loadImageColor(fname) :
    global window, canvas, paper, inW, inH, outW, outH, inImageR, inImageG, inImageB, outImageR, outImageG, outImageB, filename, photo


    # 파일 크기 계산
    photo = Image.open(fname)
    inW = photo.width;  inH = photo.height

    ### inImageR, G, B 초기화 to Numpy
    inImageR = np.zeros((inH, inW), dtype=np.uint8)
    inImageG = np.zeros((inH, inW), dtype=np.uint8)
    inImageB = np.zeros((inH, inW), dtype=np.uint8)


    # 파일 --> 메모리로 한개씩 옮기기
    photoRGB = photo.convert('RGB')
    for  i  in  range(inH) :
        for k in range(inW) :
            r, g, b = photoRGB.getpixel((k, i)) #
            inImageR[i][k] = r; inImageG[i][k] = g; inImageB[i][k] = b

    # print(inImageR[100][100],inImageG[100][100],inImageB[100][100])
def  openImage() :
    global window, canvas, paper, inW, inH, outW, outH, inImageR, inImageG, inImageB, outImageR, outImageG, outImageB, filename
    filename = askopenfilename(parent=window, filetypes=(("영상 파일", "*.gif;*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename == "" or filename == None :
        return
    # 파일 --> 메모리
    loadImageColor(filename)

    # Input --> outPut으로 동일하게 만들기.
    equalImageColor()
def displayImageColor() :
    global window, canvas, paper, inW, inH, outW, outH, inImageR, inImageG, inImageB, outImageR, outImageG, outImageB, filename
    if canvas != None :
        canvas.destroy()

    ### 고정된 화면을 준비 ###
    VIEW_X, VIEW_Y = 512,512
    if VIEW_X >= outW or VIEW_Y >= outH : # 원영상이 256이하면
        VIEW_X = outW;  VIEW_Y = outH
        step = 1
    else:
        if outW > outH:
            step = outW // VIEW_X
        else:
            step = outH // VIEW_Y

    window.geometry(str(int(VIEW_X*1.1)) + 'x' + str(int(VIEW_Y*1.1)))
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_X / 2, VIEW_Y / 2), image=paper, state='normal')

    rgbString = '' # 여기에 전체 픽셀 문자열을 저장할 계획
    for i in np.arange(0, outH, step) :
        tmpString = ''
        for k in np.arange(0, outW, step) :
            r, g, b = outImageR[i][k], outImageG[i][k], outImageB[i][k],
            tmpString += ' #%02x%02x%02x' % (r, g, b)
        rgbString += '{' + tmpString + '} '
    paper.put(rgbString)
    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))
def equalImageColor() :
    global window, canvas, paper, inW, inH, outW, outH, inImageR, inImageG, inImageB, outImageR, outImageG, outImageB, filename

    # outImage의 크기를 결정
    outH = inH;  outW = inW
    # 빈 메모리 확보 (2차원 리스트)
    outImageR, outImageG, outImageB = makeEmptyRGBList()

    #### 영상 처리 알고리즘을 구현 ####
    for i in range(inH) :
        for k in range(inW) :
            outImageR[i][k] = inImageR[i][k]
            outImageG[i][k] = inImageG[i][k]
            outImageB[i][k] = inImageB[i][k]
    ################################
    displayImageColor()
def addCloths():
    global variable,fullFrame,variable,ent1,ent2, w, inW, inH, outW, outH, inImageR, inImageG, inImageB, outImageR, outImageG, outImageB, filename,text
    itemList=['상의','하의','신발','가방'] #0,1,2,3,4

    con = pymssql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS, database=DB_NAME,
                          charset='utf8')
    cur = con.cursor()


    cnt=0
    for item in itemList:
        if item==variable.get():
            break
        cnt+=1


    categoryType=str(cnt+1)
    mC=str(ent1.get())
    comment=str(ent2.get())

    query="insert into Cloths(mainColor, categoryType, comment) values('"+mC+"', "+categoryType+", '"+comment+"')"

    cur.execute(query)
    print(query)

    query = "select max(idx) from Cloths"
    cur.execute(query)
    maxIdx=str(cur.fetchone()[0])

    query = "insert into Image(cloth_idx, width, height, imageInfo) values("+maxIdx+", "+str(inW)+", "+str(inH)+",'"+text+"')"

    cur.execute(query)


    cur.close()
    con.commit()
    con.close()
def menuAdd1():
    ######## MENU 2. 추가 ########

    global variable,fullFrame,variable,ent1,ent2,w

    if fullFrame != None:
        fullFrame.destroy()


    fullFrame=Frame(window); fullFrame.pack()


    frame1 = Frame(fullFrame); frame1.pack(side=TOP)

    itemList=['상의','하의','신발','가방']

    variable = StringVar(frame1)
    variable.set(itemList[0]) #initial value

    w=OptionMenu(frame1, variable, *itemList)
    w.pack(side=LEFT)

    ent1 = Entry(frame1); ent1.pack(side=LEFT, padx=10) #input Main color
    ent2 = Entry(frame1); ent2.pack(side=LEFT, padx=10) #input comment

    btn1 = Button(frame1, text="추가", command=addCloths);btn1.pack(side=LEFT, padx=10)


    frame2 = Frame(fullFrame); frame2.pack(side=BOTTOM)
    #label1 = Label(frame2); label1.pack()

    btn2 = Button(frame2, text="이미지 불러오기",command=openImage); btn2.pack(side=LEFT, padx=10)
    return
def sear2():
    global variable, fullFrame
    con = pymssql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS, database=DB_NAME,
                          charset='utf8')
    cur = con.cursor()

    itemList=['상의','하의','신발','가방'] #0,1,2,3,4

    itemIdx = 0
    for item in itemList:
        if item == variable.get():
            break
        itemIdx += 1
    itemIdx+=1

    query="select items, wearDate from wearing order by wearDate desc"
    cur.execute(query)
    rows=cur.fetchall()

    iList=[]
    dateList=[]
    for row in rows:
        iList.append(row[0]) ## 입은 옷 저장.
        dateList.append(row[1]) ## 입은 날짜 저장.

    for item in iList:
        print(item)

    cur.close()
    con.commit()
    con.close()
    return
def menuPrice():
    ######## MENU 3. 옷 정보 검색-가격 ########

    global variable, fullFrame

    if fullFrame != None:
        fullFrame.destroy()

    fullFrame = Frame(window);
    fullFrame.pack()
    frame1 = Frame(fullFrame);
    frame1.pack()

    itemList = ['상의','하의','신발','가방']

    variable = StringVar(frame1)
    variable.set(itemList[0])  # initial value

    w = OptionMenu(frame1, variable, *itemList)
    w.pack(side=LEFT)
    btn1 = Button(frame1, text="검색", command=sear2);
    btn1.pack(side=RIGHT)

    # print(variable.get())

    ####### 검색 결과 화면 ######
    frame2 = Frame(fullFrame);
    frame2.pack(side=TOP, expand=1)
    idx = Label(frame2, text="번호");idx.pack(side=LEFT, padx=60)
    comm = Label(frame2, text="설명");comm.pack(side=LEFT, padx=40)
    rece = Label(frame2, text="최근 착용일");rece.pack(side=LEFT, padx=50)
    image = Label(frame2, text="가격");image.pack(side=LEFT, padx=40)

    frame3 = Frame(fullFrame);
    frame3.pack(side=BOTTOM, expand=1)
    listIDX = Listbox(frame3);
    listIDX.pack(side=LEFT)
    listCOMM = Listbox(frame3);
    listCOMM.pack(side=LEFT)
    listRECE = Listbox(frame3);
    listRECE.pack(side=LEFT)
    listImage = Listbox(frame3);
    listImage.pack(side=LEFT)

    return
def menuRecent():
    ######## MENU 3. 옷 정보 검색 - 최근 착용일 ########
    global variable, fullFrame, sheet, rows, window2

    if fullFrame != None:
        fullFrame.destroy()

    fullFrame = Frame(window);
    fullFrame.pack()

    con = pymssql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS, database=DB_NAME,charset='utf8')
    cur = con.cursor()

    query="select items from Wearing order by wearDate Desc"
    cur.execute(query)

    rows=cur.fetchall()

    ## 새로운 윈도창 띄우기
    window2 = Toplevel(fullFrame)
    sheet = ttk.Treeview(window2, height=10);
    sheet.pack()
    descs = cur.description
    colNames = [d[0] for d in descs]
    sheet.column("#0", width=80);
    sheet.heading("#0", text=colNames[0])
    sheet["columns"] = colNames[1:]
    for colName in colNames[1:]:
        sheet.column(colName, width=80);
        sheet.heading(colName, text=colName)

    for row in rows:
        sheet.insert('', 'end', text=row[0], values=row[1:])
    sheet.bind('<Double-1>', sheetDblClick)


    return
def sheetDblClick(event):
    global variable, fullFrame, sheet, rows, window2, inW, inH,outW, outH,imageInfo,inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    item = sheet.identify('item', event.x, event.y)  # 'I001' ....
    entNum = int(item[1:]) - 1  ## 쿼리한 결과 리스트의 순번
    id = rows[entNum][0]  ## 선택한 id
    window2.destroy()
    # DB에서 이미지를 다운로드
    con = pymssql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS, database=DB_NAME,charset='utf8')
    cur = con.cursor()

    sql = "SELECT imageInfo, width, height from Image where cloth_idx=" + str(id)  # ID로 이미지 추출하기

    cur.execute(sql)
    row = cur.fetchone()
    cur.close()
    con.close()

    # 임시 폴더
    imageInfo=row[0]; inW=row[1]; inH=row[2]
    print(imageInfo)
    outImageR, outImageG, outImageB = makeEmptyRGBList()
    inImageR, inImageG, inImageB = makeEmptyRGBList()

    start,cnt=0,0
    for i in range(inH):
        for k in range(inW):
            newStr=""
            if imageInfo[start]=='(':
                start+=1
            while imageInfo[start] != ')':
                newStr=newStr+imageInfo[start]
                start+=1
            start+=2
            print(newStr)
            r=int(newStr.split(",")[0]); g = int(newStr.split(",")[1]); b=int(newStr.split(",")[2])
            inImageR[i][k]=r; inImageG[i][k]=g; inImageB[i][k]=b
            outImageR[i][k]=r; outImageG[i][k]=g; outImageB[i][k]=b
    outW=inW; outH=inH
    displayImageColor()
    return
def getImageFromDB():

    return
def menuAddStyleBook():
    ######## MENU 5. 스타일 북 ########
    global variable, fullFrame, sheet, rows, window2,inW, inH,imageInfo

    if fullFrame != None:
        fullFrame.destroy()

    fullFrame = Frame(window);fullFrame.pack(expand=1)
    frame1 = Frame(fullFrame);frame1.pack(expand=1)

    label1= Label(frame1, text="<< 필터 적용 후 스타일북에 저장하기>> "); label1.pack(side=TOP)



    btn1 = Button(frame1, text="이미지 불러오기", command=sear2);
    btn1.pack(side=RIGHT)

    con = pymssql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS, database=DB_NAME, charset='utf8')
    cur = con.cursor()


    query="select idx,mainColor, categoryType, comment from Cloths"
    cur.execute(query)
    rows=cur.fetchall()

    ## 새로운 윈도창 띄우기
    window2 = Toplevel(window); window2.geometry("600x600")
    sheet = ttk.Treeview(window2);sheet.pack(expand=1)
    descs = cur.description
    colNames = [d[0] for d in descs]
    sheet.column("#0", width=80);
    sheet.heading("#0", text=colNames[0])
    sheet["columns"] = colNames[1:]
    for colName in colNames[1:]:
        sheet.column(colName, width=200);
        sheet.heading(colName, text=colName)
    for row in rows:
        sheet.insert('', 'end', text=row[0], values=row[1:])
    sheet.bind('<Double-1>', sheetDblClick)

    cur.close()
    con.close()




    return
def menuRemoveBG():
    global filename, inH, inW
    openImage()
    # == Parameters =======================================================================
    BLUR = 21
    CANNY_THRESH_1 = 10
    CANNY_THRESH_2 = 200
    MASK_DILATE_ITER = 10
    MASK_ERODE_ITER = 10
    MASK_COLOR = (1.0, 1.0, 1.0)  # In BGR format

    # == Processing =======================================================================

    # -- Read image -----------------------------------------------------------------------
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # -- Edge detection -------------------------------------------------------------------
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)

    # -- Find contours in edges, sort by area ---------------------------------------------
    contour_info = []
    #_, contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # Previously, for a previous version of cv2, this line was:
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # Thanks to notes from commenters, I've updated the code but left this note
    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]

    # -- Create empty mask, draw filled polygon on it corresponding to largest contour ----
    # Mask is black, polygon is white
    mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255))

    # -- Smooth mask, then blur it --------------------------------------------------------
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([mask] * 3)  # Create 3-channel alpha mask

    # -- Blend masked img into MASK_COLOR background --------------------------------------
    mask_stack = mask_stack.astype('float32') / 255.0  # Use float matrices,
    img = img.astype('float32') / 255.0  # for easy blending

    masked = (mask_stack * img) + ((1 - mask_stack) * MASK_COLOR)  # Blend
    masked = (masked * 255).astype('uint8')  # Convert back to 8-bit

    # # split image into channels
    # c_red, c_green, c_blue = cv2.split(img)
    #
    # # merge with mask got on one of a previous steps
    # img_a = cv2.merge((c_red, c_green, c_blue, mask.astype('float32') / 255.0))
    #
    #
    #
    cv2.imshow('img',masked)  # Display
    # #cv2.imshow('img', img_a)
    #cv2.waitKey()

    cv2.imwrite('C:/Users/B-17/Desktop/DB project/afterImages/person-masked.jpg', masked)# Save
def menuPrint():
    ######## MENU 6. 프린트하기 ########

    global filename, inH, inW
    printM.printFile(filename) #현재 이미지를 출력한다.
def sheetDblClick2(event):
    global variable, fullFrame, sheet, rows, window2, inW, inH,outW, outH,imageInfo,inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    item = sheet.identify('item', event.x, event.y)  # 'I001' ....
    entNum = int(item[1:]) - 1  ## 쿼리한 결과 리스트의 순번
    id = rows[entNum][0]  ## 선택한 id
    window2.destroy()
    # DB에서 이미지를 다운로드
    con = pymssql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS, database=DB_NAME,charset='utf8')
    cur = con.cursor()

    sql= "select items from Wearing where idx="+str(id)
    print(sql)
    cur.execute(sql)
    row = cur.fetchone()
    cur.close()
    con.close()

    itemList=row[0].split(",")
    imgCnt=len(itemList)
    for item in itemList:
        pass


    # imageInfo=row[0]; inW=row[1]; inH=row[2]
    # print(imageInfo)
    # outImageR, outImageG, outImageB = makeEmptyRGBList()
    # inImageR, inImageG, inImageB = makeEmptyRGBList()
    #
    # start,cnt=0,0
    # for i in range(inH):
    #     for k in range(inW):
    #         newStr=""
    #         if imageInfo[start]=='(':
    #             start+=1
    #         while imageInfo[start] != ')':
    #             newStr=newStr+imageInfo[start]
    #             start+=1
    #         start+=2
    #         print(newStr)
    #         r=int(newStr.split(",")[0]); g = int(newStr.split(",")[1]); b=int(newStr.split(",")[2])
    #         inImageR[i][k]=r; inImageG[i][k]=g; inImageB[i][k]=b
    #         outImageR[i][k]=r; outImageG[i][k]=g; outImageB[i][k]=b
    # outW=inW; outH=inH
    # displayImageColor()
    return

def menuCallStyle():
    global variable, fullFrame, sheet, rows, window2

    if fullFrame != None:
        fullFrame.destroy()

    fullFrame = Frame(window);
    fullFrame.pack()

    con = pymssql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS, database=DB_NAME, charset='utf8')
    cur = con.cursor()

    query = "select idx, wearDate from Wearing order by wearDate Desc"
    cur.execute(query)

    rows = cur.fetchall()

    ## 새로운 윈도창 띄우기
    window2 = Toplevel(fullFrame)
    sheet = ttk.Treeview(window2, height=10);
    sheet.pack()
    descs = cur.description
    colNames = [d[0] for d in descs]
    sheet.column("#0", width=80);
    sheet.heading("#0", text=colNames[0])
    sheet["columns"] = colNames[1:]
    for colName in colNames[1:]:
        sheet.column(colName, width=80);
        sheet.heading(colName, text=colName)

    for row in rows:
        sheet.insert('', 'end', text=row[0], values=row[1:])
    sheet.bind('<Double-1>', sheetDblClick2)

    return


######## Main Menu   ########
mainMenu = Menu(window)
window.config(menu=mainMenu)

## Status Bar 추가
status = Label(window, text='이미지 정보:', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

######## MENU 1. 검색 ########
searchMenu = Menu(mainMenu)
mainMenu.add_cascade(label = "검색", menu=searchMenu)

searchMenu.add_cascade(label="옷장 검색", command=menuSearch1)

######## MENU 2. 추가 ########
addMenu = Menu(mainMenu)
mainMenu.add_cascade(label = "추가", menu=addMenu)

addMenu.add_cascade(label="옷 추가하기", command=menuAdd1)

######## MENU 3. 옷 정보 검색 ########
clothsMenu = Menu(mainMenu)
mainMenu.add_cascade(label = "옷 정보", menu=clothsMenu)

clothsMenu.add_cascade(label="가격 정보 검색", command=menuPrice)
clothsMenu.add_cascade(label="최근 착용일 검색", command=menuRecent)

######## MENU 4. 스타일링 ########
styleMenu = Menu(mainMenu)

sMenu=Menu(styleMenu)

mainMenu.add_cascade(label = "스타일링", menu=styleMenu)
styleMenu.add_cascade(label="action", menu=sMenu, command=None)
sMenu.add_cascade(label = "스타일링", command=None)
sMenu.add_cascade(label = "옷 색상 바꾸기", command=None)

######## MENU 5. 스타일 북 ########
styleBookMenu = Menu(mainMenu)

addStyleMenu=Menu(styleBookMenu)

mainMenu.add_cascade(label = "스타일 북", menu=styleBookMenu)
styleBookMenu.add_command(label="추가하기", command=menuAddStyleBook)
styleBookMenu.add_command(label="스타일 불러오기", command=menuCallStyle)

styleBookMenu.add_cascade(label="필터 적용하기", menu=addStyleMenu)
addStyleMenu.add_cascade(label ="필터1", command=menuAddStyleBook)
addStyleMenu.add_cascade(label ="필터2", command=None)

######## MENU 6. 프린트하기 ########
printMenu = Menu(mainMenu)

mainMenu.add_cascade(label="프린트하기", menu=printMenu)
printMenu.add_cascade(label="프린트하기", command=menuPrint) # filename 전달하기.


######## MENU 7. Image Processing ########
imageMenu = Menu(mainMenu)

mainMenu.add_cascade(label="이미지 프로세싱", menu=imageMenu)
imageMenu.add_cascade(label="배경제거", command=menuRemoveBG) # filename 전달하기.

window.mainloop()