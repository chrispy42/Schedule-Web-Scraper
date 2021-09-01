import pygame
import json
import time

pygame.font.init()

WIN_WIDTH = 800
WIN_HEIGHT = 450
GEN = 0
mousedown = False

#get info from json files
with open('StudentSchedules.json') as f:
    student_info = json.load(f)
with open('TeacherSchedules.json') as f:
    teacher_info = json.load(f)

#declare variables

student_names = student_info['jsonids']
teacher_names = teacher_info['jsonids']
fullclasslist = []

for person in student_names:
    for i in range(6):
        add = True
        for l in range(len(fullclasslist)):
            if student_info[person][i] + ' ' + str(i + 1) == fullclasslist[l]:
                add = False
        if add:
            fullclasslist.append(student_info[person][i] + ' ' + str(i + 1))
#frontend

class Button:
    def __init__(self, text, x, y, width, height, size=40):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.clickwait = 30
        self.startcountdown = False
        self.size = size


    def drawbutton(self, win):
        BOXCOLOR = (255, 255, 255)
        BOXWIDTH = 3
        STAT_FONT = pygame.font.SysFont('comicsans', self.size)
        text = STAT_FONT.render(self.text, 1, (255, 255, 255))
        win.blit(text, ((self.x + self.width // 2) - (text.get_width() // 2), (self.y + self.height // 2) - (text.get_height() // 2)))
        pygame.draw.line(win, BOXCOLOR, (self.x, self.y), ((self.x + self.width), self.y), BOXWIDTH)
        pygame.draw.line(win, BOXCOLOR, (self.x, self.y), (self.x, (self.y + self.height)), BOXWIDTH)
        pygame.draw.line(win, BOXCOLOR, ((self.x + self.width), self.y), ((self.x + self.width), (self.y + self.height)), BOXWIDTH)
        pygame.draw.line(win, BOXCOLOR, (self.x, (self.y + self.height)), (((self.x + self.width), (self.y + self.height))), BOXWIDTH)

    def clicked(self):
        if self.startcountdown:
            if self.clickwait == 15:
                self.startcountdown = False
            self.clickwait += 1
        if mousedown and not self.startcountdown:
            if pygame.mouse.get_pos()[0] > self.x and pygame.mouse.get_pos()[0] < self.x + self.width:
                if pygame.mouse.get_pos()[1] > self.y and pygame.mouse.get_pos()[1] < self.y + self.height:
                    self.startcountdown = True
                    self.clickwait = 0
                    return True
        return False


def getName(string):
    return(string.split('.')[0])


def getclasslist(name, dot):
    global student_info
    global teacher_info
    student_names = student_info['jsonids']
    teacher_names = teacher_info['jsonids']

    class_names = []


    for person in student_names:
        if student_info[person][int(dot)-1] == name:
            class_names.append(getName(person))
    return class_names


def getpersonlist(name):
    pass


def textbasedquestions():
    global student_info
    global teacher_info
    global fullclasslist
    student_names = student_info['jsonids']
    teacher_names = teacher_info['jsonids']

    class_names = []
    # figure out what to look for
    a = 'c'
    if a == 'c':
        b = input('what dot?')
        print('here are all the dot ' + b + ' classes')
        dotclasses = []
        for i in range(len(fullclasslist)):
            if int(fullclasslist[i][-1]) == int(b):
                dotclasses.append(fullclasslist[i])

        print(dotclasses)

        a = input('what class?')
        for person in student_names:
            if student_info[person][int(b) - 1] == a:
                class_names.append(getName(person))
        print(class_names)


def main(win):
    global mousedown
    scene = 0
    screeninfo = []
    dotnum = -1
    dotclasses = []
    classbuttons = []
    CLASSNAMESIZE = 20

    clock = pygame.time.Clock()
    run = True
    while run:
        win.fill((0, 0, 0))
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousedown = True
            else:
                mousedown = False
        if scene == 0:
            for button in dotButtons:
                button.drawbutton(win)
            for i in range(len(dotButtons)):
                if dotButtons[i].clicked() == True:
                    dotnum = i + 1
                    scene = 1
            if dotnum != -1:
                for i in range(len(fullclasslist)):
                    if int(fullclasslist[i][-1]) == int(dotnum):
                        dotclasses.append(fullclasslist[i])
                for i in range(len(dotclasses)):
                    if i % 2 == 0:
                        Button(dotclasses[i], 25, 15*i+20, 350, 20, CLASSNAMESIZE )
                        classbuttons.append(Button(dotclasses[i], 25, 15*i+20, 350, 20, CLASSNAMESIZE ))
                    elif i % 2 == 1:
                        Button(dotclasses[i], 400, 15*(i-1)+20, 350, 20, CLASSNAMESIZE )
                        classbuttons.append(Button(dotclasses[i], 400, 15 * (i-1) + 20, 350, 20, CLASSNAMESIZE))
                mousedown = False

        if scene == 1:
            studentbuttons = []
            for button in classbuttons:
                button.drawbutton(win)
            for i in range(len(classbuttons)):
                if classbuttons[i].clicked() == True:
                    scene = 2
                    currentclassname = classbuttons[i].text
                    studentsshow = getclasslist(currentclassname[:-2], dotnum)
                    for i in range(len(studentsshow)):
                        if i % 2 == 0:
                            Button(studentsshow[i], 25, 15 * i + 20, 350, 20, CLASSNAMESIZE)
                            studentbuttons.append(Button(studentsshow[i], 25, 15 * i + 20, 350, 20, CLASSNAMESIZE))
                        elif i % 2 == 1:
                            Button(studentsshow[i], 400, 15 * (i - 1) + 20, 350, 20, CLASSNAMESIZE)
                            studentbuttons.append(Button(studentsshow[i], 400, 15 * (i - 1) + 20, 350, 20, CLASSNAMESIZE))



        if scene == 2:
            for button in studentbuttons:
                button.drawbutton(win)
        pygame.display.update()


win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('course finder')
dotButtons = [Button('DOT 1', 50, 100, 200, 100), Button('DOT 2', 300, 100, 200, 100), Button('DOT 3', 550, 100, 200, 100), Button('DOT 4', 50, 300, 200, 100), Button('DOT 5', 300, 300, 200, 100), Button('DOT 6', 550, 300, 200, 100)]

main(win)


