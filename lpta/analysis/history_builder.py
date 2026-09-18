import json
from pathlib import Path

from lpta.analysis.diff_engine import diff_ir
from lpta.analysis.metrics import count_metrics
from lpta.analysis.pass_knowledge import describe_pass
from lpta.capture.opt_cli_capture import OptCliCapture

OUTPUT_PATH = Path("output/history.json")

def build_history(source_path: str, opt_level: str = "O2") -> list[dict]:
    """
    source_path: path to source file.
    opt_level: optimizatoin level.
    returns: list of dict, one per pas.
    """

    capture_backend = OptCliCapture()
    events = capture_backend.capture(source_path, opt_level)

    history = []

    for event in events: 
        history.append({
            "pass_name": event.pass_name,
            "function": event.function_name,
            "metrics_before": count_metrics(event.ir_before),
            "metrics_after": count_metrics(event.ir_after),
            "diff":diff_ir(event.ir_before, event.ir_after),
            "description": describe_pass(event.pass_name),
        })

    return history

def save_history(history: list[dict], output_path: Path = OUTPUT_PATH) ->None:
    """
    history: list of pass dicts.
    output_path: where to save.
    returns:None, writes the json file
    """

    output_path.parent.mkdir(parents = True, exist_ok = True)
    with open(output_path, "w") as file:
        json.dump(history, file, indent = 2)