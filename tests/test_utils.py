import pytest
from employee_tracker.utils.ids import new_id, check_id

class TestIDCreation:
    def test_id_prefix_used(self):
        result = new_id("idtest")
        assert result.startswith("idtest")
    def test_id_suffix_characters_are_hex(self):
        result = new_id("id")
        suffix = result.split("_")[1]
        assert isinstance(int(suffix,16),int)
    def test_id_has_8_hex_chars(self):
        result = new_id("id")
        suffix = result.split("_")[1]
        assert len(suffix) == 8
    def test_ids_created_are_unique(self):
        id_1 = new_id("id")
        id_2 = new_id("id")
        id_3 = new_id("id")
        id_4 = new_id("id")

        assert id_1 != id_2 and id_1 != id_3 and id_1 != id_4 and id_2 != id_3 and id_2 != id_4 and id_3 != id_4 

class TestIDChecker:
    def test_correct_id_passes(self):
        id = new_id("test")
        assert check_id(id,"test") is True
    def test_wrong_prefix_fails(self):
        id = new_id("test")
        assert check_id(id,"test2") is False
    def test_too_short_fails(self):
        id = new_id("test")
        id_split = id.split("_")
        id_split[1] = id_split[1][0:5]
        id = "_".join(id_split)
        assert check_id(id,"test") is False
    def test_too_long_fails(self):
        id = new_id("test")
        id_split = id.split("_")
        id_split[1] = id_split[1]+"88"
        id = "_".join(id_split)
        assert check_id(id,"test") is False
    def test_nonhex_fails(self):
        id = new_id("test")
        id_split = id.split("_")
        suffix = id_split[1]
        id_split[1] = suffix[0:2] + "Z" + suffix[3:]
        id = "_".join(id_split)
        assert check_id(id,"test") is False
        