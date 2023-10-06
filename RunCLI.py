import os
import sys
import argparse
import traceback
from typing import TextIO, BinaryIO, Optional

import Version
from ItemRandomiser import ItemRandomiser

# TODO Refactor code to use filetypes as input variables, but for now rest of codebase does not support
class ArgumentParser(argparse.Namespace):
    input: str
    output: str
    mode: str
    race: Optional[str] = None
    racestring: Optional[bool] = False
    log: bool = False
    seed: Optional[str] = None
    seednumeric: Optional[int] = None
    cli: bool = False
    checks: Optional[str] = None
    attempts = 0
    instance = None

    _parser = argparse.ArgumentParser()
    _subparser_factory = _parser.add_subparsers()
    _subparser = _subparser_factory.add_parser('cli')
    _subparser.add_argument('-i', '--input', type=str, help='Input ROM file')
    _subparser.add_argument('-o', '--output', type=str, help='Path to save randomized ROM')
    _subparser.add_argument('-m', '--mode', type=str, help='YAML file containing randomization settings')
    _me_group = _subparser.add_mutually_exclusive_group()
    _me_group.add_argument('-r', '--race', nargs='?', help='Race mode string')
    _me_group.add_argument('-l', '--log', action='store_true', default=False, help='Should output spoiler log')
    _me_group.add_argument('-rs', '--racestring', action='store_true', default=False, help='Race mode string output')

    _subparser.add_argument('-s', '--seed', help='RNG seed for reproducible randomization')
    _subparser.add_argument('-sn', '--seednumeric', help='RNG seed for reproducible randomization, numeric form')

    _subparser.add_argument('-c', '--checks', help='Checks to output based on inputs')

    def __init__(self, args=None):
        self.__class__._parser.parse_args(args, self)
        self.cli = hasattr(self, 'input') and hasattr(self, 'output') and hasattr(self, 'mode')
        self.check_results = None
        self.instance = None

    def main(self):
        item_rando = ItemRandomiser(GUI=None)
        item_rando.DisplayMessage("CKIR V{}".format(Version.GetItemRandoVersion()), "Version", type="INFO")
    
        if self.race is None:
            settingsFile = self.mode
            item_rando.loadSettings(settingsFile)

            if self.seednumeric is not None:
                use_seed = int(self.seednumeric)
            else:
                use_seed = self.seed

            rom_md5 = None
        else:
            data = item_rando.LoadRaceModeSettings(raceString=self.race)
            use_seed = data[2]
            rom_md5 = data[3]
    
        flags = {"Spoiler" : self.log, "RaceMode": self.race is not None or self.racestring}

        item_rando.runRandomizer(in_file=self.input, out_file=self.output,
                                 seed=use_seed, run_flags=flags, requiredMD5=rom_md5, attempts=self.attempts)

        self.instance = item_rando

        #if self.checks is not None:
        #    self.check_results = item_rando.performChecks(self.checks.split(","))
#
        #    if __name__ == '__main__':
        #        print(self.check_results)

    def PerformChecks(self):
        if self.checks is not None and self.instance is not None:
            self.check_results = self.instance.performChecks(self.checks.split(","))

            if __name__ == '__main__':
                print(self.check_results)
        else:
            return None

def main():
    try:
        ArgumentParser().main()
        return 0
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
