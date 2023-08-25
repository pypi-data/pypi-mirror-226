#!/usr/bin/python3

"""
This script is used for updating `values.yaml` file `image` tag inside CI/CD pipeline
"""

from ruamel.yaml import YAML, YAMLError
import argparse
from sys import exit
from common.extended_dict import ExtendedDict
import re

parser = argparse.ArgumentParser(description='helm "values.yaml" tag updater')

parser.add_argument('-t', '--tag', help="NOTE: If 'prod' mode is active provided tag should match regular expression. default: v[0-9].[0-9].[0-9] (e.g v0.0.1, v2.5.9 and so on)", required=True)
parser.add_argument('-f', '--filepath', help="Path for 'values.yaml' file", required=True)
parser.add_argument('-p', '--prod', help="(Optional) Enables prod mode, e.g enable regular expression matching for tag", action=argparse.BooleanOptionalAction)
parser.add_argument('-e', '--expression', help="(Optional) Your production regular expression", required=False, default="v[0-9].[0-9].[0-9]")
parser.add_argument('-y', '--yaml_path', help="(Optional) Path to the tag in yaml file, default for helm chart is `image.tag`", required=False, default="image.tag")

# creates a new YAML class object
yaml = YAML()

# read file content
def read_file_and_replace_tag(filepath, tag, yaml_path) -> None:
    manifest = None

    # write to file updated yaml dictionary
    def write_to_file():
        with open(filepath, mode="w") as file:
            yaml.dump(manifest, file)

    # read file content
    with open(filepath) as file:
        try:
            # load file content and parse it as python dictionary
            manifest = yaml.load(file)
            
            # function for updating tag
            ExtendedDict().update_dict(manifest, path=yaml_path, value=tag)

            if manifest is not None:
                write_to_file()

        except YAMLError:
            print("Some error accuped while reading yaml file")
            exit(1)

def main() -> None:
    args = parser.parse_args()

    # If prod mode is active tag should match user regular expression. default: vX.X.X, (e.g v2.0.4 and so on)
    prod_mode_re = re.search(args.expression, args.tag)

    # check if 'prod' mode is enabled and tag matches 'prod_mode_re' regular expression
    if args.prod and not(prod_mode_re):
        print("If production mode is enabled tag should match regular expression {}".format(args.expression))
        exit(1)

    read_file_and_replace_tag(args.filepath, args.tag, args.yaml_path)

if __name__ == "__main__":
    main()
