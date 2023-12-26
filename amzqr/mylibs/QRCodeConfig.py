from dataclasses import dataclass
import os

@dataclass
class QRCodeConfig:
    words: str
    version: int = 1
    level: str = 'H'
    picture: str = None
    colorized: bool = False
    contrast: float = 1.0
    brightness: float = 1.0
    save_name: str = None
    save_dir: str = os.getcwd()

    def __post_init__(self): # 實例初始化後被呼叫
        self.check()

    def check(self):
        supported_chars = r"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ··,.:;+-*/\~!@#$%^&`'=<>[]()?_{}|"

        # check every parameter
        if not isinstance(self.words, str) or any(i not in supported_chars for i in self.words):
            raise ValueError('Wrong words! Make sure the characters are supported!')
        if not isinstance(self.version, int) or self.version not in range(1, 41):
            raise ValueError('Wrong version! Please choose a int-type value from 1 to 40!')
        if not isinstance(self.level, str) or len(self.level)>1 or self.level not in 'LMQH':
            raise ValueError("Wrong level! Please choose a str-type level from {'L','M','Q','H'}!")
        if self.picture:
            if not isinstance(self.picture, str) or not os.path.isfile(self.picture) or self.picture[-4:] not in ('.jpg','.png','.bmp','.gif'):
                raise ValueError("Wrong picture! Input a filename that exists and be tailed with one of {'.jpg', '.png', '.bmp', '.gif'}!")
            if self.picture[-4:] == '.gif' and self.save_name and self.save_name[-4:] != '.gif':
                raise ValueError('Wrong save_name! If the picuter is .gif format, the output filename should be .gif format, too!')
            if not isinstance(self.colorized, bool):
                raise ValueError('Wrong colorized! Input a bool-type value!')
            if not isinstance(self.contrast, float):
                raise ValueError('Wrong contrast! Input a float-type value!')
            if not isinstance(self.brightness, float):
                raise ValueError('Wrong brightness! Input a float-type value!')
        if self.save_name and (not isinstance(self.save_name, str) or self.save_name[-4:] not in ('.jpg','.png','.bmp','.gif')):
            raise ValueError("Wrong save_name! Input a filename tailed with one of {'.jpg', '.png', '.bmp', '.gif'}!")
        if not os.path.isdir(self.save_dir):
            raise ValueError('Wrong save_dir! Input a existing-directory!')