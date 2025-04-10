import pygame
import sys
import math
import random

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Cheat Menu Simulador")

# Colores
WHITE = (255, 255, 255)
DARK_BG = (18, 18, 18)
RED = (230, 50, 50)
DARK_RED = (180, 30, 30)
GRAY = (60, 60, 60)
LIGHT_GRAY = (130, 130, 130)
MULTICOLOR = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]

font = pygame.font.SysFont("Arial", 18)
small_font = pygame.font.SysFont("Arial", 14)

current_tab = "Aimbot"

options = {
    "Aimbot": {
        "Aimbot": False,
        "Circle FOV": False,
        "Filled FOV": False,
        "Square FOV": False,
        "Multicolor FOV": False,
        "Aimbot FOV": 300,
        "Player Render": 500,
        "Smoothness": 1.0,
        "Aimbot Bone": "Head",
        "Aim Key": "Right Mouse",
        "FOV Color": RED
    },
    "ESP": {
        "Ammo ESP": False,
        "Reload Check": False,
        "Box": False,
        "Filled Boxes": False,
        "Skeleton": False,
        "Distance": False,
        "Snaplines": False,
        "Middle Snaplines": False
    },
    "Exploits": {
        "Crosshair": False,
        "Nazi Crosshair": False,
        "Safe Mode": False,
        "Spinbot": False,
        "Rapid Fire": False
    }
}

aimbot_bones = ["Head", "Chest", "Pelvis"]
aim_keys = ["Right Mouse", "Left Mouse", "Q", "E"]
bone_index = 0
key_index = 0
color_index = 0


def draw_checkbox(x, y, label, checked):
    box = pygame.Rect(x, y, 20, 20)
    pygame.draw.rect(screen, LIGHT_GRAY if checked else GRAY, box, border_radius=4)
    if checked:
        pygame.draw.rect(screen, RED, box.inflate(-6, -6), border_radius=3)
    text = font.render(label, True, WHITE)
    screen.blit(text, (x + 30, y + 2))
    return box

def draw_slider(x, y, label, value, min_val, max_val):
    pygame.draw.rect(screen, GRAY, (x, y + 20, 200, 6), border_radius=3)
    knob_x = x + int(((value - min_val) / (max_val - min_val)) * 200)
    pygame.draw.circle(screen, RED, (knob_x, y + 23), 8)
    label_text = font.render(f"{label}: {round(value, 2)}", True, WHITE)
    screen.blit(label_text, (x, y))
    return pygame.Rect(knob_x - 8, y + 15, 16, 16)

def draw_dropdown(x, y, label, current):
    pygame.draw.rect(screen, GRAY, (x, y + 20, 200, 30), border_radius=4)
    text = font.render(current, True, WHITE)
    screen.blit(text, (x + 10, y + 25))
    screen.blit(font.render(label, True, WHITE), (x, y))
    return pygame.Rect(x, y + 20, 200, 30)

def draw_tab_buttons():
    buttons = {}
    tabs = ["Aimbot", "ESP", "Exploits"]
    for i, tab in enumerate(tabs):
        btn = pygame.Rect(50 + i * 120, 20, 100, 35)
        color = DARK_RED if current_tab == tab else GRAY
        pygame.draw.rect(screen, color, btn, border_radius=6)
        text = font.render(tab, True, WHITE)
        screen.blit(text, (btn.x + 20, btn.y + 8))
        buttons[tab] = btn
    return buttons

def get_multicolor_color(frame):
    i = frame // 10 % len(MULTICOLOR)
    return MULTICOLOR[i]

clock = pygame.time.Clock()
dragging_slider = None
frame_count = 0

