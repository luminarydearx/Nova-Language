# Bytecode & Virtual Machine - Nova Language

Nova v2.0 mendukung kompilasi ke **Bytecode** dan eksekusi di **Virtual Machine (VM)**.

## Apa itu Bytecode?

Bytecode adalah representasi kode yang lebih rendah (low-level) dari AST. Ini memungkinkan eksekusi yang lebih cepat.

## Alur Eksekusi

```
Kode Nova (.nova)
    ↓
Lexer (Tokenisasi)
    ↓
Parser (AST Generation)
    ↓
Compiler (Bytecode Generation)  ← Baru di v2.0!
    ↓
VM (Stack-based Execution)      ← Baru di v2.0!
    ↓
Output
```

## Contoh Kompilasi

### Kode Nova

```nova
var x = 10
var y = 20
print(x + y)
```

### Bytecode yang Dihasilkan

```
LOAD_CONST 0    # Push 10 ke stack
STORE_VAR x     # Simpan ke variabel x
LOAD_CONST 1    # Push 20 ke stack
STORE_VAR y     # Simpan ke variabel y
LOAD_VAR x       # Push nilai x
LOAD_VAR y       # Push nilai y
ADD              # Pop 2, jumlahkan, push hasil
PRINT            # Pop & cetak
```

## Cara Kerja VM (Stack-based)

VM menggunakan **Operand Stack** untuk memproses instruksi:

```
Stack: []
Eksekusi: LOAD_CONST 10
Stack: [10]

Eksekusi: LOAD_CONST 20
Stack: [10, 20]

Eksekusi: ADD
Stack: [30]  ← 10 + 20 = 30

Eksekusi: PRINT
Output: 30
Stack: []
```

## Opcode yang Didukung

| Opcode | Deskripsi | Stack Effect |
|--------|-------------|----------------|
| `LOAD_CONST` | Push konstanta | `[] → [const]` |
| `LOAD_VAR` | Push nilai variabel | `[] → [value]` |
| `STORE_VAR` | Simpan ke variabel | `[value] → []` |
| `ADD` | Penjumlahan | `[a, b] → [a+b]` |
| `SUB` | Pengurangan | `[a, b] → [a-b]` |
| `MUL` | Perkalian | `[a, b] → [a*b]` |
| `DIV` | Pembagian | `[a, b] → [a/b]` |
| `PRINT` | Cetak nilai | `[value] → []` |
| `JUMP` | Lompat ke alamat | `[] → []` |
| `JUMP_IF_FALSE` | Lompat jika false | `[cond] → []` |

## Menggunakan Compiler & VM

```python
from nova.bytecode.compiler import Compiler
from nova.bytecode.vm import VM

# Kompilasi
compiler = Compiler()
bytecode = compiler.compile(ast)

# Eksekusi
vm = VM()
output = vm.run(bytecode.instructions, bytecode.constants)
```

## Fitur yang Digunakan

- ✅ Bytecode Compiler
- ✅ Stack-based Virtual Machine
- ✅ Instruction Set (ADD, SUB, MUL, dll.)
- ✅ Constant Pool
