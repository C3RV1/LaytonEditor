from .UIElement import UIElement


class UIManager:
    def __init__(self):
        self.current_ui_elements = []

    def add(self, element):
        if isinstance(element, list):
            for ele in element:
                self.add(ele)
            return
        if element not in self.current_ui_elements:
            self.current_ui_elements.append(element)

    def remove(self, element):
        if isinstance(element, list):
            for ele in element:
                self.remove(ele)
            return
        if element in self.current_ui_elements:
            self.current_ui_elements.remove(element)

    def clear(self):
        self.current_ui_elements = []

    def update(self):
        already_interacted = False
        for element in self.current_ui_elements:
            if not isinstance(element, UIElement):
                continue
            if not callable(element.check_interacting):
                continue

            if already_interacted:
                pre_interact = element.interact
                element.interacting = False
                if callable(element.post_interact) and pre_interact:
                    element.post_interact()
                continue

            pre_interact = element.interacting

            element.check_interacting()

            if pre_interact and not element.interacting and callable(element.post_interact):
                element.post_interact()

            if not pre_interact and element.interacting and callable(element.pre_interact):
                element.pre_interact()

            if element.interacting and callable(element.interact):
                already_interacted = True
                element.interact()
        return already_interacted

