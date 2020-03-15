"""Utils for JSON support instead of doing raw write to file."""
import json


def read_json_file(path):
    """Returns dict from json file."""
    with open(path, 'r', encoding='utf-8') as f:
        json_dict = json.load(f)
    return json_dict


def add_shitpost_record(command, raw_msg):
    """Add shitpost record to json pseudo-db."""
    with open('shitpost.json', 'r+', encoding='utf-8') as f:
        json_dict = json.load(f)
        f.seek(0)
        json_dict.update(
            {command: raw_msg}
        )
        json.dump(json_dict, f, ensure_ascii=False, indent=4)


def delete_shitpost_record(command):
    """Remove shitpost record from json pseudo-db."""
    with open('shitpost.json', 'r+', encoding='utf-8') as f:
        json_dict = json.load(f)
        if command in json_dict:
            del json_dict[command]
        else:
            return False
    with open('shitpost.json', 'w+', encoding='utf-8') as f:
        json.dump(json_dict, f, ensure_ascii=False, indent=4)
        return True
