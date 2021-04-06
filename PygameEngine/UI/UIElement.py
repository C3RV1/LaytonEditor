

class UIElement:
    def __init__(self):
        self.interacting = False
        self.check_interacting = None
        self.interact = None
        self.pre_interact = None
        self.post_interact = None
