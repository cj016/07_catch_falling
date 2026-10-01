"""
collision: figures out whether a falling object is within the basket.
"""


def is_caught(basket_rect, obj):
    within_x = basket_rect.left <= obj.x <= basket_rect.right
    reached_basket = obj.y + obj.radius >= basket_rect.top    # bottom edge touches basket top
    not_below_basket = obj.y - obj.radius <= basket_rect.bottom  # hasn't fallen past it
    return within_x and reached_basket and not_below_basket