# Module System - Nova Language

Nova mendukung **Module System** untuk membagi kode ke dalam file yang berbeda.

## Kode

### File: `math_utils.nova`

```nova
// math_utils.nova
// Module untuk operasi matematika

func add(a, b) {
    return a + b
}

func multiply(a, b) {
    return a * b
}
```

### File: `main.nova`

```nova
// main.nova
// Import module lain

import "math_utils.nova"

print(add(10, 20))     // 30
print(multiply(5, 4))   // 20
```

## Penjelasan

### Keyword `import`

```nova
import "nama_file.nova"
```

- Memuat file `.nova` lain dan menjadikannya bagian dari program.
- Variabel dan fungsi yang dideklarasikan di file module bisa diakses di file utama.
- Saat ini menggunakan **shared scope** dengan interpreter utama.

### Cara Kerja

1. `import "math_utils.nova"` diproses oleh Module System
2. File dibaca dari direktori yang sama dengan file pemanggil
3. Lexer → Parser → Interpreter menjalankan kode module
4. Fungsi `add()` dan `multiply()` terdaftar di Symbol Table
5. File utama bisa memanggil fungsi tersebut

## Struktur Folder

```
project/
├── main.nova           # File utama
└── math_utils.nova     # Module
```

## Cara Menjalankan

```bash
python main.py main.nova
```

## Output

```
30
20
```

## Fitur yang Digunakan

- ✅ Module System
- ✅ Import Statement
- ✅ Function Declaration
- ✅ Return Statement
