import os

import yaml


ROOT_DIR = os.getcwd()
YAML_PATH = "instance/config.yaml"
ABS_YAML_PATH = os.path.join(ROOT_DIR, YAML_PATH)

config = dict()
with open(ABS_YAML_PATH) as f:
    config = yaml.safe_load(f)


def init():
    ...
