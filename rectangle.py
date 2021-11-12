class Rectangle:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.x2 = x + width
        self.y2 = y + width
        self.width = width
        self.color = 'black'

    # Drawable coordinates
    def setColor(self, newColor):
        self.color = newColor