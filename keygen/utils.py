import string


SAFE_EXCLUDE = set(";\"'\\`$")


def build_charset(signature: str, safe: bool = True) -> str:
    charset = ''
    if 'u' in signature:
        charset += string.ascii_uppercase
    if 'l' in signature:
        charset += string.ascii_lowercase
    if 'd' in signature:
        charset += string.digits
    if 'p' in signature:
        charset += string.punctuation
    if 'h' in signature:
        charset += string.hexdigits
    if 'o' in signature:
        charset += string.octdigits
    if 'b' in signature:
        charset += '01'

    if safe:
        charset = ''.join([c for c in charset if c not in SAFE_EXCLUDE])

    return ''.join(sorted(set(charset)))
