"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (25, 30, 45)
COLOR_BASKET = (150, 110, 70)
COLOR_TEXT = (255, 255, 255)
COLOR_BASKET_BOOST = (255, 210, 70)
COLOR_BOOST_READY = (110, 220, 130)
COLOR_BOOST_RECHARGE = (140, 150, 170)


def draw_scene(surface, basket, objects):
    surface.fill(COLOR_BG)
    for obj in objects:
        pygame.draw.circle(surface, obj.color, (int(obj.x), int(obj.y)), obj.radius)
    basket_color = COLOR_BASKET_BOOST if basket.is_boosted() else COLOR_BASKET
    rect = basket.get_rect()
    pygame.draw.rect(surface, basket_color, rect, border_radius=6)
    if basket.is_boosted():
        pygame.draw.rect(surface, (255, 255, 255), rect.inflate(6, 6), width=2, border_radius=8)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)

def draw_boost_hud(surface, font, basket):
    pos = (10, 62)
    bar = pygame.Rect(10, 88, 120, 8)

    if basket.is_boosted():
        label, color = "BOOST ACTIVE", COLOR_BASKET_BOOST
        frac = basket.boosted_frames / basket.boost_duration        # drains as it runs out
    elif basket.can_boost():
        label, color = "Boost ready (SPACE)", COLOR_BOOST_READY
        frac = 1.0
    else:
        label, color = "Boost recharging", COLOR_BOOST_RECHARGE
        frac = 1 - basket.cooldown_frames / basket.cooldown_frames_total()
    draw_text(surface, font, label, pos, color)
    pygame.draw.rect(surface, (60, 65, 85), bar, border_radius=4)
    fill = bar.copy()
    fill.width = int(bar.width * frac)
    pygame.draw.rect(surface, color, fill, border_radius=4)