from .UIElement import UIElement


class UIManager:
    def __init__(self):
        self.current_ui_elements = []

    def add(self, element):
        if isinstance(element, list):
            for ele in element:
                self.add(ele)
            return
        self.current_ui_elements.append(element)

    def remove(self, element):
        if isinstance(element, list):
            for ele in element:
                self.remove(ele)
            return
        self.current_ui_elements.remove(element)

    def clear(self):
        self.current_ui_elements = []

    def update(self):
        already_interacted = False
        for element in self.current_ui_elements:
            if not isinstance(element, UIElement):
                continue
            if element.check_interacting is None:
                continue

            if already_interacted:
                element.interacting = False
                if element.post_interact is not None:
                    element.post_interact()
                continue

            pre_interact = element.interacting

            element.check_interacting()

            if pre_interact and not element.interacting and element.post_interact is not None:
                element.post_interact()

            if not pre_interact and element.interacting and element.pre_interact is not None:
                element.pre_interact()

            if element.interacting and element.interact is not None:
                already_interacted = True
                element.interact()
        return already_interacted

