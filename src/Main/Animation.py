import pygame

class Animation:
    """
    A list of frames
    """

    def add(self, path):
        """
        Adds an image to the list
        """
        frame = pygame.image.load(path).convert_alpha()
        self.frame.append(frame)
        self.width = max(self.width, frame.get_width())
        self.height = max(self.height, frame.get_height())
        return self

    def __init__(self, fps = 15):
        """
        Initializes an empty list
        """
        self.width = 0
        self.height = 0
        self.frame = []
        self.fps = fps
