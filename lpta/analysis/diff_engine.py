import difflib

def diff_ir(ir_before: str, ir_after: str) -> list[str]:
    """
    ir_before, ir_after: IR text snapshots
    returns: list of unified-diff lines
    """

    return list(difflib.unified_diff(ir_before.splitlines(), ir_after.splitlines(), lineterm=""))