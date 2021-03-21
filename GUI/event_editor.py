import threading
from previewers.event_preview import EventPlayer
from PygameEngine.GameManager import GameManager
from pygame_utils.rom.RomSingleton import RomSingleton
import pygame as pg
from gui.generated import EventEditor
from pygame_utils.rom.rom_extract import clear_extracted


class PygameThread(threading.Thread):
    def __init__(self, event_id, rom):
        super(PygameThread, self).__init__()
        clear_extracted()
        self.rom_singleton = RomSingleton(rom=rom)
        self.current_event_id = event_id
        self.gm = None
        self.has_to_load = threading.Event()
        self.can_load = threading.Event()
        self.can_load.set()
        self.check_gm()
        self.event_player = EventPlayer.EventPlayer(event_id)
        self.event_player.load()
        self.load(event_id)

    def check_gm(self):
        self.gm = GameManager(screen_size=(256 * 2, 194 * 4), name="Event Preview", full_screen=False)

    def load(self, event_id):
        self.check_gm()
        self.has_to_load.set()
        while not self.can_load.isSet():
            pass
        self.current_event_id = event_id

        self.event_player.reset()
        self.event_player.set_event_id(event_id)
        self.event_player.load()
        self.event_player.run_gds_command()

        self.has_to_load.clear()
        self.can_load.clear()

    def run(self) -> None:
        while True:
            while self.event_player.running:
                self.gm.tick()
                dirties = self.event_player.run()
                pg.display.update(dirties)
                if self.has_to_load.isSet():
                    self.can_load.set()
                    while self.has_to_load.isSet():
                        pass
            self.gm.exit()
            self.can_load.set()
            while not self.event_player.running:
                pass
        clear_extracted()

    def end(self):
        self.event_player.running = False


class EventEditor2(EventEditor):
    def __init__(self, parent, rom):
        super(EventEditor2, self).__init__(parent)
        self.rom = rom
        self.pygame_thread: PygameThread = None

    def StartPreviewer(self, event):
        pass

    def OnBtnLoadEvent( self, event ):
        try:
            event_id = int(self.event_id_inp.Value)
        except:
            return
        if self.pygame_thread is None:
            self.pygame_thread = PygameThread(event_id, self.rom)
            self.pygame_thread.start()
        else:
            self.pygame_thread.load(event_id)

    def EndPreviewer(self, event):
        if self.pygame_thread is not None:
            self.pygame_thread.end()
        self.Destroy()
