import hashlib
import uuid

import pytest

from keygen.transforms import Algorythm


class TestAlgorythm:
    def test_enum_values(self):
        assert str(Algorythm.MD5) == 'md5'
        assert str(Algorythm.SHA1) == 'sha1'
        assert str(Algorythm.SHA224) == 'sha224'
        assert str(Algorythm.SHA256) == 'sha256'
        assert str(Algorythm.SHA384) == 'sha384'
        assert str(Algorythm.SHA512) == 'sha512'
        assert str(Algorythm.UUID) == 'uuid'

    def test_md5_apply(self):
        test_value = 'test_string'
        result = Algorythm.MD5.apply(test_value)
        expected = hashlib.md5(test_value.encode()).hexdigest()
        assert result == expected
        assert len(result) == 32

    def test_sha1_apply(self):
        test_value = 'test_string'
        result = Algorythm.SHA1.apply(test_value)
        expected = hashlib.sha1(test_value.encode()).hexdigest()
        assert result == expected
        assert len(result) == 40

    def test_sha224_apply(self):
        test_value = 'test_string'
        result = Algorythm.SHA224.apply(test_value)
        expected = hashlib.sha224(test_value.encode()).hexdigest()
        assert result == expected
        assert len(result) == 56

    def test_sha256_apply(self):
        test_value = 'test_string'
        result = Algorythm.SHA256.apply(test_value)
        expected = hashlib.sha256(test_value.encode()).hexdigest()
        assert result == expected
        assert len(result) == 64

    def test_sha384_apply(self):
        test_value = 'test_string'
        result = Algorythm.SHA384.apply(test_value)
        expected = hashlib.sha384(test_value.encode()).hexdigest()
        assert result == expected
        assert len(result) == 96

    def test_sha512_apply(self):
        test_value = 'test_string'
        result = Algorythm.SHA512.apply(test_value)
        expected = hashlib.sha512(test_value.encode()).hexdigest()
        assert result == expected
        assert len(result) == 128

    def test_uuid_apply(self):
        test_value = 'test_string'
        result = Algorythm.UUID.apply(test_value)
        expected = str(uuid.uuid3(uuid.NAMESPACE_OID, test_value))
        assert result == expected
        # UUID format: 8-4-4-4-12 characters
        assert len(result) == 36
        assert result.count('-') == 4

    def test_apply_with_empty_string(self):
        empty = ''
        assert Algorythm.MD5.apply(empty) == hashlib.md5(empty.encode()).hexdigest()
        assert Algorythm.SHA256.apply(empty) == hashlib.sha256(empty.encode()).hexdigest()
        assert Algorythm.UUID.apply(empty) == str(uuid.uuid3(uuid.NAMESPACE_OID, empty))

    def test_apply_with_unicode(self):
        test_value = 'тест 测试 🔑'
        result = Algorythm.MD5.apply(test_value)
        expected = hashlib.md5(test_value.encode()).hexdigest()
        assert result == expected

    def test_all_algorithms_return_string(self):
        test_value = 'test'
        for algo in Algorythm:
            result = algo.apply(test_value)
            assert isinstance(result, str)
            assert len(result) > 0

    def test_deterministic_output(self):
        test_value = 'deterministic_test'
        for algo in Algorythm:
            result1 = algo.apply(test_value)
            result2 = algo.apply(test_value)
            assert result1 == result2
