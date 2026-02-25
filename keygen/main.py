import secrets
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

from keygen.transforms import Algorythm
from keygen.utils import build_charset


def generate(symbols: str = 'uldp', length: int = 32, emulate: Algorythm = None, safe: bool = True):
    charset = build_charset(symbols, safe)
    result = ''.join([secrets.choice(charset) for _ in range(length)])
    if emulate:
        result = emulate.apply(result)
    return result


def main():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-s', '--symbols', dest='symbols', default='uldp', type=str, help='Symbols can set of next vals:\n  u - ASCII uppercase letters\n  l - ASCII lowеrcase letters\n  d - digits\n  p - punctuation\n  h - HEX digits\n  o - OCT digits\n  b - BIN digits\nDefault: uldp')
    parser.add_argument('-l', '--length', dest='length', default=32, type=int, help='Length of generated key\nDefault: 32')
    parser.add_argument('-e', '--emulate', dest='emulate', type=Algorythm, choices=list(Algorythm), help='Emulate result of encryption algorithm\nSupports algorithms: %s\nDefault: None' % ', '.join([str(v) for v in Algorythm]))
    parser.add_argument('--unsafe', dest='unsafe', action='store_true', help='Allow potentially unsafe characters in the output (includes ; " \\\' \\\\ ` $)\nDefault: False (safe mode)')

    args = parser.parse_args()

    invalid_symbols = ''.join(filter(lambda s: s not in 'uldphob', args.symbols))
    if invalid_symbols:
        sys.stderr.write('Invalid symbol set identifier: "%s".\n' % invalid_symbols)
        exit()

    sys.stdout.write('%s\n' % generate(args.symbols, args.length, args.emulate, not args.unsafe))


if __name__ == '__main__':
    main()
