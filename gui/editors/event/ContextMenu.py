from PySide6 import QtWidgets


class CommandListContextMenu(QtWidgets.QMenu):
    def __init__(self):
        super().__init__()
        screen_menu = self.addMenu("Screen")
        if True:
            fade_action = screen_menu.addAction("Fade")
            load_background_action = screen_menu.addAction("Load Background")
            set_bottom_tint_action = screen_menu.addAction("Set Bottom Tint")
            shake_action = screen_menu.addAction("Shake")
            flash_bottom_action = screen_menu.addAction("Flash Bottom")
        dialogue_menu = self.addMenu("Dialogue")
        if True:
            dialogue_line_action = dialogue_menu.addAction("Dialogue Line")
            voice_clip_action = dialogue_menu.addAction("Voice Clip")
        character_menu = self.addMenu("Character")
        if True:
            set_visibility_action = character_menu.addAction("Set Visibility")
            set_slot_action = character_menu.addAction("Set Slot")
            set_animation_action = character_menu.addAction("Set Animation")
            shake_action = character_menu.addAction("Shake")
        sequencing_menu = self.addMenu("Sequencing")
        if True:
            set_mode_action = sequencing_menu.addAction("Set Mode")
            set_mode_id_action = sequencing_menu.addAction("Set Mode ID")
        wait_action = self.addAction("Wait")
        self.addSeparator()
        audio_menu = self.addMenu("Audio")
        if True:
            sound_effect_action = audio_menu.addAction("Sound Effect")
            stop_train_sound_action = audio_menu.addAction("Stop Train Sound")
            play_music_action = audio_menu.addAction("Play Music")
            fade_music_action = audio_menu.addAction("Fade Music")
        progression_menu = self.addMenu("Progression")
        if True:
            unlock_journal_action = progression_menu.addAction("Unlock Journal")
            mystery_action = progression_menu.addAction("Reveal/Solve Mystery")
            send_puzzles_action = progression_menu.addAction("Send Puzzles to Granny Riddleton")
            item_action = progression_menu.addAction("Pick Up/Remove Item")
            save_prompt_action = progression_menu.addAction("Save Progress Prompt")
            unlock_minigame_action = progression_menu.addAction("Unlock Minigame")
            companion_action = progression_menu.addAction("Companion")
            complete_game_action = progression_menu.addAction("Complete Game")
        start_tea_action = self.addAction("Start Tea")

