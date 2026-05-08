# Contoh Lengkap - Nova Language v2.0

Ini adalah contoh program **Nova** yang menggunakan hampir semua fitur v2.0.

## Kode Lengkap

```nova
// full_example.nova
// Demonstrasi semua fitur Nova v2.0

// 1. Variabel & Type Inference
var nama = "Nova Developer"
const VERSION = "2.0"
var score = 100

print("=== Selamat Datang di " + nama + " ===")
print("Version: " + VERSION)

// 2. Operasi Aritmatika & Constant Folding
var a = 10
var b = 20
var c = 2 + 3  // Akan di-fold menjadi: var c = 5

print("\n--- Aritmatika ---")
print("a + b = " + (a + b))   // 30
print("a * b = " + (a * b))   // 200
print("c = " + c)               // 5 (hasil folding)

// 3. Scope (Lingkup)
print("\n--- Scope Test ---")
var x = "global"

{
    var x = "local"
    print("Di dalam blok: " + x)  // "local"
}

print("Di luar blok: " + x)      // "global"

// 4. Control Flow (If-Else)
print("\n--- Control Flow ---")
if (score >= 100) {
    print("Selamat! Skor Anda: " + score)
} else {
    print("Skor kurang")
}

// 5. Loop (While)
print("\n--- While Loop ---")
var count = 1
while (count <= 3) {
    print("Count: " + count)
    count = count + 1
}

// 6. Exception Handling
print("\n--- Exception Handling ---")
try {
    print("Mencoba blok try...")
    // throw "Test error"  // Uncomment untuk test
} catch (Error e) {
    print("Tangkap: " + e)
} finally {
    print("Blok finally selalu dieksekusi")
}

// 7. Native Functions
print("\n--- Native Functions ---")
print("Waktu saat ini: " + clock())
print("Akar 144: " + sqrt(144))

print("\n=== Program Selesai ===")
```

## Cara Menjalankan

```bash
python main.py examples/full_example.nova
```

## Output yang Diharapkan

```
=== Selamat Datang di Nova Developer ===
Version: 2.0
---
--- Aritmatika ---
a + b = 30
a * b = 200
c = 5
---
--- Scope Test ---
Di dalam blok: local
Di luar blok: global
---
--- Control Flow ---
Selamat! Skor Anda: 100
---
--- While Loop ---
Count: 1
Count: 2
Count: 3
---
--- Exception Handling ---
Mencoba blok try...
Blok finally selalu dieksekusi
---
--- Native Functions ---
Waktu saat ini: 1712345678.123
Akar 144: 12.0
===
Program Selesai ===
```

## Fitur yang Digunakan

- ✅ Variables & Constants
- ✅ Type Inference
- ✅ Arithmetic Operations
- ✅ Constant Folding
- ✅ Scope Stack (Nested)
- ✅ If-Else Statements
- ✅ While Loops
- ✅ Exception Handling (Try-Catch-Finally)
- ✅ Native Function Bridge (`clock()`, `sqrt()`)
- ✅ String Concatenation
- ✅ Print Statements

## Struktur Kode

| Baris | Fitur |
|-------|-------|
| 7-9 | Var & Const Declarations |
| 18-27 | Arithmetic & Constant Folding |
| 30-37 | Scope Test |
| 40-46 | If-Else Control Flow |
| 49-56 | While Loop |
| 59-68 | Try-Catch-Finally |
| 71-74 | Native Functions |

---

**Ini adalah contoh lengkap bagaimana Nova v2.0 bekerja!** 🚀
