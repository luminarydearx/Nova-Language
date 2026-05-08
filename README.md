# Nova Language v2.0

![Nova](https://img.shields.io/badge/Nova-v2.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Nova** adalah bahasa pemrograman modern yang dirancang untuk menjadi **profesional, terstruktur, dan mudah digunakan**. Versi 2.0 adalah *rewrite* total dari versi sebelumnya (0.5.7 Java) ke Python dengan arsitektur yang lebih bersih.

## Fitur Utama v2.0

### 1. **Symbol Table & Scope Stack**
Manajemen variabel yang rapi dengan dukungan *nested scope* (global, fungsi, blok).

### 2. **Abstract Syntax Tree (AST)**
Representasi kode sebagai pohon hierarki yang memudahkan optimasi dan analisis.

### 3. **Visitor Pattern**
Pemisahan logika eksekusi dari struktur data AST menggunakan pola desain *Visitor*.

### 4. **Lexer & Parser yang Kokoh**
*Tokenizer* dan *parser rekursif turun* (recursive descent) untuk analisis sintaks yang akurat.

### 5. **Type Inference**
Penentuan tipe data otomatis (`var x = 10` → int, `var y = "hello"` → string).

### 6. **Constant Folding**
Optimasi *compile-time*: `var x = 2 + 3` langsung diubah menjadi `var x = 5`.

### 7. **Native Function Bridge**
Bahasa Nova bisa memanggil fungsi Python langsung (misal: `sqrt()`, `clock()`).

### 8. **Exception Handling**
Dukungan `try-catch-finally` untuk penanganan error yang *robust*.

### 9. **Bytecode Compiler & Virtual Machine (VM)**
Kompilasi AST menjadi *bytecode* dan eksekusi di *stack-based VM* yang cepat.

### 10. **Module System**
*Import* file `.nova` lain untuk modularitas kode.

## Struktur Proyek

```
Nova-Language2/
├── nova/
│   ├── lexer/           # Tokenizer
│   ├── parser/          # Parser (AST generator)
│   ├── interpreter/     # Interpreter (Visitor Pattern)
│   ├── ast/             # AST Node definitions
│   ├── symbol_table/    # Symbol Table & Scope
│   ├── native_bridge/   # Native Function Bridge
│   ├── bytecode/        # Compiler & VM
│   ├── module/          # Module System
│   └── ast_visualizer/  # AST to JSON/Text
├── tests/               # Unit tests
├── examples/            # Contoh program .nova
├── main.py              # Entry point
├── README.md           # Dokumentasi ini
└── LICENSE             # MIT License
```

## Instalasi

```bash
git clone https://github.com/luminarydearx/Nova-Language2.git
cd Nova-Language2
```

## Quick Start

Buat file `hello.nova`:
```nova
print("Hello, Nova v2.0!")
```

Jalankan:
```bash
python main.py examples/hello.nova
```

## Contoh Kode

### Hello World
```nova
// examples/hello.nova
print("Hello from Nova Language v2.0!")
```

### Aritmatika
```nova
// examples/arithmetic.nova
var a = 10
var b = 20
print(a + b)  // 30
print(a - b)  // -10
print(a * b)  // 200
print(a / b)  // 0.5
```

### Scope (Lingkup)
```nova
// examples/scope_test.nova
var x = "global"

{
    var x = "local"
    print(x)  // Output: "local"
}

print(x)  // Output: "global"
```

### Exception Handling
```nova
// examples/try_catch.nova
try {
    print("Mencoba blok try...")
    // throw "Something went wrong"
} catch (Error e) {
    print("Tangkap: " + e)
} finally {
    print("Blok finally selalu dieksekusi")
}
```

### Native Functions
```nova
// examples/native_functions.nova
print("Waktu sekarang: " + clock())
print("Akar 16: " + sqrt(16))
```

## Testing

Jalankan semua test:
```bash
python tests/test_interpreter.py
python tests/test_samples.py
```

## Kontribusi

Pull request sangat diterima! Pastikan:
1. Kode Python mengikuti PEP 8
2. Tambahkan test untuk fitur baru
3. Update dokumentasi jika diperlukan

## Lisensi

Proyek ini dilisensikan di bawah **MIT License** - lihat file [LICENSE](LICENSE).

---

**Dibuat dengan ❤️ oleh [Dearly Febriano](https://github.com/luminarydearx)**
