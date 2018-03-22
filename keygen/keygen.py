import random
import string
import sys
from argparse import ArgumentParser, RawTextHelpFormatter


def main():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-s', '--symbols', dest='symbols', default='uldp', type=str, help='Symbols can set of next vals:\n  u - ASCII uppercase letters\n  l - ASCII lowеrcase letters\n  d - digits\n  p - punctuation\n  h - HEX digits\n  o - OCT digits\n  b - BIN digits\nDefault: uldp')
    parser.add_argument('-l', '--length', dest='length', default=32, type=int, help='Length of generated key\nDefault: 32')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Output more info\nDefault: false')
    args = parser.parse_args()

    invalid = ''.join(filter(lambda s: s not in 'uldphob', args.symbols))
    if invalid:
        sys.stderr.write(f'Invalid symbol set identifier: "{invalid}".\n')
        exit()

    chars = ''
    if 'u' in args.symbols:
        chars += string.ascii_uppercase
    if 'l' in args.symbols:
        chars += string.ascii_lowercase
    if 'd' in args.symbols:
        chars += string.digits
    if 'p' in args.symbols:
        chars += string.punctuation
    if 'h' in args.symbols:
        chars += string.hexdigits
    if 'o' in args.symbols:
        chars += string.octdigits
    if 'b' in args.symbols:
        chars += '01'

    charset = list(set(chars))

    result = ''.join([random.choice(charset) for _ in range(args.length)])

    if args.verbose:
        sys.stdout.write(f'Symbols: {chars}\n')
        sys.stdout.write(f'Length:  {args.length}\n')
        sys.stdout.write(f'Result:  {result}\n')
    else:
        sys.stdout.write(f'{result}\n')


if __name__ == '__main__':
    main()
