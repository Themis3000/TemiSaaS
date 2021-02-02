#!/usr/bin/env python3

from temiReceiver import start_pack, working_dir, get_packs
import yaml


for pack in get_packs():
    with open(f"{working_dir}/packs/{pack}.yml", "r") as f:
        config = yaml.load(f)
        if config["autostart"]:
            start_pack(pack)
