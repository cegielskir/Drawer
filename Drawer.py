import json
import sys
import pygame


my_colors = []
fg_color = (0, 0, 0)
screen_height = 1


def str2rgb(s):
    rgba = s.split(",")
    if len(rgba) not in (3, 4):
        return 0, 0, 0
    return tuple(map(int, rgba))


def hex2rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def all2rgb(color):
    if color[0] == '#':
        return hex2rgb(color)
    elif color[0] == '(':
        return str2rgb(color[1:-1])
    else:
        return all2rgb(my_colors[color])


def handle_color(figure):
    if "color" in figure:
        return all2rgb(figure["color"])
    elif "fg_color" in figure:
        return all2rgb(figure["fg_color"])
    else:
        return fg_color


def hand_y(cord):
    return screen_height - cord - 1


def hand_points(points):
    final_list = []
    for two_points in points:
        x = two_points[0]
        y = hand_y(two_points[1])
        final_list.append(tuple((x,y)))
    return final_list


def draw_point(figure, screen):
    pygame.draw.rect(screen, handle_color(figure), (figure["x"] - 1, hand_y(figure["y"]), 1, 1), 0)


def draw_circle(figure, screen):
    pygame.draw.circle(screen, handle_color(figure), (figure["x"], hand_y(figure["y"])), figure["radius"], 0)


def draw_polygon(figure, screen):
    pygame.draw.polygon(screen, handle_color(figure), hand_points(figure["points"]), 0)


def draw_rectangle(figure, screen):
    pygame.draw.rect(screen, handle_color(figure),
                     (figure["x"],
                      hand_y(figure["y"]) - figure["height"],
                      figure["width"],
                      figure["height"]), 0)


def draw_square(figure, screen):
    pygame.draw.rect(screen, handle_color(figure),
                     (figure["x"],
                      hand_y(figure["y"]) - figure["size"],
                      figure["size"],
                      figure["size"]), 0)


def draw_figure(figure, screen):
    if figure["type"] == "point":
        draw_point(figure, screen)
    elif figure["type"] == "circle":
        draw_circle(figure, screen)
    elif figure["type"] == "polygon":
        draw_polygon(figure, screen)
    elif figure["type"] == "rectangle":
        draw_rectangle(figure, screen)
    elif figure["type"] == "square":
        draw_square(figure, screen)



def display(file_path):
    global my_colors, fg_color, screen_height
    pygame.init()
    json_data = open(file_path).read()
    data = json.loads(json_data)
    my_colors = data["Palette"]
    screen = pygame.display.set_mode((data["Screen"]["width"], data["Screen"]["height"]))
    screen_height = data["Screen"]["height"]
    screen.fill(all2rgb(data["Screen"]["bg_color"]))
    fg_color = handle_color(data["Screen"])
    running = True
    for figure in data["Figures"]:
        draw_figure(figure, screen)
    pygame.display.update()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    return screen


def main(argv):
    try:
        screen = display(argv[0])
        if len(argv) == 3:
            if argv[1] == '-o' or argv[1] == "--output":
                pygame.image.save(screen, argv[2] + ".PNG")
    except IOError as err:
        print("ERROR, opening file failed: " + str(err))
    except KeyError as err:
        print("ERROR: Wrong data in json file")
    except ValueError as err:
        print("Wrong HEX color value")
    except TypeError as err:
        print("Wrong RGB color value")


if __name__ == "__main__":
    main(sys.argv[1:])
