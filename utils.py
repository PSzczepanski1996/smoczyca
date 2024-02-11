"""Various utils made for KenSoft smoczyca bot."""
import json
import os
import subprocess
from consts import db_json_name


def read_json_file(path):
    """Returns dict from json file."""
    with open(path, 'r', encoding='utf-8') as f:
        json_dict = json.load(f)
    return json_dict


def init_file_existence(path):
    """Check file existence, if not, create it."""
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=4)


def add_message_record(command, raw_msg):
    """Add message record to json pseudo-db."""
    with open(db_json_name, 'r+', encoding='utf-8') as f:
        json_dict = json.load(f)
        f.seek(0)
        json_dict.update(
            {command: raw_msg}
        )
        json.dump(json_dict, f, ensure_ascii=False, indent=4)


def delete_message_record(command):
    """Remove message record from json pseudo-db."""
    with open(db_json_name, 'r+', encoding='utf-8') as f:
        json_dict = json.load(f)
        if command in json_dict:
            del json_dict[command]
        else:
            return False
    with open(db_json_name, 'w+', encoding='utf-8') as f:
        json.dump(json_dict, f, ensure_ascii=False, indent=4)
        return True


def get_commit_version():
    """Return SHORT commit number."""
    return subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'],
    ).decode('ascii').replace('"', '')[:7]