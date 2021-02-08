import json


def dump_jsonl(data, output_path, append=True):
    """
    Write list of objects to a JSON lines file.
    """
    mode = "a+" if append else "w"
    with open(output_path, mode, encoding="utf-8") as f:
        for line in data:
            json_record = json.dumps(line, ensure_ascii=False)
            f.write(json_record + "\n")


def load_jsonl(input_path) -> list:
    """
    Read list of objects from a JSON lines file.
    """
    data = []
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line.rstrip("\n|\r")))
    return data


def get_last_tweet_id(path: str) -> int:
    with open(path, "r") as f:
        return json.load(f).get("id")


def update_last_tweet_id(last_tweet_id: int, path: str) -> None:
    with open(path, "w") as f:
        json.dump({"id": last_tweet_id}, f)