while True:
    screen.fill(DARK_BG)
    mx, my = pygame.mouse.get_pos()
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
            if current_tab == "Aimbot":
                if aimbot_fov_knob.collidepoint(mx, my):
                    dragging_slider = "Aimbot FOV"
                elif player_render_knob.collidepoint(mx, my):
                    dragging_slider = "Player Render"
                elif smoothness_knob.collidepoint(mx, my):
                    dragging_slider = "Smoothness"
                elif bone_dropdown.collidepoint(mx, my):
                    bone_index = (bone_index + 1) % len(aimbot_bones)
                    options["Aimbot"]["Aimbot Bone"] = aimbot_bones[bone_index]
                elif aimkey_dropdown.collidepoint(mx, my):
                    key_index = (key_index + 1) % len(aim_keys)
                    options["Aimbot"]["Aim Key"] = aim_keys[key_index]
        if event.type == pygame.MOUSEBUTTONUP:
            dragging_slider = None
        if event.type == pygame.MOUSEMOTION and dragging_slider:
            rel_x = max(0, min(mx - 400, 200))
            percent = rel_x / 200
            if dragging_slider == "Aimbot FOV":
                options["Aimbot"]["Aimbot FOV"] = int(100 + percent * 500)
            elif dragging_slider == "Player Render":
                options["Aimbot"]["Player Render"] = int(100 + percent * 900)
            elif dragging_slider == "Smoothness":
                options["Aimbot"]["Smoothness"] = round(0.1 + percent * 4.9, 2)

    tab_buttons = draw_tab_buttons()
    if click:
        for tab, rect in tab_buttons.items():
            if rect.collidepoint(mx, my):
                current_tab = tab

    y = 80
    boxes = {}
    if current_tab == "Aimbot":
        screen.blit(font.render("AIMBOT", True, WHITE), (50, y))
        y += 35
        for key in ["Aimbot", "Circle FOV", "Filled FOV", "Square FOV", "Multicolor FOV"]:
            box = draw_checkbox(50, y, key, options["Aimbot"][key])
            boxes[key] = box
            y += 35

        aimbot_fov_knob = draw_slider(400, 80, "Aimbot FOV", options["Aimbot"]["Aimbot FOV"], 100, 600)
        player_render_knob = draw_slider(400, 140, "Player Render", options["Aimbot"]["Player Render"], 100, 1000)
        smoothness_knob = draw_slider(400, 200, "Smoothness", options["Aimbot"]["Smoothness"], 0.1, 5.0)
        bone_dropdown = draw_dropdown(400, 270, "Aimbot Bone", options["Aimbot"]["Aimbot Bone"])
        aimkey_dropdown = draw_dropdown(400, 330, "Aim Key", options["Aimbot"]["Aim Key"])

        if click:
            for key, box in boxes.items():
                if box.collidepoint(mx, my):
                    options["Aimbot"][key] = not options["Aimbot"][key]

        if options["Aimbot"]["Circle FOV"]:
            center = (800, 350)
            radius = int(options["Aimbot"]["Aimbot FOV"] / 2)
            fov_color = get_multicolor_color(frame_count) if options["Aimbot"]["Multicolor FOV"] else options["Aimbot"]["FOV Color"]
            if options["Aimbot"]["Filled FOV"]:
                pygame.draw.circle(screen, fov_color, center, radius)
            else:
                pygame.draw.circle(screen, fov_color, center, radius, 2)

    elif current_tab == "ESP":
        screen.blit(font.render("ESP", True, WHITE), (50, y))
        y += 35
        for key in options["ESP"]:
            box = draw_checkbox(50, y, key, options["ESP"][key])
            boxes[key] = box
            y += 35
        if click:
            for key, box in boxes.items():
                if box.collidepoint(mx, my):
                    options["ESP"][key] = not options["ESP"][key]

    elif current_tab == "Exploits":
        screen.blit(font.render("EXPLOITS", True, WHITE), (50, y))
        y += 35
        for key in options["Exploits"]:
            box = draw_checkbox(50, y, key, options["Exploits"][key])
            boxes[key] = box
            y += 35
        if click:
            for key, box in boxes.items():
                if box.collidepoint(mx, my):
                    options["Exploits"][key] = not options["Exploits"][key]

    frame_count += 1
    pygame.display.flip()
    clock.tick(60)
