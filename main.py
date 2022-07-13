import pyautogui
import PIL
from PIL import Image
screen = pyautogui.screenshot("screenshot.png")
# screen = Image.open("screenshot.png")
pix = screen.load()
begin_point_color = (255,0,0)
field_begin_point_color = (128,128,128)
cell_colors = [(192,192,192),(128,128,128),(255,255,255)]
color_pos = 0

def find_on_field(screen, pix, object,move_to=False, click=False,return_coords = False,find_last=False,beging_with=(0,0), find_only_in_row=False):
    cords=()
    begin_with_x = beging_with[0]
    for y in range(beging_with[1],screen.height):
        if find_only_in_row:
            if pix[begin_with_x, y] == object:
                if not find_last:
                    if move_to:
                        pyautogui.moveTo(begin_with_x, y)
                    if click:
                        pyautogui.click(begin_with_x, y)
                    if return_coords:
                        return (begin_with_x, y)
                    else:
                        return 0
                else:
                    cords = (begin_with_x, y)
        else:
            for x in range(begin_with_x,screen.width):
                if pix[x, y] == object:
                    if not find_last:
                        if move_to:
                            pyautogui.moveTo(x, y)
                        if click:
                            pyautogui.click(x, y)
                        if return_coords:
                            return (x,y)
                        else:
                            return 0
                    else:
                        cords=(x,y)
            begin_with_x = 0
    if find_last:
        if move_to:
            pyautogui.moveTo(cords)
        if click:
            pyautogui.click(cords)
        if return_coords:
            return cords
        else:
            return 0
    return "aboba"
# выделение нужного окна
find_on_field(screen, pix,(255,255,255),True,True)
# скрин в нужном окне
screen = pyautogui.screenshot("screenshot2.png")
# screen = Image.open("screenshot2.png")

pix = screen.load()

#нахождение отправной точки отсчета
cords = find_on_field(screen,pix, begin_point_color,False,False, True)
x_cord = cords[0]

y_cord = find_on_field(screen,pix, begin_point_color,True,True, True,True)[1]

#нахождение начальной точки поля с ячейками
field_beging_coords = find_on_field(screen,pix, field_begin_point_color,True,False,True,False,(x_cord,y_cord),True)
field_beging_coords = find_on_field(screen,pix, (255,255,255),True,False,True,False,(field_beging_coords[0],field_beging_coords[1]),True)
cell = []

# помечаем сколько пикселей занимает каждый цвет
new_x, new_y = field_beging_coords[0],field_beging_coords[1]

for i in range(0,len(cell_colors)):
    new_pos = find_on_field(screen, pix, cell_colors[i], False, False, True, False, (new_x, new_y),True)
    distance = new_pos[1] - new_y
    cell.append(distance)
    new_y = new_pos[1]


# считаем клетки по вертикали
field_width = 0
field_height = 0
flag = True
new_x, new_y = field_beging_coords[0],field_beging_coords[1]
print(cell)
while flag:
    for i in range(len(cell)):
        new_pos = find_on_field(screen, pix, cell_colors[i], True, False, True, False, (new_x, new_y), True)
        distance = new_pos[1] - new_y
        new_y = new_pos[1]
        print(new_x,new_y,new_pos,distance)
        if distance != cell[i%len(cell)]:
            flag= False
            break

    field_height+=1
print(field_height)
s = input()