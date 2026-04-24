import opcode, dis , struct, marshal

VERSION = 1.4
TEST    = """
var = 10
print(var)

if var == 1:
    print("passed ! ")
else : 
    print('failed ! ')

var += 1
print(var)

"""


###################################################
"""
  0           0 RESUME                   0

  2           2 LOAD_CONST               0 (10)
              4 STORE_NAME               0 (var)

  3           6 PUSH_NULL
              8 LOAD_NAME                1 (print)
             10 LOAD_NAME                0 (var)
             12 CALL                     1
             20 POP_TOP

  4          22 LOAD_NAME                0 (var)
             24 LOAD_CONST               1 (1)
             26 COMPARE_OP              40 (==)
             30 POP_JUMP_IF_FALSE        9 (to 50)

  5          32 PUSH_NULL
             34 LOAD_NAME                1 (print)
             36 LOAD_CONST               2 ('UD')
             38 CALL                     1
             46 POP_TOP
             48 RETURN_CONST             4 (None)

  7     >>   50 PUSH_NULL
             52 LOAD_NAME                1 (print)
             54 LOAD_CONST               3 ('gg')
             56 CALL                     1
             64 POP_TOP
             66 RETURN_CONST             4 (None)
"""
###################################################


OP_MAP = {
    "CACHE"             : 0x0,
    "POP_TOP"           : 0x1,
    "PUSH_NULL"         : 0x2,
    "INTERPRETER_EXIT"  : 0x3,
    "END_FOR"           : 0x4,
    "END_SEND"          : 0x5,
    "NOP"               : 0x9,
    "UNARY_NEGATIVE"    : 0xB,
    "UNARY_NOT"         : 0xC,
    "UNARY_INVERT"      : 0xF,
    "RESERVED"          : 0x11,
    "BINARY_SUBSCR"     : 0x19,
    "BINARY_SLICE"      : 0x1A,
    "STORE_SLICE"       : 0x1B,
    "GET_LEN"           : 0x1E,
    "MATCH_MAPPING"     : 0x1F,
    "MATCH_SEQUENCE"    : 0x20,
    "MATCH_KEYS"        : 0x21,
    "PUSH_EXC_INFO"     : 0x23,
    "CHECK_EXC_MATCH"   : 0x24,
    "CHECK_EG_MATCH"    : 0x25,
    "WITH_EXCEPT_START" : 0x31,
    "GET_AITER"         : 0x32,
    "GET_ANEXT"         : 0x33,
    "BEFORE_ASYNC_WITH" : 0x34,
    "BEFORE_WITH"       : 0x35,
    "END_ASYNC_FOR"     : 0x36,
    "CLEANUP_THROW"     : 0x37,
    "STORE_SUBSCR"      : 0x3C,
    "DELETE_SUBSCR"     : 0x3D,
    "GET_ITER"          : 0x44,
    "GET_YIELD_FROM_ITER": 0x45,
    "LOAD_BUILD_CLASS"    : 0x47,
    "LOAD_ASSERTION_ERROR": 0x4A,
    "RETURN_GENERATOR"    : 0x4B,
    "RETURN_VALUE"        : 0x53,
    "SETUP_ANNOTATIONS"   : 0x55,
    "LOAD_LOCALS"         : 0x57,
    "POP_EXCEPT"          : 0x59,
    "STORE_NAME"          : 0x5A,
    "DELETE_NAME"         : 0x5B,
    "UNPACK_SEQUENCE"     : 0x5C,
    "FOR_ITER"            : 0x5D,
    "UNPACK_EX"           : 0x5E,
    "STORE_ATTR"          : 0x5F,
    "DELETE_ATTR"         : 0x60,
    "STORE_GLOBAL"        : 0x61,
    "DELETE_GLOBAL"       : 0x62,
    "SWAP"                : 0x63,
    "LOAD_CONST"          : 0x64,
    "LOAD_NAME"           : 0x65,
    "BUILD_TUPLE"         : 0x66,
    "BUILD_LIST"          : 0x67,
    "BUILD_SET"           : 0x68,
    "BUILD_MAP"           : 0x69,
    "LOAD_ATTR"           : 0x6A,
    "COMPARE_OP"          : 0x6B,
    "IMPORT_NAME"         : 0x6C,
    "IMPORT_FROM"         : 0x6D,
    "JUMP_FORWARD"        : 0x6E,
    "POP_JUMP_IF_FALSE"   : 0x72,
    "POP_JUMP_IF_TRUE"    : 0x73,
    "LOAD_GLOBAL"         : 0x74,
    "IS_OP"               : 0x75,
    "CONTAINS_OP"         : 0x76,
    "RERAISE"             : 0x77,
    "COPY"                : 0x78,
    "RETURN_CONST"        : 0x79,
    "BINARY_OP"           : 0x7A,
    "INPLACE_ADD"         : 0x7A,
    "SEND"                : 0x7B,
    "LOAD_FAST"           : 0x7C,
    "STORE_FAST"          : 0x7D,
    "DELETE_FAST"         : 0x7E,
    "LOAD_FAST_CHECK"     : 0x7F,
    "POP_JUMP_IF_NOT_NONE": 0x80,
    "POP_JUMP_IF_NONE"    : 0x81,
    "RAISE_VARARGS"       : 0x82,
    "GET_AWAITABLE"       : 0x83,
    "MAKE_FUNCTION"       : 0x84,
    "BUILD_SLICE"         : 0x85,
    "JUMP_BACKWARD_NO_INTERRUPT": 0x86,
    "MAKE_CELL"         : 0x87,
    "LOAD_CLOSURE"      : 0x88,
    "LOAD_DEREF"        : 0x89,
    "STORE_DEREF"       : 0x8A,
    "DELETE_DEREF"      : 0x8B,
    "JUMP_BACKWARD"     : 0x8C,
    "LOAD_SUPER_ATTR"   : 0x8D,
    "CALL_FUNCTION_EX"  : 0x8E,
    "LOAD_FAST_AND_CLEAR": 0x8F,
    "EXTENDED_ARG"      : 0x90,
    "LIST_APPEND"       : 0x91,
    "SET_ADD"           : 0x92,
    "MAP_ADD"           : 0x93,
    "COPY_FREE_VARS"    : 0x95,
    "YIELD_VALUE"       : 0x96,
    "RESUME"            : 0x97,
    "MATCH_CLASS"       : 0x98,
    "FORMAT_VALUE"      : 0x9B,
    "BUILD_CONST_KEY_MAP": 0x9C,
    "BUILD_STRING"      : 0x9D,
    "LIST_EXTEND"       : 0xA2,
    "SET_UPDATE"        : 0xA3,
    "DICT_MERGE"        : 0xA4,
    "DICT_UPDATE"       : 0xA5,
    "CALL"              : 0xAB,
    "KW_NAMES"          : 0xAC,
    "CALL_INTRINSIC_1"  : 0xAD,
    "CALL_INTRINSIC_2"  : 0xAE,
    "LOAD_FROM_DICT_OR_GLOBALS"     : 0xAF,
    "LOAD_FROM_DICT_OR_DEREF"       : 0xB0,
    "INSTRUMENTED_LOAD_SUPER_ATTR"  : 0xED,
    "INSTRUMENTED_POP_JUMP_IF_NONE" : 0xEE,
    "INSTRUMENTED_POP_JUMP_IF_NOT_NONE": 0xEF,
    "INSTRUMENTED_RESUME": 0xF0,
    "INSTRUMENTED_CALL"  : 0xF1,
    "INSTRUMENTED_RETURN_VALUE": 0xF2,
    "INSTRUMENTED_YIELD_VALUE" : 0xF3,
    "INSTRUMENTED_CALL_FUNCTION_EX": 0xF4,
    "INSTRUMENTED_JUMP_FORWARD" : 0xF5,
    "INSTRUMENTED_JUMP_BACKWARD": 0xF6,
    "INSTRUMENTED_RETURN_CONST" : 0xF7,
    "INSTRUMENTED_FOR_ITER"     : 0xF8,
    "INSTRUMENTED_POP_JUMP_IF_FALSE": 0xF9,
    "INSTRUMENTED_POP_JUMP_IF_TRUE" : 0xFA,
    "INSTRUMENTED_END_FOR"  : 0xFB,
    "INSTRUMENTED_END_SEND" : 0xFC,
    "INSTRUMENTED_INSTRUCTION": 0xFD,
    "INSTRUMENTED_LINE": 0xFE,
    "SETUP_FINALLY": 0x100,
    "SETUP_CLEANUP": 0x101,
    "SETUP_WITH": 0x102,
    "POP_BLOCK" : 0x103,
    "JUMP"      : 0x104,
    "JUMP_NO_INTERRUPT": 0x105,
    "LOAD_METHOD"      : 0x106,
    "LOAD_SUPER_METHOD": 0x107,
    "LOAD_ZERO_SUPER_METHOD": 0x108,
    "LOAD_ZERO_SUPER_ATTR"  : 0x109,
    "STORE_FAST_MAYBE_NULL" : 0x10A,
    "CALL_FUNCTION"  :  0x1A1,
}

