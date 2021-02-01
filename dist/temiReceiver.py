#!/usr/bin/env python3

import sys
import os
import yaml

# Directory where all files created and managed stay. Nothing is affected outside this path
working_dir = os.path.expanduser("~/temi")


def get_packs():
    pack_names = [f.name for f in os.scandir(f"{working_dir}/packs/") if f.is_dir()]
    return pack_names


def get_pack_path(pack_name):
    return f"{working_dir}/packs/{pack_name}"


def create_pack(pack_name, repo):
    pack_path = get_pack_path(pack_name)

    # insures the pack directory is properly created
    try:
        os.makedirs(pack_path)
    except FileExistsError:
        print(f"Pack {pack_name} already exists")
        return
    except Exception:
        print(f"Unable to create file {pack_path}")
        return

    # clones remote repo
    os.system(f"git clone {repo} {pack_path}")

    # runs init and update tasks
    proc_config = get_proc_config(pack_name)
    commands = []
    if "init" in proc_config:
        commands = proc_config["init"]
    if "update" in proc_config:
        commands += proc_config["update"]

    if len(commands) > 0:
        print("running init and update tasks")
        for command in commands:
            print(f"running {command}")
            os.system(f"cd {pack_path} && {command}")


def update_pack(pack_name):
    pack_path = get_pack_path(pack_name)
    os.system(f"git -C {pack_path} fetch origin master")
    os.system(f"git -C {pack_path} reset --hard origin/master")
    proc_config = get_proc_config(pack_name)
    if "update" in proc_config:
        print("running update tasks")
        for command in proc_config["update"]:
            print(f"running {command}")
            os.system(f"cd {pack_path} && {command}")


def get_proc_config(pack_name):  # TODO: Check for import key and merge configs before returning
    pack_path = get_pack_path(pack_name)
    with open(f"{pack_path}/Procfile.yml", "r") as f:
        return yaml.load(f, Loader=yaml.BaseLoader)


def start_pack(pack_name):
    pack_path = get_pack_path(pack_name)
    proc_config = get_proc_config(pack_name)

    def exec_command(command):
        if command[:1] == "(":  # Handles for when there is a background task described
            proc_name = command[1:command.find(")")]
            stripped_command = command[len(proc_name)+2:]
            command = f"nohup bash -c \"exec -a temi:pack:{pack_name}:{proc_name} {stripped_command}\" > log:{proc_name}.out &"
        os.system(f"cd {pack_path} && {command}")

    if "startup" in proc_config:
        print("running startup tasks")
        os.system(f"cd {pack_path}")
        for command in proc_config["startup"]:
            print(f"running {command}")
            exec_command(command)
        os.system("cd ~/")


def stop_pack(pack_name):
    os.system(f"pkill -f temi:pack:{pack_name}")


def delete_pack(pack_name):
    pack_path = get_pack_path(pack_name)
    os.system(f"rm -rf {pack_path}")


# TODO: Find a more sophisticated way of processing user inputs that auto generates help commands
while True:
    args = input(">> ").split(" ")
    command = args[0]

    if command == "create":  # working
        pack_name = args[1]
        repo = args[2]
        print(f"Cloning {repo} as {pack_name}...")
        create_pack(pack_name, repo)
        print(f"Pack {pack_name} successfully created")
        print(f"Use \"start {pack_name}\" to start your new pack")

    elif command == "start":  # working
        pack_name = args[1]
        print(f"Starting {pack_name}")
        start_pack(pack_name)

    elif command == "stop":  # working
        pack_name = args[1]
        print(f"Stopping pack {pack_name}")
        stop_pack(pack_name)

    elif command == "delete":  # working
        pack_name = args[1]
        print(f"Deleting {pack_name}")
        delete_pack(pack_name)

    elif command == "update":  # working
        pack_name = args[1]
        print(f"Stopping {pack_name}")
        stop_pack(pack_name)
        print(f"Pulling latest changes for {pack_name}")
        update_pack(pack_name)
        print(f"Starting {pack_name}")
        start_pack(pack_name)

    elif command == "command":  # not working
        pack_name = args[1]
        commands = args[2]
        pack_args = args[3:]

    elif command == "logs":  # not working
        pack_name = args[1]
        pack_path = get_pack_path(pack_name)
        print(f"tailing logs for {pack_name}, use ctrl+c to exit")
        os.system(f"tail -f {pack_path}/nohup.out")

    elif command == "list":  # working
        packs = ", ".join(get_packs())
        print(f"List of packs installed: {packs}")

    elif command == "shell":  # working
        sys.exit(244)

    elif command == "exit":  # working
        sys.exit(0)

    else:
        print("unrecognised command")
