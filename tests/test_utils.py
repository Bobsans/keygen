import string

import pytest

from keygen.utils import SAFE_EXCLUDE, build_charset


class TestBuildCharset:
    def test_uppercase_only(self):
        result = build_charset('u')
        assert result == ''.join(sorted(set(string.ascii_uppercase)))
        assert len(result) == 26

    def test_lowercase_only(self):
        result = build_charset('l')
        assert result == ''.join(sorted(set(string.ascii_lowercase)))
        assert len(result) == 26

    def test_digits_only(self):
        result = build_charset('d')
        assert result == ''.join(sorted(set(string.digits)))
        assert len(result) == 10

    def test_punctuation_only_safe(self):
        result = build_charset('p', safe=True)
        expected = ''.join(sorted(set(c for c in string.punctuation if c not in SAFE_EXCLUDE)))
        assert result == expected

    def test_punctuation_only_unsafe(self):
        result = build_charset('p', safe=False)
        expected = ''.join(sorted(set(string.punctuation)))
        assert result == expected

    def test_hexdigits_only(self):
        result = build_charset('h')
        assert result == ''.join(sorted(set(string.hexdigits)))

    def test_octdigits_only(self):
        result = build_charset('o')
        assert result == ''.join(sorted(set(string.octdigits)))

    def test_binary_only(self):
        result = build_charset('b')
        assert result == '01'

    def test_combined_ul(self):
        result = build_charset('ul')
        expected = ''.join(sorted(set(string.ascii_uppercase + string.ascii_lowercase)))
        assert result == expected

    def test_combined_uld(self):
        result = build_charset('uld')
        expected = ''.join(sorted(set(
            string.ascii_uppercase + string.ascii_lowercase + string.digits
        )))
        assert result == expected

    def test_combined_uldp_safe(self):
        result = build_charset('uldp', safe=True)
        charset = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
        expected = ''.join(sorted(set(c for c in charset if c not in SAFE_EXCLUDE)))
        assert result == expected

    def test_combined_uldp_unsafe(self):
        result = build_charset('uldp', safe=False)
        charset = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
        expected = ''.join(sorted(set(charset)))
        assert result == expected

    def test_safe_excludes_dangerous_chars(self):
        result = build_charset('p', safe=True)
        for char in SAFE_EXCLUDE:
            assert char not in result

    def test_unsafe_includes_dangerous_chars(self):
        result = build_charset('p', safe=False)
        for char in SAFE_EXCLUDE:
            if char in string.punctuation:
                assert char in result

    def test_empty_signature(self):
        result = build_charset('')
        assert result == ''

    def test_duplicate_signature(self):
        result1 = build_charset('uu')
        result2 = build_charset('u')
        assert result1 == result2

    def test_no_duplicates_in_result(self):
        result = build_charset('uldp')
        assert len(result) == len(set(result))

    def test_result_is_sorted(self):
        result = build_charset('uldp')
        assert result == ''.join(sorted(result))
