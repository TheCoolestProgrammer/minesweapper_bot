import pyautogui
import PIL
from PIL import Image

screen = pyautogui.screenshot("screenshot.png")
# screen = Image.open("screenshot.png")
pix = screen.load()
begin_point_color = (255, 0, 0)
field_begin_point_color = (128, 128, 128)
cell_colors_y = [(192, 192, 192), (128, 128, 128), (255, 255, 255)]
cell_colors_x = [(192, 192, 192), (128, 128, 128), (255, 255, 255)]
color_pos = 0
zero_point = []

def find_on_field(screen, pix, object, move_to=False, click=False,
                  return_coords=False, find_last=False, beging_with=(0, 0), find_only_in_row=False, find_only_in_column=False):
    cords = ()
    begin_with_x = beging_with[0]
    if find_only_in_column:
        y = beging_with[1]
        for x in range(begin_with_x, screen.width):
            if pix[x, y] == object:
                if not find_last:
                    if move_to:
                        pyautogui.moveTo(x, y)
                    if click:
                        pyautogui.click(x, y)
                    if return_coords:
                        return (x, y)
                    else:
                        return 0
                else:
                    cords = (x, y)
    else:
        for y in range(beging_with[1], screen.height):
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
                for x in range(begin_with_x, screen.width):
                    if pix[x, y] == object:
                        if not find_last:
                            if move_to:
                                pyautogui.moveTo(x, y)
                            if click:
                                pyautogui.click(x, y)
                            if return_coords:
                                return (x, y)
                            else:
                                return 0
                        else:
                            cords = (x, y)
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
    return 0


# выделение нужного окна
find_on_field(screen, pix, (255, 255, 255), True, True)
# скрин в нужном окне
screen = pyautogui.screenshot("screenshot2.png")
# screen = Image.open("screenshot2.png")

pix = screen.load()

# нахождение отправной точки отсчета
cords = find_on_field(screen, pix, begin_point_color, False, False, True)
x_cord = cords[0]

y_cord = find_on_field(screen, pix, begin_point_color, True, True, True, True)[1]

# нахождение начальной точки поля с ячейками
field_beging_coords = find_on_field(screen, pix, field_begin_point_color, True, False, True, False, (x_cord, y_cord),
                                    True)
field_beging_coords = find_on_field(screen, pix, (255, 255, 255), True, False, True, False,
                                    (field_beging_coords[0], field_beging_coords[1]), True)
cell_y = []
cell_x = []
# помечаем сколько пикселей занимает каждый цвет по у координате
new_x, new_y = field_beging_coords[0], field_beging_coords[1]

for i in range(0, len(cell_colors_y)):
    new_pos = find_on_field(screen, pix, cell_colors_y[i], False, False, True, False, (new_x, new_y), True)
    distance = new_pos[1] - new_y
    cell_y.append(distance)
    new_y = new_pos[1]

# считаем клетки по вертикали
field_width = -1
field_height = -1
flag = True
new_x, new_y = field_beging_coords[0], field_beging_coords[1]
while flag:
    field_height += 1
    for i in range(len(cell_y)):
        new_pos = find_on_field(screen, pix, cell_colors_y[i], True, False, True, False, (new_x, new_y), True)
        distance = new_pos[1] - new_y
        new_y = new_pos[1]

        if distance != cell_y[i % len(cell_y)]:
            flag = False
            break




new_x, new_y = field_beging_coords[0], field_beging_coords[1]
new_y= new_y+ sum(cell_y)//2

new_pos = find_on_field(screen, pix, cell_colors_y[1], False, False, True, False, (0, new_y), False, True)
new_pos = find_on_field(screen, pix, cell_colors_y[2], False, False, True, False, (new_pos[0], new_y), False, True)
# #нашли начало отсчета кооординат по х
zero_point = (new_pos[0],field_beging_coords[1])
x_pos = new_pos[0]
new_x = new_pos[0]
for i in range(0, len(cell_colors_x)):
    new_pos = find_on_field(screen, pix, cell_colors_y[i], False, False, True, False, (new_x, new_y), False,True)
    distance = new_pos[0] - new_x
    cell_x.append(distance)
    new_x = new_pos[0]
#считаем клетки по горизонтали
new_x, new_y = field_beging_coords[0], field_beging_coords[1]
new_y= new_y+ sum(cell_y)//2
new_x = x_pos
flag = True
print("________________________________________________")
while flag:
    field_width += 1
    for i in range(len(cell_x)):
        new_pos = find_on_field(screen, pix, cell_colors_y[i], True, False, True, False, (new_x, new_y), False,True)
        distance = new_pos[0] - new_x
        new_x = new_pos[0]
        # print(new_x, new_y, new_pos, distance)
        if distance != cell_x[i % len(cell_x)]:
            flag = False
            break



field = [[0]*field_width for y in range(field_height)]
for i in field:
    print(i)
print("field size is",field_width,"X", field_height)
s = input()
