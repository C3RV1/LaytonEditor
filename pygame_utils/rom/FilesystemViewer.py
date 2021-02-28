import PygameEngine.GameManager
import PygameEngine.UI.Button
import PygameEngine.UI.Text
import PygameEngine.UI.UIElement
import PygameEngine.UI.UIManager
import PygameEngine.Camera
import PygameEngine.Screen
import PygameEngine.Input
import PygameEngine.Sprite
from PygameEngine.Debug import Debug
from PygameEngine import Renderer
import pygame as pg
from pygame_utils.rom.rom_extract import load_bg, load_animation
from pygame_utils.rom import RomSingleton


class ButtonWithText(PygameEngine.UI.UIElement.UIElement, PygameEngine.UI.Text.Text):
    def __init__(self, groups):
        PygameEngine.UI.UIElement.UIElement.__init__(self)
        PygameEngine.UI.Text.Text.__init__(self, groups)

        self.command = None

        self.check_interacting = self._check_interacting
        self.interact = self._interact

    def _check_interacting(self):
        mouse_pos = PygameEngine.Input.Input().get_screen_mouse_pos()
        if PygameEngine.Input.Input().get_mouse_down(1):
            if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.interacting = True
                return
        self.interacting = False

    def _interact(self):
        if callable(self.command):
            self.command()


class FilesystemViewer(Renderer.Renderer):
    def __init__(self, render_rect):
        super(FilesystemViewer, self).__init__()
        self.rom = RomSingleton.RomSingleton().rom

        self.group = pg.sprite.LayeredDirty()
        self.camera = PygameEngine.Camera.Camera()
        self.camera.display_port = render_rect
        self.group.set_clip(self.camera.display_port)

        self.camera.cam_alignment = [PygameEngine.Sprite.Sprite.ALIGNMENT_RIGHT, PygameEngine.Sprite.Sprite.ALIGNMENT_BOTTOM]
        self.blank_surface.fill(pg.Color(20, 20, 20))

        self.preview_group = pg.sprite.LayeredDirty()
        self.preview_camera = PygameEngine.Camera.Camera()
        self.preview_camera.display_port = pg.Rect(render_rect.x + 256 * 2, 1080 - 192 * 2, 256 * 2, 192 * 2)
        self.preview_group.set_clip(self.preview_camera.display_port)

        self.preview_sprite = PygameEngine.Sprite.Sprite([])
        self.preview_sprite.is_world = False
        # self.preview_sprite.world_rect.x = 256 * 2
        # self.preview_sprite.world_rect.y += 192

        self.ui_manager = PygameEngine.UI.UIManager.UIManager()
        self.button_y = 0

    def fill(self):
        self.screen.fill(pg.Color(120, 120, 120), rect=self.camera.display_port)

    def load(self):
        # load_bg("data_lt2/bg/map/main10.arc", self.sprite_test)
        self.open_folder("data_lt2/")

    def change_to_folder(self, folder_path):
        Debug.log(f"Changing to folder: {folder_path}", self)
        self.open_folder(folder_path + "/")

    def change_to_file(self, file_path):
        Debug.log(f"Changing to file: {file_path}", self)
        if file_path.endswith(".arc"):
            try:
                load_animation(file_path, self.preview_sprite)
                if self.preview_sprite.frame_count > 0:
                    self.preview_sprite.set_frame(1)
            except:
                load_bg(file_path, self.preview_sprite)
            self.preview_sprite.add(self.preview_group)

    def create_new_folder(self, name, mapping_path):
        new_button = ButtonWithText(self.group)
        new_button.draw_alignment[0] = new_button.ALIGNMENT_RIGHT
        new_button.draw_alignment[1] = new_button.ALIGNMENT_TOP
        new_button.set_font(None, 22)
        new_button.set_text(name, color=(255, 0, 255))
        new_button.world_rect.y += self.button_y
        self.button_y += 22

        path = mapping_path
        new_button.command = lambda folder_path=path: self.change_to_folder(mapping_path)

        self.ui_manager.add(new_button)

    def create_new_file(self, name, mapping_path):
        new_button = ButtonWithText(self.group)
        new_button.draw_alignment[0] = new_button.ALIGNMENT_RIGHT
        new_button.draw_alignment[1] = new_button.ALIGNMENT_TOP
        new_button.set_font(None, 22)
        new_button.set_text(name, color=(255, 255, 0))
        new_button.world_rect.y += self.button_y
        self.button_y += 22

        path = mapping_path
        new_button.command = lambda folder_path=path: self.change_to_file(mapping_path)

        self.ui_manager.add(new_button)

    def open_folder(self, path, show_folders=True):
        self.button_y = 0
        for current_button in self.ui_manager.current_ui_elements:  # type: PygameEngine.Sprite.Sprite
            current_button.kill()
        self.ui_manager.clear()
        if path == "/":
            folders = [fol[0] for fol in self.rom.filenames.folders]
            files = self.rom.filenames.files
        else:
            folders = [fol[0] for fol in self.rom.filenames[path].folders]
            files = self.rom.filenames[path].files
        if show_folders:
            if path != "/":
                self.create_new_folder("..", "/".join(path.split("/")[:-2]))
            for folder_name in folders:
                folder_path = path + folder_name
                self.create_new_folder(folder_name, folder_path)
        for file_name in files:
            file_path = path + file_name
            self.create_new_file(file_name, file_path)

    def clear(self):
        self.group.clear(self.screen, self.blank_surface)
        self.preview_group.clear(self.screen, self.blank_surface)

    def update(self):
        if self.inp.quit:
            self.running = False
        if self.inp.get_mouse_up(4):
            self.camera.position[1] += 2000 * self.gm.delta_time
        if self.inp.get_mouse_up(5):
            self.camera.position[1] -= 2000 * self.gm.delta_time
        self.ui_manager.update()

    def draw(self):
        self.camera.draw(self.group)
        self.preview_camera.draw(self.preview_group)
        dirty = self.group.draw(self.screen)
        dirty.extend(self.preview_group.draw(self.screen))
        return dirty
