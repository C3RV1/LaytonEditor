from formats.puzzle import Puzzle
from formats_parsed.dcc import DCCParser
from formats_parsed.gds_parsers import get_puzzle_gds_parser


class PuzzleDCC:
    def __init__(self, pz=None):
        self.pz = pz
        if self.pz is None:
            self.pz = Puzzle()
        
        self.parser = DCCParser()
    
    def parse(self, data: str):
        self.parser.reset()
        try:
            self.parser.parse(data)
        except Exception as e:
            return False, str(e)

        required_paths = ["pzd.title", "pzd.type", "pzd.number", "pzd.text", "pzd.correct_answer",
                          "pzd.incorrect_answer", "pzd.hint1", "pzd.hint2", "pzd.hint3", "pzd.tutorial_id",
                          "pzd.reward_id", "pzd.bg_btm_id", "pzd.bg_location_id", "pzd.judge_char", "pzd.flag_bit2",
                          "pzd.flag_bit5", "pzd.location_id", "pzd.picarat_decay", "pzd.bg_lang", "pzd.ans_bg_lang"]

        for req_path in required_paths:
            if not self.parser.exists(req_path):
                return False, f"Missing {req_path}"

        self.pz.title = self.parser["pzd.title"]
        self.pz.type = self.parser["pzd.type"]
        self.pz.number = self.parser["pzd.number"]
        self.pz.text = self.parser["pzd.text"]
        self.pz.correct_answer = self.parser["pzd.correct_answer"]
        self.pz.incorrect_answer = self.parser["pzd.incorrect_answer"]
        self.pz.hint1 = self.parser["pzd.hint1"]
        self.pz.hint2 = self.parser["pzd.hint2"]
        self.pz.hint3 = self.parser["pzd.hint3"]

        self.pz.tutorial_id = self.parser["pzd.tutorial_id"]
        self.pz.reward_id = self.parser["pzd.reward_id"]
        self.pz.bg_btm_id = self.parser["pzd.bg_btm_id"]
        self.pz.bg_location_id = self.parser["pzd.bg_location_id"]
        self.pz.judge_char = self.parser["pzd.judge_char"]
        self.pz.flag_bit2 = self.parser["pzd.flag_bit2"]
        self.pz.flag_bit5 = self.parser["pzd.flag_bit5"]
        self.pz.location_id = self.parser["pzd.location_id"]
        self.pz.picarat_decay = []
        for picarat in self.parser["pzd.picarat_decay::unnamed"]:
            self.pz.picarat_decay.append(picarat)

        self.pz.bg_lang = self.parser["pzd.bg_lang"]
        self.pz.ans_bg_lang = self.parser["pzd.ans_bg_lang"]

        gds_parser = get_puzzle_gds_parser(self.pz)
        successful, error_msg = gds_parser.parse_from_dcc(self.pz.gds, self.parser)
        return successful, error_msg
    
    def serialize(self):
        self.parser.reset()
        self.parser.get_path("pzd", create=True)
        self.parser.set_named("pzd.title", self.pz.title)
        self.parser.set_named("pzd.type", self.pz.type)
        self.parser.set_named("pzd.number", self.pz.number)
        self.parser.set_named("pzd.location_id", self.pz.location_id)
        self.parser.set_named("pzd.tutorial_id", self.pz.tutorial_id)
        self.parser.set_named("pzd.reward_id", self.pz.reward_id)
        self.parser.set_named("pzd.bg_btm_id", self.pz.bg_btm_id)
        self.parser.set_named("pzd.bg_location_id", self.pz.bg_location_id)
        self.parser.set_named("pzd.judge_char", self.pz.judge_char)
        self.parser.set_named("pzd.flag_bit2", self.pz.flag_bit2)
        self.parser.set_named("pzd.flag_bit5", self.pz.flag_bit5)
        self.parser.set_named("pzd.bg_lang", self.pz.bg_lang)
        self.parser.set_named("pzd.ans_bg_lang", self.pz.ans_bg_lang)
        self.parser.get_path("pzd.picarat_decay", create=True)
        for picarat in self.pz.picarat_decay:
            self.parser["pzd.picarat_decay::unnamed"].append(picarat)
        self.parser.set_named("pzd.text", self.pz.text)
        self.parser.set_named("pzd.correct_answer", self.pz.correct_answer)
        self.parser.set_named("pzd.incorrect_answer", self.pz.incorrect_answer)
        self.parser.set_named("pzd.hint1", self.pz.hint1)
        self.parser.set_named("pzd.hint2", self.pz.hint2)
        self.parser.set_named("pzd.hint3", self.pz.hint3)

        gds_parser = get_puzzle_gds_parser(self.pz)
        gds_parser.serialize_into_dcc(self.pz.gds, self.parser)
        return self.parser.serialize()
