import unittest
from convert import Converter, ConfigParserException


class TestConfigConverter(unittest.TestCase):
    data = {}

    def setUp(self):
        super().setUp()
        self.converter = Converter('old-test.txt', 'new-test.txt')
        self.converter.convert()
        self.data['test_key_convert'] = {
            "/Scripts/Key Bindings/GUI/Key": 52,
            "/GUI/Key": 52,
            "/Key Bindings/Script Bindings/GUI/Key": 52,
            "/.FAIO/7. dodgeIT/3. Dangerous enemy skills/Table 1/chaos_knight_chaos_bolt {{dodger}}": 1,
            "/Scripts/Script Options/.FAIO/7. dodgeIT/3. Dangerous enemy skills/Table 1/chaos_knight_chaos_bolt {{dodger}}": 1,
            "/Scripts/Script Options/.FAIO/2. Item Usage/1. Offensive items/1. Combo usage/Items/Use Item Shivas Guard": 1,
            "/.FAIO/2. Item Usage/1. Offensive items/1. Combo usage/Items/Use Item Shivas Guard": 1,
            "/.FAIO/6. Last hitter/7. Push key {{lasthit}}": 36,
            "/Key Bindings/Script Bindings/.FAIO/6. Last hitter/7. Push key {{lasthit}}": 36,
            "/Scripts/Key Bindings/.FAIO/6. Last hitter/7. Push key {{lasthit}}": 36,
            "/Scripts/Script Options/.FAIO/3. Hero Scripts/3. Intelligence heroes/Tinker/3. Push mode/1. Tinker push mode": 1,
            "/.FAIO/3. Hero Scripts/3. Intelligence heroes/Tinker/3. Push mode/1. Tinker push mode": 1,
            "/.FAIO/3. Hero Scripts/3. Intelligence heroes/Tinker/3. Push mode/2. Tinker push key {{tinker}}": 58,
            "/Key Bindings/Script Bindings/.FAIO/3. Hero Scripts/3. Intelligence heroes/Tinker/3. Push mode/2. Tinker push key {{tinker}}": 58,
            "/Scripts/Key Bindings/.FAIO/3. Hero Scripts/3. Intelligence heroes/Tinker/3. Push mode/2. Tinker push key {{tinker}}": 58,
            "/Utility/Translate/My Text To": 5,
            "/Utility/Translate/Their Text To": 2,
            "/Awareness/ESP/Illusion ESP": 1,
            "/Awareness/ESP/Illusion ESP/Illusion ESP": 1,
            "/Awareness/ESP/Illusion ESP/Illusion ESP: Hero Floats": 1,
            "/Awareness/ESP/Illusion ESP/Illusion ESP: Show on MiniMap": 1,
            "/Awareness/ESP/Illusion ESP/Illusion ESP: Unselectable": 0,
            "/Hero Specific/Shadow Fiend/Shadowraze Key": 36,
            "/Key Bindings/Shadowraze Key": 36,
            "/.FAIO/3. Hero Scripts/3. Intelligence heroes/Invoker/5. Fast skills/Chaos meteor/2. Activation key {{invoker Chaos meteor}}": 4,
            "/Key Bindings/Script Bindings/.FAIO/3. Hero Scripts/3. Intelligence heroes/Invoker/5. Fast skills/Chaos meteor/2. Activation key {{invoker Chaos meteor}}": 4,
            "/Scripts/Key Bindings/.FAIO/3. Hero Scripts/3. Intelligence heroes/Invoker/5. Fast skills/Chaos meteor/2. Activation key {{invoker Chaos meteor}}": 4,
            "/Scripts/Script Options/Awareness/Show Hidden Spells Plus/Invoker - EMP": 1
        }

    def test_key_convert(self):
        self.assertEqual(self.data['test_key_convert'], self.converter.new_config)

    def test_config_parser_exceptions(self):
        with self.assertRaises(ConfigParserException):
            Converter('fakename.txt', 'fakename2.txt')
