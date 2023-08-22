from numtofi import number_to_text, number_to_text_length
import unittest

class TestNumToFiCore(unittest.TestCase):

    number_tests = {
        # Base numbers
        0: ('nolla', 'nolla'),
        1: ('yksi', 'yksi'),
        10: ('kymmenen', 'kymmenen'),

        # Numbers from 1-19
        11: ('yksitoista', 'yksitoista'),
        15: ('viisitoista', 'viisitoista'),
        19: ('yhdeksäntoista', 'yhdeksäntoista'),

        # Numbers from 20-99
        20: ('kaksikymmentä', 'kaksikymmentä'),
        21: ('kaksikymmentäyksi', 'kaksikymmentäyksi'),
        35: ('kolmekymmentäviisi', 'kolmekymmentäviisi'),
        99: ('yhdeksänkymmentäyhdeksän', 'yhdeksänkymmentäyhdeksän'),

        # Numbers in the 100s
        100: ('sata', 'sata'),
        101: ('satayksi', 'satayksi'),
        150: ('sataviisikymmentä', 'sataviisikymmentä'),
        199: ('satayhdeksänkymmentäyhdeksän', 'satayhdeksänkymmentäyhdeksän'),

        # Numbers in the 200s
        200: ('kaksisataa', 'kaksisataa'),
        202: ('kaksisataakaksi', 'kaksisataakaksi'),
        250: ('kaksisataaviisikymmentä', 'kaksisataaviisikymmentä'),
        299: ('kaksisataayhdeksänkymmentäyhdeksän', 'kaksisataayhdeksänkymmentäyhdeksän'),

        # Numbers in the 1000s
        1000: ('tuhat', 'tuhat'),
        1001: ('tuhatyksi', 'tuhatyksi'),
        1010: ('tuhatkymmenen', 'tuhatkymmenen'),
        1100: ('tuhatsata', 'tuhatsata'),
        1999: ('tuhatyhdeksänsataayhdeksänkymmentäyhdeksän', 'tuhatyhdeksänsataayhdeksänkymmentäyhdeksän'),

        # Numbers in the 2000s
        2000: ('kaksituhatta', 'kaksituhatta'),
        2002: ('kaksituhattakaksi', 'kaksituhatta kaksi'),
        2020: ('kaksituhattakaksikymmentä', 'kaksituhatta kaksikymmentä'),
        2200: ('kaksituhattakaksisataa', 'kaksituhatta kaksisataa'),

        # Larger numbers
        30000: ('kolmekymmentätuhatta', 'kolmekymmentätuhatta'),
        33000: ('kolmekymmentäkolmetuhatta', 'kolmekymmentäkolmetuhatta'),
        33300: ('kolmekymmentäkolmetuhattakolmesataa', 'kolmekymmentäkolmetuhatta kolmesataa'),
        400000: ('neljäsataatuhatta', 'neljäsataatuhatta'),
        400400: ('neljäsataatuhattaneljäsataa', 'neljäsataatuhatta neljäsataa'),

        1000000: ('miljoona', 'miljoona'),
        1100000: ('miljoonasatatuhatta', 'miljoonasatatuhatta'),
        1100100: ('miljoonasatatuhattasata', 'miljoonasatatuhatta sata'),
        1010100: ('miljoonakymmenentuhattasata', 'miljoonakymmenentuhatta sata'),
        1001100: ('miljoonatuhatsata', 'miljoonatuhatsata'),
        1002100: ('miljoonakaksituhattasata', 'miljoonakaksituhatta sata'),

        2000000: ('kaksimiljoonaa', 'kaksi miljoonaa'),
        2200000: ('kaksimiljoonaakaksisataatuhatta', 'kaksimiljoonaa kaksisataatuhatta'),
        2020000: ('kaksimiljoonaakaksikymmentätuhatta', 'kaksimiljoonaa kaksikymmentätuhatta'),
        2002000: ('kaksimiljoonaakaksituhatta', 'kaksimiljoonaa kaksituhatta'),
        2000200: ('kaksimiljoonaakaksisataa', 'kaksimiljoonaa kaksisataa'),
        2000020: ('kaksimiljoonaakaksikymmentä', 'kaksimiljoonaa kaksikymmentä'),
        2000002: ('kaksimiljoonaakaksi', 'kaksimiljoonaa kaksi'),
        2200200: ('kaksimiljoonaakaksisataatuhattakaksisataa', 'kaksimiljoonaa kaksisataatuhatta kaksisataa'),

        1000000000: ('miljardi', 'miljardi'),
        9000000000: ('yhdeksänmiljardia', 'yhdeksän miljardia'),
        1000000000000: ('biljoona', 'biljoona'),
        1000000000000000: ('triljoona', 'triljoona'),

        # Maximum number
        999999999999999999: ('yhdeksänsataayhdeksänkymmentäyhdeksäntriljoonaayhdeksänsataayhdeksänkymmentäyhdeksänbiljoonaayhdeksänsataayhdeksänkymmentäyhdeksänmiljardiayhdeksänsataayhdeksänkymmentäyhdeksänmiljoonaayhdeksänsataayhdeksänkymmentäyhdeksäntuhattayhdeksänsataayhdeksänkymmentäyhdeksän', 'yhdeksänsataayhdeksänkymmentäyhdeksäntriljoonaa yhdeksänsataayhdeksänkymmentäyhdeksänbiljoonaa yhdeksänsataayhdeksänkymmentäyhdeksänmiljardia yhdeksänsataayhdeksänkymmentäyhdeksänmiljoonaa yhdeksänsataayhdeksänkymmentäyhdeksäntuhatta yhdeksänsataayhdeksänkymmentäyhdeksän'),
    }

    def _number_to_text_errors(self, func):
        v = -1
        try:
            func(v)
        except ValueError as e:
            assert(f'{e}' == 'Number must be a positive integer less than 10^18.')
        # 10^18
        v = 1000000000000000000
        try:
            func(v)
        except ValueError as e:
            assert(f'{e}' == 'Number must be a positive integer less than 10^18.')

    def test_number_to_text(self):
        for num, (no_space, with_space) in self.number_tests.items():
            assert(number_to_text(num) == with_space)
            assert(number_to_text(num, False) == no_space)

    def test_number_to_text_errors(self):
        self._number_to_text_errors(number_to_text)

    def test_number_to_text_length(self):
        for num, (no_space, with_space) in self.number_tests.items():
            assert(number_to_text_length(num) == len(with_space))
            assert(number_to_text_length(num, False) == len(no_space))

    def test_number_to_text_length_errors(self):
        self._number_to_text_errors(number_to_text_length)

if __name__ == '__main__':
    unittest.main()
