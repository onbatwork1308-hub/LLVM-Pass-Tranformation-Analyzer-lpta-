from dataclasses import dataclass

@dataclass

class PassEvent:
    """
    pass name: name of the LLVM pass (e.g. "mem2reg")
    
    function name: function the pass ran on 
    
    ir_before: IR before the pass ran
    
    ir_after: IR after the pass ran
    """

    pass_name: str
    function_name: str
    ir_before: str
    ir_after:str