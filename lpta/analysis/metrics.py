import llvmlite.binding  as llvm 

def count_metrics(ir_text: str) -> dict:
    """
    ir_text: LLVM IR as text.
    returns: dict of counts(instructions, basic_blocks, loads, stores, branches,
    calls, allocas)
    """

    counts = {"instructions" : 0, "basic_blocks" : 0, "loads" : 0, "stores" : 0,
               "branches" : 0, "calls" : 0, "allocas" : 0}

    if not ir_text.strip():
        return counts

    module = llvm.parse_assembly(ir_text) 
    for function in module.functions: 
        for block in function.blocks:
            counts["basic_blocks"] += 1 
            for instruction in block.instructions:  
                counts["instructions"] += 1
                opcode = instruction.opcode

                if opcode == "load":
                    counts["loads"] += 1
                elif opcode == "store":
                    counts["stores"] += 1
                elif opcode in ("br", "switch"):
                    counts["branches"] += 1
                elif opcode == "call":
                    counts["calls"] += 1
                elif opcode == "alloca":
                    counts["allocas"] += 1

    return counts


