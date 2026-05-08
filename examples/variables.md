# Variabel & Tipe Data - Nova Language

Nova mendukung deklarasi variabel dengan kata kunci `var` dan `const`, serta dilengkapi dengan **Type Inference**.

## Kode

```nova
// variables.nova

// Type inference: tipe data ditentukan otomatis
var nama = "Dearly"
var umur = 20
var aktif = true

// Const (konstanta, tidak bisa diubah)
const PI = 3.14159

// Dengan anotasi tipe (opsional)
var skor: int = 100

print(nama)
print(umur)
print(aktif)
print(PI)
print(skor)
```

## Penjelasan

| Keyword | Keterangan |
|---------|-------------|
| `var` | Variabel yang bisa diubah nilainya |
| `const` | Konstanta (nilai tetap) |
| `: tipe` | Anotasi tipe (opsional) |

**Type Inference:** Jika anotasi tipe tidak ditulis, Nova akan menebak tipe dari nilai yang diberikan.

## Tabel Tipe Data

| Nilai | Tipe Terdeteksi |
|-------|----------------|
| `"teks"` | `string` |
| `123` | `int` |
| `3.14` | `float` |
| `true/false` | `bool` |
| `null` | `none` |

## Cara Menjalankan

```bash
python main.py examples/variables.nova
```

## Output

```
Dearly
20
True
3.14159
100
```

## Fitur yang Digunakan

- ✅ Var & Const Declarations
- ✅ Type Inference
- ✅ Symbol Table
- ✅ Type Annotations (Optional)
