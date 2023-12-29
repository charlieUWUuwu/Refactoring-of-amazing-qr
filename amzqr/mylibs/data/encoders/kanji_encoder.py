from ..base_encoder import BaseEncoder

class KanjiEncoder(BaseEncoder):
    def __init__(self, ver, ecl):
        super().__init__(ver, ecl, mode='kanji')

    def get_code(self, str):
        pass