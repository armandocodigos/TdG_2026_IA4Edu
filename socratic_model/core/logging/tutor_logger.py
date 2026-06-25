import json

from pathlib import Path

from datetime import datetime


LOG_PATH = Path(
    "logs/tutor_logs.jsonl"
)


def log_tutor(
    data: dict
):

    LOG_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    payload = {

        "timestamp":
        datetime.now().isoformat(),

        **data
    }

    with open(

        LOG_PATH,

        "a",

        encoding="utf-8"

    ) as f:

        f.write(

            json.dumps(
                payload,
                ensure_ascii=False
            ) + "\n"
        )