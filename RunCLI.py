import os
import sys
import argparse
import traceback
from typing import TextIO, BinaryIO, Optional

from ItemRandomiser import ItemRandomiser

class ArgumentParser(argparse.Namespace):
    input: BinaryIO
    output: BinaryIO
    mode: TextIO
    race: Optional[str] = None
    log: bool = False
    seed: Optional[str] = None

    _parser = argparse.ArgumentParser()
    _subparser_factory = _parser.add_subparsers()
    _subparser = _subparser_factory.add_parser('cli')
    _subparser.add_argument('-i', '--input', type=argparse.FileType('rb'), help='Input ROM file')
    _subparser.add_argument('-o', '--output', type=argparse.FileType('wb'), help='Path to save randomized ROM')
    _subparser.add_argument('-m', '--mode', type=argparse.FileType(), help='YAML file containing randomization settings')
    _me_group = _subparser.add_mutually_exclusive_group()
    _me_group.add_argument('-r', '--race', nargs='?', help='Race mode string')
    _me_group.add_argument('-l', '--log', action='store_true', default=False, help='Should output spoiler log')
    _subparser.add_argument('-s', '--seed', help='RNG seed for reproducible randomization')

    def __init__(self, args=None):
        self.__class__._parser.parse_args(args, self)

    def main(self):
        item_rando = ItemRandomiser(GUI=None)
    
        if self.race is None:
            settingsFile = self.mode
            item_rando.loadSettings(settingsFile)
            use_seed = self.seed
            rom_md5 = None
        else:
            data = item_rando.LoadRaceModeSettings(raceString=race_mode)
            use_seed = data[2]
            rom_md5 = data[3]
    
    
        flags = {"Spoiler" : self.log, "RaceMode": self.race is not None}
        print(flags, self)
    
        item_rando.runRandomizer(in_file=self.input, out_file=self.output,
                                 seed=use_seed, run_flags=flags, requiredMD5=rom_md5)


def main():
    try:
        ArgumentParser().main()
        return 0
    except Exception as e:
        traceback.print_exception(e, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
