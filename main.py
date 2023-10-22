from pygame import *
from random import randint, choice
font.init()
mixer.init()

cellprop = 45

global FlagsLeft
FlagsLeft = 0
global BombsLeft
BombsLeft = 0

window_height = int(cellprop*20)
window_width = int(cellprop*18)
window = display.set_mode((window_width,window_height))
display.set_caption("Sapper")


class Cell:
    def __init__(self,cellX,cellY):
        self.opened = False
        self.marked = False
        self.bomb = False
        self.color = (0,240,0)
        self.colorClone = self.color
        self.w = cellprop
        self.h = cellprop
        self.square = Surface((self.w,self.h))
        self.barrier = False
        self.rect = self.square.get_rect()
        self.number = -1
        self.rect.x = cellX
        self.rect.y = cellY
        self.flagImg = transform.scale(image.load("kill_flag.png"),(26*cellprop//35,26*cellprop//35))

        
    def colorDefention(self):
        color1 = (0,200,0)
        if Cells_list[len(Cells_list)-2].color == self.color:
            self.color = color1
        
        if self.rect.x == 0:
            self.color = Cells_list[len(Cells_list)-2].color

        self.colorClone = self.color

    def drawCell(self):                         #drawCell
        self.barrierDraw()
        self.square.fill(self.color)
        window.blit(self.square,(self.rect.x,self.rect.y))

        try:
            if self.opened:
                window.blit(self.BombRender(),(self.rect.x*1.02,self.rect.y+cellprop/7*0.5))
        except:
            pass
        
        if self.marked:
            window.blit(self.flagImg,(self.rect.x,self.rect.y+cellprop/7))
       
    def ButtonCollide(self,x,y,ev):
        if ev.type == MOUSEBUTTONDOWN:
            if ev.button == 1:
                if self.rect.collidepoint(x,y):
                    self.open()
            
            if ev.button == 3:
                if self.rect.collidepoint(x,y):
                    self.changeMark()
    
    def barrierDraw(self):
        if self.barrier:
            self.color = (45,45,45)
            self.bomb = False
            self.marked = False
            self.opened = False
    
    def open(self):                         #open
        if not self.barrier and not self.opened and not self.marked:
            self.opened = True
            cellOpen.play()

            if not self.bomb:
                self.bombDetection()
                
                for cell in self.cellsAroundList:
                    cell.bombDetection()
                    
                if self.color == (0,240,0):
                    self.color = (240,170,30)
                else:
                    self.color = (220,150,0)

    def changeMark(self):
        global FlagsLeft
        global BombsLeft
        if not self.barrier and not self.opened and not self.marked and FlagsLeft>0:
            self.marked = True
            putFlag.play()
            FlagsLeft -= 1
            if self.bomb:
                BombsLeft -= 1

        elif self.marked:
            self.marked = False
            FlagCut.play()
            FlagsLeft += 1
            if self.bomb:
                BombsLeft += 1
            
    def bombDetection(self):
        if not self.barrier:
            self.cellsAroundGet()

            self.bombsAmtAround = 0
            for cell in self.cellsAroundList:
                if cell.bomb:
                    self.bombsAmtAround += 1
        
    def BombRender(self):
        colour = {1:(0, 85, 255),2:(0,255,0),3:(255,50,0),4:(50,0,255),
        5:(170, 60, 15),6:(0,255,255),7:(0,0,0),8:(255,255,255)}

        mfont = font.Font(None,int(cellprop*1.5))
        try:
            return mfont.render(str(self.bombsAmtAround),True,colour[self.bombsAmtAround])
        except:
            pass
    
    def cellsAroundGet(self):
        index = self.number

        leftCellcheck = Cells_list[index-1]
        rightCellcheck = Cells_list[index+1]

        leftUpCellcheck = Cells_list[index-CellInLine-1]
        midUpCellcheck = Cells_list[index-CellInLine]
        rightUpCellcheck = Cells_list[index-CellInLine+1]
        
        leftDownCellcheck = Cells_list[index+CellInLine-1]
        midDownCellcheck = Cells_list[index+CellInLine]
        rightDownCellcheck = Cells_list[index+CellInLine+1]

        self.cellsAroundList = (leftCellcheck,rightCellcheck,leftUpCellcheck,
            midUpCellcheck,rightUpCellcheck,leftDownCellcheck,midDownCellcheck,rightDownCellcheck)
    

class Button:
    def __init__(self,x,y):
        self.w = cellprop*5.5
        self.h = cellprop*2
        self.clrR = 100
        self.clrG = 175
        self.clrB = 255
        self.color = (self.clrR,self.clrG,self.clrB)
        self.area = Surface((self.w,self.h))
        self.area.fill(self.color)
        self.rect = self.area.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.haveText = False
        self.area.set_alpha(160)
        self.fontsize = self.h
        self.activated = False

    def proportionsSet(self,w,h,fontsize):
        self.fontsize = fontsize
        self.w = w
        self.h = h
        self.area = Surface((self.w,self.h))
        self.rect = self.area.get_rect()
        self.rect.x = self.x - self.w / cellprop*1.5
        self.rect.y = self.y - self.h / cellprop

        self.area.fill(self.color)

    def addText(self,text,x,y,clr):
        tfont = font.Font(None,int(self.fontsize))
        self.textForRender = text
        self.text = tfont.render(str(text),True,(clr))
        self.textpropx = x
        self.textpropy = y
        self.haveText = True
    
    def update(self):
        if self.activated:
            self.area.fill((255,140,140))
        else:
            self.area.fill((self.color))
        window.blit(self.area,(self.rect.x,self.rect.y))
        if self.haveText:
            window.blit(self.text,(self.textpropx,self.textpropy))
    
    def changeColor(self,r,g,b):
        self.color = (r,g,b)
        self.area.fill(self.color)
    

    def collider(self,x,y):
        if self.rect.collidepoint(x,y):
            self.activated = True
            for but in complexityButtons:
                if but != self:
                    but.activated = False
            return True


Cells_list = list()

cell = Cell(0,0)
Cells_list.append(cell)

#кнопки
#рестарта и выходы
restartButton = Button(cellprop*6.25,cellprop*9.5)
restartButton.addText("Restart",cellprop*6.5,cellprop*9.8,(255,255,255))

ExitButton = Button(cellprop*6.75,cellprop*16)
ExitButton.addText("Exit",cellprop*7.5,cellprop*16,(255,255,255))
ExitButton.proportionsSet(cellprop*5,cellprop*1.5,cellprop)
ExitButton.changeColor(200,50,50)

#кнопки установления сложности
BombsAmtSetX = cellprop*1.2

xlowbombs = Button(BombsAmtSetX,cellprop*2.2)
xmidbombs = Button(BombsAmtSetX,cellprop*3.3)
xnicebombs = Button(BombsAmtSetX,cellprop*4.4)
xmuchbombs = Button(BombsAmtSetX,cellprop*5.5)

xnicebombs.activated = True
complexityButtons = [xlowbombs,xmidbombs,xnicebombs,xmuchbombs]

complexityNumber = 40
for button in complexityButtons:
    button.proportionsSet(cellprop,cellprop,cellprop)
    button.addText(complexityNumber,button.rect.x*1.1,button.rect.top+cellprop*0.15,(255,255,255))
    complexityNumber += 15

maxBombsAmount = int(xnicebombs.textForRender)

#некоторые важные элементы и функции
firstClickTxtArea = Surface((cellprop*5.5,cellprop))
firstClickTxtArea.fill((50,50,255))
firstClickTxtArea.set_alpha(130)
FirstCkiclCluetxt = font.Font(None,cellprop).render("Click to any cell",True,(255,255,255))

xCord = cellprop*6.25
yArea = cellprop*3.5
yTxt = cellprop*3.7

def firsClickClueBlit(area=firstClickTxtArea,txt=FirstCkiclCluetxt,xProp=xCord,yAreaProp=yArea,yTxtProp=yTxt):
    window.blit(area,(xProp,yAreaProp))
    window.blit(txt,(xProp,yTxtProp))

LoadingMssgArea = Surface((cellprop*8,cellprop*2))
LoadingMssgArea.fill((35,35,35))
LoadingMssgArea.set_alpha(200)
LoadingTxt = font.Font(None,int(cellprop*2.5)).render("Loading...",True,(255,255,255))

xLAreaCord = cellprop*5
xLtxtCord = cellprop*5
yLAreaCord = cellprop*5
yLtxtCord = cellprop*5.2

def LoadingMssgBlit(area=LoadingMssgArea,text=LoadingTxt,xPropArea=xLAreaCord,xPropTxt=xLtxtCord,yAreaProp=yLAreaCord,yTxtProp=yLtxtCord):
    window.blit(area,(xPropArea,yAreaProp))
    window.blit(text,(xPropTxt,yTxtProp))


#создание клеток
amountOfCells = window_height*window_width // cellprop**2
for i in range(amountOfCells-1):
    currentX = Cells_list[len(Cells_list)-1].rect.x+cellprop
    currentY = Cells_list[len(Cells_list)-1].rect.y

    if Cells_list[len(Cells_list)-1].rect.x >= window_width-cellprop:
        currentY = Cells_list[len(Cells_list)-1].rect.y+cellprop
        currentX = 0
        
    cell = Cell(currentX, currentY)
    Cells_list.append(cell)
    cell.colorDefention()

for c in Cells_list:
    c.number = Cells_list.index(c)

CellInLine = 18
#постановка барьеров
for i in range(CellInLine):
    Cells_list[342+i].barrier = True

for cell in Cells_list:
    if cell.number in range(0,36):
        cell.barrier = True
    
    if cell.number%CellInLine == 0:
        cell.barrier = True
        Cells_list[cell.number-1].barrier = True

#стартовый клик: определяет количество нулевых 
#  клеток вокруг первой вскрытой и заполняет поле бомбами
def firstClickBombsDefection():
    FirsclickBool = True
    global running
    global maxBombsAmount
    clicked = False
    for ev in events:
        if ev.type == QUIT:
            running = False
        if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
            x,y = ev.pos
            for but in complexityButtons:
                if but.collider(x,y):
                    maxBombsAmount = int(but.textForRender)
                    clicked = True

            if not clicked:
                for cell in Cells_list:
                    collideBool = cell.ButtonCollide(x,y,ev)
                    cellBarrier = cell.barrier
                    
                    zeroCellAround = randint(3,8)
                    if cell.opened:
                        cell.cellsAroundGet()
                        cellsArnd = cell.cellsAroundList
            try:
                i = 0
                for i in range(zeroCellAround*2):
                    choice(cellsArnd).open()

                for cell in Cells_list:
                    if cell.opened:
                        cell.cellsAroundGet()
                        cellsArnd += cell.cellsAroundList
                
                cellsInt = zeroCellAround*5

                for i in range(cellsInt):
                    choice(cellsArnd).open()
                        
                FirsclickBool = False
            except:
                pass

    return FirsclickBool


#win/loose actions
def loose():
    for cell in Cells_list:
        cell.open()

        if cell.bomb:
            window.blit(
                transform.scale(image.load('bombImg.png'),(cellprop,cellprop)),(cell.rect.x,cell.rect.y)
            )

def win():
    window.blit(
        font.Font(None,cellprop*4).render('Победа!',True,(0,55,255)),(cellprop*3.3,cellprop*6)
    )

#interface
LmbClue = transform.scale(image.load('LMB.png'),(int(cellprop/1.5),int(cellprop*1)))
RmbClue = transform.scale(image.load('RMB.png'),(int(cellprop/1.5),int(cellprop)))
showelClue = transform.scale(image.load('showel.png'),(int(cellprop),int(cellprop)))
flagClue = transform.scale(image.load('kill_flag.png'),(int(cellprop),int(cellprop)))
BombImage = transform.scale(image.load('bombImg.png'),(cellprop,cellprop))

lbmX = cellprop*2
lbmY = cellprop*0.5
rmbX = cellprop*6
rmbY = lbmY

showelCl_x = cellprop*0.7
showelCl_y = lbmY
flagCl_x = cellprop*4.8
flagCl_y = lbmY

amtCl_x = cellprop*9
amtCl_y = lbmY

flag2Clx = amtCl_x*1.15
flag2Cly = amtCl_y

fontProp = cellprop*1.5

#sounds
cellOpen = mixer.Sound("shovelSound.ogg")
exploison = mixer.Sound("explosion.ogg")
putFlag = mixer.Sound("flagstand.ogg")
FlagCut = mixer.Sound("flagcut.ogg")

cellOpen.set_volume(0.2)
exploison.set_volume(0.2)
putFlag.set_volume(0.2)
FlagCut.set_volume(0.2)

#переменные для цикла
winned = False
loosed = False
global running
running = True
game = False
frames = 60
fps = time.Clock()
firstClick = True
needDefBombs = True

#цикл
while running:
    events = event.get()
    for cell in Cells_list:
        cell.drawCell()
        if cell.opened and cell.bomb and not needDefBombs and not loosed:
            exploison.play()
            game = False
            loosed = True
        if BombsLeft == 0 and not firstClick and not needDefBombs:
            game = False
            winned = True

    #interface
    window.blit(LmbClue,(lbmX,lbmY))
    window.blit(showelClue,(showelCl_x,showelCl_y))

    window.blit(RmbClue,(rmbX,rmbY))
    window.blit(flagClue,(flagCl_x,flagCl_y))

    window.blit(
        font.Font(None,int(fontProp)).render(str(FlagsLeft),True,(255,255,255)),(amtCl_x,amtCl_y)
        )
    window.blit(flagClue,(flag2Clx,flag2Cly))

    #firsclick
    if needDefBombs:
            if firstClick:
                for but in complexityButtons:
                    but.update()
                    window.blit(BombImage,(but.rect.x+cellprop,but.rect.y))
                    

                firsClickClueBlit()
                firstClick = firstClickBombsDefection()
                
            if not firstClick and needDefBombs:
                LoadingMssgBlit()

                cell = choice(Cells_list)
                if not cell.bomb and not cell.barrier and not cell.opened and FlagsLeft != maxBombsAmount:
                    cell.bomb = True
                    FlagsLeft += 1
                
                elif FlagsLeft == maxBombsAmount:
                    needDefBombs = False
                    BombsLeft = FlagsLeft
                    for cell in Cells_list:
                        if not cell.barrier:
                            cell.bombDetection()
                    game = True
    #main game
    if game:
        for ev in events:   
            if ev.type == QUIT:
                running = False
                
            if ev.type == MOUSEBUTTONDOWN and not firstClick:
                x,y = ev.pos
                for cell in Cells_list:
                    cell.ButtonCollide(x,y,ev)
                    
    if loosed:
        loose()
    elif winned:
        win()
    
    if loosed or winned:
        restartButton.update()
        ExitButton.update()

        #restart game
        for ev in events:
            if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
                x,y = ev.pos
                if ExitButton.collider(x,y):
                    running = False
                elif restartButton.collider(x,y):
                    FlagsLeft = 0
                    BombsLeft = 0
                    winned = False
                    loosed = False
                    firstClick = True
                    needDefBombs = True
                    for cell in Cells_list:
                        cell.bomb = False
                        cell.opened = False
                        cell.marked = False
                        cell.color = cell.colorClone

                    for button in complexityButtons:
                        if int(button.textForRender) == maxBombsAmount:
                            button.activated = True        
    fps.tick(frames)
    display.update()