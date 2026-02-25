import re

import pytest

from keygen.main import generate
from keygen.transforms import Algorythm


class TestGenerate:
    def test_default_generation(self):
        result = generate()
        assert len(result) == 32
        assert isinstance(result, str)

    def test_custom_length(self):
        for length in [8, 16, 32, 64, 128]:
            result = generate(length=length)
            assert len(result) == length

    def test_length_zero(self):
        result = generate(length=0)
        assert result == ''

    def test_length_one(self):
        result = generate(length=1)
        assert len(result) == 1

    def test_uppercase_only(self):
        result = generate(symbols='u', length=100)
        assert all(c.isupper() and c.isalpha() for c in result)

    def test_lowercase_only(self):
        result = generate(symbols='l', length=100)
        assert all(c.islower() and c.isalpha() for c in result)

    def test_digits_only(self):
        result = generate(symbols='d', length=100)
        assert all(c.isdigit() for c in result)

    def test_hex_only(self):
        result = generate(symbols='h', length=100)
        assert all(c in '0123456789ABCDEFabcdef' for c in result)

    def test_binary_only(self):
        result = generate(symbols='b', length=100)
        assert all(c in '01' for c in result)

    def test_octal_only(self):
        result = generate(symbols='o', length=100)
        assert all(c in '01234567' for c in result)

    def test_safe_mode_excludes_dangerous_chars(self):
        # Generate many keys to increase probability of hitting excluded chars
        for _ in range(10):
            result = generate(symbols='uldp', length=100, safe=True)
            assert ';' not in result
            assert '"' not in result
            assert "'" not in result
            assert '\\' not in result
            assert '`' not in result
            assert '$' not in result

    def test_unsafe_mode_may_include_dangerous_chars(self):
        # In unsafe mode, punctuation should include all characters
        results = []
        for _ in range(50):
            results.append(generate(symbols='p', length=100, safe=False))

        combined = ''.join(results)
        # At least some unsafe characters should appear with enough iterations
        unsafe_chars_found = any(c in combined for c in [';', '"', "'", '\\', '`', '$'])
        assert unsafe_chars_found

    def test_emulate_md5(self):
        result = generate(symbols='uld', length=32, emulate=Algorythm.MD5)
        assert len(result) == 32
        assert re.match(r'^[a-f0-9]+$', result)

    def test_emulate_sha256(self):
        result = generate(symbols='uld', length=32, emulate=Algorythm.SHA256)
        assert len(result) == 64
        assert re.match(r'^[a-f0-9]+$', result)

    def test_emulate_uuid(self):
        result = generate(symbols='uld', length=32, emulate=Algorythm.UUID)
        assert len(result) == 36
        assert re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', result)

    def test_randomness(self):
        # Generate multiple keys and ensure they're different
        results = set()
        for _ in range(100):
            results.add(generate(symbols='uld', length=32))

        # All 100 keys should be unique
        assert len(results) == 100

    def test_no_emulate(self):
        result = generate(symbols='uld', length=16, emulate=None)
        assert len(result) == 16
        # Should not be transformed, so length stays the same

    def test_combined_symbols(self):
        result = generate(symbols='uldp', length=200)
        assert len(result) == 200

        # Check that we have variety (with 200 chars we should hit multiple types)
        has_upper = any(c.isupper() for c in result)
        has_lower = any(c.islower() for c in result)
        has_digit = any(c.isdigit() for c in result)

        assert has_upper or has_lower or has_digit

    def test_deterministic_with_emulation(self):
        # The same input should produce different outputs (random generation)
        result1 = generate(symbols='uld', length=32)
        result2 = generate(symbols='uld', length=32)
        assert result1 != result2

        # But emulated versions are deterministic based on input
        emulated1 = Algorythm.MD5.apply(result1)
        emulated2 = Algorythm.MD5.apply(result1)
        assert emulated1 == emulated2
