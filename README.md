# Python VM Virtualizer

Hey ! i've make a simple stack-based virtual machine that translates and executes Python bytecode because i was  busy and just wanna have some fun. This project was originally created for a high school presentation to demonstrate how Python interprets code but i wanna share it here if anyone want to take a look

# disclaimer : the script was fully made by my own and NOT AI generated so if you see comments its just mine ( crazy i need to say that ) -_-

When you write Python code, CPython doesn't execute it directly. It first compiles your source code into bytecode, then interprets that bytecode. This project replicates a small part of that process:

1. Takes Python source code
2. Compiles it using CPython's `compile()`
3. Translates the bytecode into a custom virtual instruction set
4. Executes the translated bytecode on a custom stack-based VM

It's not a full Python interpreter , it supports a limited subset of operations (variables, constants, print, comparisons, simple arithmetic, conditionals). The goal is educational, to show the core concepts of bytecode interpretation.

## How to test it myself ? 

```bash
python vm.py
```

It will:
- Compile the test code
- Translate it to virtual bytecode
- Save it as `output.vmpy`
- Execute the virtual bytecode

### Using your own code

```python
from vm import VM

source = """
x = 42
print(x)
if x > 10:
    print("big")
else:
    print("small")
"""

vm = VM(source)
vm.virtualize()
vm.run("output.vmpy")
```

## How it works

### The bytecode pipelines

```
Python source → CPython compilation → Python bytecode → Translation → .vmpy file → VM execution
```

### The stack

The VM uses a LIFO stack for temporary values. For example, `var += 1` becomes:

```
LOAD_NAME var   → push current value of var
LOAD_CONST 1    → push 1
BINARY_OP +=    → pop two values, add them, push result
STORE_NAME var  → pop result and store in variables["var"]
```

[`handle_binary_op`](vm.py#L309) and [`handle_inplace_add`](vm.py#L339) methods in [`vm.py`](vm.py) for how these operations are implemented.

### The dispatcher

The execution loop follows the fetch-decode-execute pattern ( simple as that ):

```python
while ip < len(bytecode):
    opcode, arg = fetch_instruction()
    handler = handlers[opcode]
    handler(arg)
```

[`dispatcher`](vm.py#L437) method in [`vm.py`](vm.py) 

## Supported operations

- `LOAD_CONST`, `LOAD_NAME`, `STORE_NAME` - see [`handle_load_const`](vm.py#L364), [`handle_load_name`](vm.py#L369), [`handle_store_name`](vm.py#L352)
- `CALL` (function calls) - see [`handle_call`](vm.py#L410)
- `COMPARE_OP` (comparisons) - see [`handle_compare_op`](vm.py#L344)
- `BINARY_OP`, `INPLACE_ADD` (arithmetic) - see [`handle_binary_op`](vm.py#L309), [`handle_inplace_add`](vm.py#L339)
- `POP_JUMP_IF_FALSE`, `JUMP_FORWARD` (control flow) - see [`handle_pop_jump_if_false`](vm.py#L389), [`handle_jump_forward`](vm.py#L332)
- `RETURN_CONST`, `RETURN_VALUE` - see [`handle_return_const`](vm.py#L359), [`handle_return_value`](vm.py#L428)

All handlers are defined in the [`VM`](vm.py#L205) class in [`vm.py`](vm.py).

## File format (.vmpy)

I've wanted to make my own custom format based on python one ( yeah totally not the same thing )

```
magic(4) + bytecode_length(4) + bytecode + marshal(consts) + marshal(names)
```

- `magic`: just a custom magic number `PYVM`
- `bytecode_length`: Length of the virtual bytecode section
- `bytecode`: Encoded VM instructions
- `consts/names`: Serialized metadata using Python's marshal module

## Architecture

The VM state consists of:

- `stack`: Temporary values for operations
- `variables`: Dictionary storing variable names and values
- `ip`: Instruction pointer (program counter)
- `consts`: Constants from compiled code
- `names`: Variable/function names from compiled code

## Limitations

This is an educational project, not a production interpreter:

- Only supports a small subset of Python bytecode
- No loops, functions, classes, or imports
- No exception handling
- Not suitable for running untrusted code
- The `.vmpy` format uses `marshal` which is not designed for security

## Documentation

Just check the documentation in the `docs/` folder

## Requirements

- Python 3.11+ (tested on 3.12)
- Standard library only: `opcode`, `dis`, `struct`, `marshal`