# print("OP_MAP = { ")        <-- si ta la flemme de faire la map manuellement
# for name, code in opcode.opmap.items():
#    print(f"    {name}", " : ", str(code) + ",")
# print("}")


class VM( ):
    def __init__(self, sourcecode, name: bytes = b'PYVM'):
        self.name = name 
        
        self.stack    = []
        self.ip       = 0
        self.to_debug = True
                
        self.code_obj = compile(sourcecode, "<string>", "exec")
        self.consts   = self.code_obj.co_consts
        self.names    = self.code_obj.co_names
        self.variables= {}

        self.escape_byte =  0xFF
        self.bytecode    = self.translate(self.code_obj.co_code)

        self.handlers = {
            # you can add here other opcodes if you want to support more 
           OP_MAP["LOAD_CONST"]       : self.handle_load_const,
           OP_MAP["LOAD_NAME"]        : self.handle_load_name,
           OP_MAP["LOAD_FAST"]        : self.handle_load_fast,
           OP_MAP["CALL"]             : self.handle_call,
           OP_MAP["CALL_FUNCTION"]    : self.handle_call,
           OP_MAP["CALL_FUNCTION_EX"] : self.handle_call_function_ex,
           OP_MAP["POP_TOP"]          : self.handle_pop_top,
           OP_MAP["RETURN_VALUE"]     : self.handle_return_value,
           OP_MAP["RESUME"]           : self.handle_resume,
           OP_MAP["PUSH_NULL"]        : self.handle_push_null,
           OP_MAP["CACHE"]            : self.handle_resume,
           OP_MAP["RETURN_CONST"]     : self.handle_return_const,
           OP_MAP["STORE_NAME"]       : self.handle_store_name,
           OP_MAP["COMPARE_OP"]       : self.handle_compare_op,
           OP_MAP["POP_JUMP_IF_FALSE"]: self.handle_pop_jump_if_false,
           OP_MAP["BINARY_OP"]        : self.handle_binary_op,
           OP_MAP["JUMP_FORWARD"]    : self.handle_jump_forward,
           OP_MAP["INPLACE_ADD"]    : self.handle_inplace_add
        }

    def dbg(self, msg : str = "----") -> str: 
        if self.to_debug: print(f"[DBG] : {msg}\n    IP = {self.ip} STACK = {self.stack}")

    def translate(self, codebase) -> bytearray:
        virtual_CODE  = bytearray()
        self.addr_map = {}

        for _ in range(0, len(codebase), 2):
            op_code = codebase[_]

            self.addr_map[_] = len(virtual_CODE)
            
            if not op_code == self.escape_byte : 
                arg = codebase[_+1] 
            else:
                oplow   = codebase[_ + 1]
                ophight = codebase[_ + 2]
                op_code = oplow + ophight
                arg = codebase[_+3] 


            op_name = opcode.opname[op_code]

            if op_name in OP_MAP: 

                virtualized_opcode = OP_MAP[op_name]

                if virtualized_opcode <= 0xFE:
                    virtual_CODE.append(virtualized_opcode)
                    virtual_CODE.append(arg)
                else:
                    virtual_CODE.append(self.escape_byte)
                    virtual_CODE.append(virtualized_opcode & 0xFF)
                    virtual_CODE.append((virtualized_opcode >> 8) & 0xFF)
                    virtual_CODE.append(arg)

                print(f"[VM] {op_name} ({op_code}) -> {hex(virtualized_opcode)}")
            
            else:print(f'[VM] ( 3.12 ) ERROR ON -> {op_name} | {op_code}')

        print(virtual_CODE)

        return virtual_CODE


    def virtualize(self) -> None:

        with open('output.vmpy', "wb") as f :

            CODE_LENGHT   = struct.pack('<I', len(self.bytecode))
            BYTECODE      = self.bytecode

            f.write(b"PYVM")
            f.write(CODE_LENGHT)
            f.write(BYTECODE)

            marshal.dump(self.consts, f)
            marshal.dump(self.names, f)

        print('[VM] SAVED ')


    def handle_exit(self):
        self.dbg("[DBG] : exit call")
        self.ip = len(self.bytecode) + 1

    def handle_binary_op(self, arg):
        right = self.stack.pop()
        left  = self.stack.pop()
        self.stack.append(left + right)


    def handle_call_function(self, arg):
        self.dbg()
        arguments = []
        for _ in range(arg):
            arguments.append(self.stack.pop())
        #LIFO
        arguments.reverse()

        func = self.stack.pop()
        #NULL
        self.stack.pop() 
        self.dbg(f"EXECUTION : {func}({arguments})")

        result = func(*arguments)

        self.stack.append(result)

    def handle_jump_forward(self, arg):
        # JUMP_FORWARD lui est relatif dans le bytecode Python
        # on calcule dabord l'adresse Python cible puis on convertit
        python_current = [k for k, v in self.addr_map.items() if v == self.ip][0]
        python_target  = python_current + (arg * 2)
        self.ip        = self.addr_map[python_target]

    def handle_inplace_add(self, arg):
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(left + right)

    def handle_compare_op(self, arg):
        self.dbg()
        var1, var2 = self.stack[-2:] 
        del self.stack[-2:]
        if var1 == var2:
            self.stack.append(True)
        else : self.stack.append(False)

    def handle_store_name(self, arg):
        self.dbg()
        val = self.stack.pop()
        var = self.names[arg]
        self.variables[var] = val
        self.dbg(f"STORE NAME : {var} -> {val}")

    def handle_return_const(self, arg):
        val = self.consts[arg]
        self.dbg(f"END with : {val}")
        self.handle_exit()
        
    def handle_load_const(self, arg):
        val = self.consts[arg]
        self.dbg(f"LOAD CONST '{val}'")
        self.stack.append(val)

    def handle_load_name(self, arg):
        name = self.names[arg]
        if name in self.variables:
            self.dbg(f"found -> {name} in self.variables")
            val = self.variables[name]
        elif name in globals():
            val = globals()[name]
        elif name in __builtins__.__dict__:
            val = __builtins__.__dict__[name]
        else:
            self.dbg(f'ERROR ON LOADING {name}')

        self.dbg(f"LOAD_NAME '{name}'")
        self.stack.append(val)

    def handle_load_fast(self, arg):
        val = self.consts[arg]
        self.dbg(f"PUSH CONST '{val}'")
        self.stack.append(val)

    def handle_pop_jump_if_false(self, arg):
        val = self.stack.pop()
        if not val:
            self.ip = self.addr_map[arg]   # arg*2 = adresse Python, addr_map donne l'adresse virtuelle

    def handle_call_function_ex(self, arg):
        self.dbg()
        params = []
        for i in range(arg):
            params.append(self.stack.pop())     # POP ALL ARGS 
        params.reverse()
        
        func = self.stack.pop()          # POP ( plop )
        if self.stack and self.stack[-1] is None:
            params.append(self.stack.pop())  # POP SECURITY NULL

        result = func(*params)
        self.dbg(f"HANDLE CALL {func}")
        self.stack.append(result)

    def handle_call(self, arg):
        self.dbg()
        arguments = []
        for _ in range(arg):
            arguments.append(self.stack.pop())
        #LIFO
        arguments.reverse()

        func = self.stack.pop() 
        #NULL
        if self.stack and self.stack[-1] is None:
            self.stack.pop()
        self.dbg(f"EXECUTION : {func}({arguments})")

        result = func(*arguments)

        self.stack.append(result)

    def handle_return_value(self, arg):
        val = self.stack.pop()
        self.dbg(f"RETURN VALUE '{val}'")
        # Return value si deja sur la stack

    def handle_push_null(self, arg)  : self.stack.append(None)
    def handle_pop_top(self, arg)    :  self.stack.pop()
    def handle_resume(self, arg): pass 

    def dispatcher(self, vm_context : bytearray):

        while self.ip < len(vm_context):

            virtualized_opcode = vm_context[self.ip]

            if virtualized_opcode == self.escape_byte:
                virtualized_opcode = vm_context[self.ip+1] | (vm_context[self.ip+2] << 8)
                argument           = vm_context[self.ip+3]
                self.ip  += 4
            else:
                argument  = vm_context[self.ip+1]
                self.ip  += 2

            if virtualized_opcode in self.handlers:
                try: self.handlers[virtualized_opcode](argument)
                except NameError as e:
                    self.dbg(f'[VM] ERROR during execution of {virtualized_opcode} with {e}')
            
            else: self.dbg(f'[VM] ERROR with : {virtualized_opcode} ARG= {argument}')


    def run(self, file) -> None :
        print(f" -- [ VERSION ] V{VERSION}")
        print(f" -- [   UwU   ] -- ")

        with open(file, "rb") as f:
            
            if f.read(4) != b'PYVM': return '[VM] Error : Bad Header'
            
            CODE_LENGHT = struct.unpack('<I', f.read(4))[0]
            CODE = f.read(CODE_LENGHT)
        
            self.consts = marshal.load(f)
            self.names  = marshal.load(f)
            vm_bytecode = CODE

        self.dispatcher(vm_bytecode)

if __name__ == "__main__":
    dis.dis(TEST)

    pyvm = VM(TEST)
    pyvm.virtualize()
    pyvm.run("output.vmpy")