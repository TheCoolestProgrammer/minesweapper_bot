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
numbers_colors = {
    1:{(0,0,255),},
    2: {(0,128,0),},
    3: {(255,0,0),},
    4: {(0,0,128),},
    5: {(128,0,0),},
    6: {(0,128,128),},
    7: {(0,0,0),},
    # 8: {(128,128,128),},
    "flag":{(255,0,0),(0,0,0),}
}
allowed_colors= [(0,0,255), (0,128,0),(255,0,0),(0,0,128),(128,0,0),(0,128,128),(0,0,0),(128,128,128),]

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
field_height = 0
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


field = [[None]*field_width for y in range(field_height)]
for i in field:
    print(i)
print("field size is",field_width,"X", field_height)




def coordinates_changer(coords):
    # new_x = (coords[0]-zero_point[0])//sum(cell_x)
    new_x = zero_point[0] + sum(cell_x)*coords[0]
    # new_y = (coords[1]-zero_point[1])//sum(cell_y)
    new_y = zero_point[1] + sum(cell_y)*coords[1]
    return (new_x,new_y)

def find_number_in_cell(x,y):
    colors = set()
    other_colors = set()
    coords_begin = coordinates_changer((x,y))

    for y in range(coords_begin[1],coords_begin[1]+sum(cell_y)):
        for x in range(coords_begin[0],coords_begin[0]+sum(cell_x)):

            color = pix[x,y]
            if color in allowed_colors:
                colors.add(color)
            else:
                other_colors.add(color)
    if (255,255,255) in other_colors:
        return None
    for i in numbers_colors.keys():
        if colors == numbers_colors[i]:
            return i
    return 0
def fields_arround(cords):
    results={
        None:[],
        "flag":[]
    }
    for y in range(cords[1]-1,cords[1]+2):
        for x in range(cords[0]-1,cords[0]+2):
            if 0<=x<len(field[0]) and 0<=y<len(field):
                if field[y][x] == None or field[y][x] == "flag":
                    results[field[y][x]].append((x,y))
    return results
def algorhytm1():
    numbers=dict()
    for y in range(field_height):
        for x in range(field_width):
            res = find_number_in_cell(x,y)
            field[y][x] = res
            if res:
                if 1<= res <=8 or res == "flag":
                    if res not in numbers.keys():
                        numbers[res] = [(x,y)]
                    else:
                        numbers[res].append((x,y))
    print("тут все заебись")
    for i in field:
        print(i)
    print(numbers)
    #TODO: отсортировать словарь
    for i in numbers.keys():
        for j in numbers[i]:
            res = fields_arround(j)
            if len(res[None])- len(res["flag"]) == i:
                for k in res[None]:
                    if k not in res["flag"]:
                        pyautogui.rightClick(coordinates_changer((k[0],k[1])))
                        res["flag"].append(k)
                        field[k[1]][k[0]] = "flag"
    print("и тут")
pyautogui.click(zero_point[0]+2,zero_point[1]+2)
screen = pyautogui.screenshot("screenshot3.png")
# screen = Image.open("screenshot3.png")
pix = screen.load()
try:
    algorhytm1()
except Exception as e:
    print(e)
    s = input()
print("заебумба ^_^")
s = input()
