# Bytecode pipeline

## Step 1: Python source code

Example:

```python
var = 10
print(var)

if var == 1:
    print("passed !")
else:
    print("failed !")
```

## Step 2: CPython compilation

CPython can compile the source code into a code object:

```python
code = compile(source, "demo.py", "exec")
```

The code object contains:

- `co_code`: bytecode bytes;
- `co_consts`: constants such as `10`, `1`, and strings;
- `co_names`: names such as `var` and `print`.

## Step 3: Disassembly

The project uses `dis.get_instructions()` to obtain readable instructions.

Example output can look like:

```text
LOAD_CONST      0   10
STORE_NAME      0   var
LOAD_NAME       1   print
PUSH_NULL
LOAD_NAME       0   var
CALL            1
POP_TOP
```

Exact opcode names and numbers can change between Python versions. That is why the VM normalizes some names, for example `POP_JUMP_FORWARD_IF_FALSE` and `POP_JUMP_BACKWARD_IF_FALSE` become `POP_JUMP_IF_FALSE`.

## Step 4: Translation

The translator maps CPython instruction names to this VM's instruction names and numeric opcode values.

Example ( not the same as i have in my vm.py ) :

| CPython instruction | VM instruction      | VM opcode  |
|---                  |---                  |---:        |
| `LOAD_CONST`        | `LOAD_CONST`        | `0x203`    |
| `STORE_NAME`        | `STORE_NAME`        | `0x206`    |
| `CALL`              | `CALL`              | `0x209`    |
| `POP_JUMP_IF_FALSE` | `POP_JUMP_IF_FALSE` | `0x20e`    |

The names stay readable for documentation, but the bytes written into `.vmpy` are custom.

## Step 5: Execution

During execution, the VM does:

```text
fetch  -> read next instruction
 decode -> identify opcode and argument
 execute -> call handler and update stack/variables/IP
```

This cycle is the software equivalent of the CPU idea often called fetch-decode-execute.
