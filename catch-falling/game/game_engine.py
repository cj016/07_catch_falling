"""
GameEngine: owns the basket and all falling objects.

Starter version: basket movement and spawning both work at a basic
level (Tasks 2 and 3 ask you to improve them), there's no speed boost
yet (Task 4 builds it from scratch), and catch detection has two
known bugs (see game/collision.py and the catch-checking loop below)
that Task 1 asks you to fix.
"""

import random
import pygame

from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 50
MAX_MISSES = 5
SPAWN_INTERVAL_MIN = 30      # frames
SPAWN_INTERVAL_MAX = 70
MAX_OBJECTS = 8              # cap on simultaneous falling objects
MIN_SPAWN_SEPARATION = 100   # px: next spawn must be at least this far from the last
OBJECT_RADIUS = 14

class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []
        self.frames_until_spawn = 0
        self.last_spawn_x = None
        self.score = 0
        self.misses = 0
        self.game_over = False

    def _pick_spawn_x(self):
        # Object centers must stay at least one radius from each edge so the
        # whole circle is inside the playable area.
        lo = OBJECT_RADIUS
        hi = WIDTH - OBJECT_RADIUS

        if self.last_spawn_x is None:
            return random.randint(lo, hi)

        last = self.last_spawn_x
        sep = MIN_SPAWN_SEPARATION

        # Valid x ranges: [lo, last - sep] on the left, [last + sep, hi] on the right.
        left_len = max(0, (last - sep) - lo)
        right_len = max(0, hi - (last + sep))
        total = left_len + right_len

        if total <= 0:
            # Separation can't be satisfied (e.g. a very large value): go to the
            # farther edge.
            return lo if (last - lo) > (hi - last) else hi

        # Pick uniformly across both valid ranges, weighted by their length.
        pick = random.uniform(0, total)
        if pick < left_len:
            return int(lo + pick)
        return int(last + sep + (pick - left_len))

    def _spawn_object(self):
        x = self._pick_spawn_x()
        self.objects.append(
            FallingObject(x=x, y=-OBJECT_RADIUS, radius=OBJECT_RADIUS, speed=3)
        )
        self.last_spawn_x = x

    def _spawn_object(self):
        x = random.randint(20, WIDTH - 20)
        self.objects.append(FallingObject(x=x, y=-14, speed=3))

    def handle_input(self, keys_pressed):
        if self.game_over:
            return

        # Net direction: -1, 0 or +1. If both keys are held they cancel out,
        # instead of the basket drifting right because RIGHT is checked last.
        direction = keys_pressed[pygame.K_RIGHT] - keys_pressed[pygame.K_LEFT]
        self.basket.x += direction * self.basket.speed

        # Basket x is its center, so keep the center at least half a width
        # away from each edge. That keeps the whole rect on screen.
        half = self.basket.width / 2
        self.basket.x = max(half, min(WIDTH - half, self.basket.x))

    def handle_keydown(self, key):
        if self.game_over:
            if key == pygame.K_r:
                self.__init__()
            return
        if key in (pygame.K_SPACE, pygame.K_LSHIFT, pygame.K_RSHIFT):
            self.basket.activate_boost()

    def update(self):
        if self.game_over:
            return
        self.basket.update()

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            if len(self.objects) < MAX_OBJECTS:
                self._spawn_object()
            self.frames_until_spawn = random.randint(SPAWN_INTERVAL_MIN, SPAWN_INTERVAL_MAX)

        for obj in self.objects:
            obj.update()

        basket_rect = self.basket.get_rect()
        remaining = []
        for obj in self.objects:
            if is_caught(basket_rect, obj):
                self.score += 1
            else:
                remaining.append(obj)
        self.objects = remaining

        missed = [o for o in self.objects if o.is_past_bottom(HEIGHT)]
        if missed:
            self.objects = [o for o in self.objects if not o.is_past_bottom(HEIGHT)]
            self.misses += len(missed)
            if self.misses >= MAX_MISSES:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.basket, self.objects)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Misses: {self.misses}/{MAX_MISSES}", (10, 36))
        renderer.draw_boost_hud(surface, font, self.basket)

        if self.game_over:
            renderer.draw_banner(surface, font, f"Game Over! Final score: {self.score}. Press R to restart.")
