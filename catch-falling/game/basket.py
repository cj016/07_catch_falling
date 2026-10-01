"""
Basket: the player-controlled catcher at the bottom of the screen.
"""

import pygame


class Basket:
    def __init__(self, x, y, width=90, height=24, speed=5,
                 boost_speed=9, boost_duration=120, boost_cooldown=300):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed                  # effective speed used by movement code
        self.normal_speed = speed
        self.boost_speed = boost_speed
        self.boost_duration = boost_duration    # frames the boost lasts (2 s at 60 FPS)
        self.boost_cooldown = boost_cooldown    # frames from activation until reusable (5 s)
        self.boosted_frames = 0
        self.cooldown_frames = 0

    def is_boosted(self):
        return self.boosted_frames > 0

    def can_boost(self):
        return self.boosted_frames == 0 and self.cooldown_frames == 0

    def activate_boost(self):
        if not self.can_boost():
            return False
        self.boosted_frames = self.boost_duration
        self.cooldown_frames = self.boost_cooldown
        self.speed = self.boost_speed
        return True

    def update(self):
        """Call once per frame to tick the boost and cooldown timers."""
        if self.boosted_frames > 0:
            self.boosted_frames -= 1
            if self.boosted_frames == 0:
                self.speed = self.normal_speed   # automatic return to normal
        if self.cooldown_frames > 0:
            self.cooldown_frames -= 1

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )
    def cooldown_frames_total(self):
        return max(1, self.boost_cooldown - self.boost_duration)