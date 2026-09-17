# How to add a new LLVM pass description

Pass descriptions live in lpta/data/pass_descriptions.yaml, not in Python
code. To add support for explaining a new pass:

1. Open lpta/data/pass_descriptions.yaml
2. Add a new entry using the same structure as the existing ones
   (pass name, category, description)
3. Save the file

No code changes are needed. This is intentional: it should be possible to
extend LPTA's pass coverage by editing data, not by writing new code.
