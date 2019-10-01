import re
import sys


class ConfigParserException(Exception):
    pass


class Converter:
    old_config = {}
    new_config = {}
    failures = []

    def __init__(self, old: str, new: str):
        """
        Converter constructor
        :param old:  Old configuration file name
        :param new:  New configuration file name
        """
        self.old_config_fn = old
        self.new_config_fn = new
        self.load_configs()

    @property
    def old(self):
        return self.old_config

    @property
    def new(self):
        return self.new_config

    # noinspection PyTypeChecker
    # WHY: Intellij doesn't properly interpolate type in one liner.
    def load_configs(self) -> None:
        """
        Config loader
        """
        try:
            self.old_config = dict([line.rstrip('\n').split('=') for line in open(self.old_config_fn, encoding="utf8")])
            self.new_config = dict([line.rstrip('\n').split('=') for line in open(self.new_config_fn, encoding="utf8")])
        except:
            raise ConfigParserException('The configs were not able to be read. '
                                        'Please verify the files exist in this directory and the name is correct.')
        if not (self.old_config and self.new_config):
            raise ConfigParserException('The configs were not parsed properly. '
                                        'Ensure that they are valid configurations before continuing.')
        # WHY: repair value being interpolated as string
        self.old_config = {k: int(v) for k, v in self.old_config.items()}
        self.new_config = {k: int(v) for k, v in self.new_config.items()}

    def convert(self) -> list:
        """
        Converts old format config option to new format
        :return: failures
        """
        for k, v in self.old_config.items():
            partial_key = None
            # WHY: Scripts include their name in path. We intentionally exclude the leading '/' due to differences
            # such as FAIO.lua vs. /.FAIO/. We can still partial match if we exclude the leading '/'
            m = re.search('(?i)(.+?)\.lua\s', k)
            if m:
                try:
                    partial_key = [m.group(1), k.replace(m.group(1) + '.lua ', '')]
                    k = m.group(1) + "/" + k.replace(m.group(1) + '.lua ', '')
                except:
                    self.failures.append((k, v))
                    continue

            # WHY: Key without a number is now mode/toggle, or just nothing at all.
            # Strip the word key off, and we can search for it.
            m = re.search('(?i)(key(?:\s{{[a-z]+}}))$', k)
            if m:
                k = re.sub('(?i)\skey\s', '', k)
                k = re.sub('(?:\s?{{[a-z]+}})', '', k)
                k = re.sub('\d\.\s', '', k)
                if partial_key:
                    partial_key[1] = re.sub('(?i)key\s', '', partial_key[1])
                    partial_key[1] = re.sub('(?:\s?{{[a-z]+}})', '', partial_key[1])
                    partial_key[1] = re.sub('\d\.\s', '', partial_key[1])

            # WHY: key0 is the only key we care about, this will match up to "key" in the new config
            if "key0" in k:
                k = k.replace('key0', 'key')
                if partial_key:
                    partial_key[1] = partial_key[1].replace('key0', 'key')

            if "Key0" in k:
                k = k.replace('Key0', 'Key')
                if partial_key:
                    partial_key[1] = partial_key[1].replace('Key0', 'Key')

            # WHY: We don't want key1, key2, key3. These don't exist in the new config
            m = re.search('(?i)(key(?:\s{{[a-z\s_]+}})?)(\d)', k)
            if m:
                try:
                    if int(m.group(2)) != 0:
                        continue
                    else:
                        k = k.rstrip('0')
                        partial_key[1] = partial_key[1].rstrip('0')
                except:
                    continue

            # naming difference cases
            if "autodefend" in k.lower():
                k = k.replace('AutoDefend', 'Auto Defend')

            if "HiddenSpells" in k:
                k = k.replace('HiddenSpells', 'Hidden Spells Plus')

            if "VisibilityLines" in k:
                k = k.replace('VisibilityLines', 'Visibility Lines')

            converted = 0
            for k_ in self.new_config.keys():
                if k.lower() in k_.lower():
                    self.new_config[k_] = v
                    converted = 1
                elif partial_key and partial_key[0].lower() in k_.lower() and partial_key[1].lower() in k_.lower():
                    if "key" in k_.lower() and "key" not in partial_key[1].lower():
                        continue
                    self.new_config[k_] = v
                    converted = 1
            if converted == 0:
                self.failures.append((k, v))

        # write results to file
        with open('dota2-converted.txt', 'w') as f:
            [f.write('{0}={1}\n'.format(k, v)) for k, v in self.new_config.items()]

        return self.failures


converter = Converter('dota2reborn.txt', 'dota2.txt')
failures = converter.convert()
print("Failed to convert {} out of {}".format(len(failures), len(converter.new)))
with open('failures.txt', 'w', encoding="utf8") as f:
    [f.write('{0}={1}\n'.format(k, v)) for k, v in failures]
