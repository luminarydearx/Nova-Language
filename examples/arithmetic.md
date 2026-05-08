# Operasi Aritmatika - Nova Language

Nova mendukung semua operasi matematika dasar dan optimasi **Constant Folding**.

## Kode

```nova
// arithmetic.nova

var a = 10
var b = 20

// Operasi dasar
print(a + b)  // Penjumlahan: 30
print(a - b)  // Pengurangan: -10
print(a * b)  // Perkalian: 200
print(a / b)  // Pembagian: 0.5
print(a % b)  // Modulo: 10

// Constant Folding (2 + 3 otomatis jadi 5 saat parsing)
var c = 2 + 3
print(c)  // 5
```

## Penjelasan

### Operator Aritmatika

| Operator | Keterangan | Contoh |
|----------|-------------|--------|
| `+` | Penjumlahan | `a + b` |
| `-` | Pengurangan | `a - b` |
| `*` | Perkalian | `a * b` |
| `/` | Pembagian | `a / b` |
| `%` | Modulo (sisa bagi) | `a % b` |
| `**` | Pangkat | `a ** 2` |

### Constant Folding

Nova melakukan optimasi saat compile-time. Jika menemukan:
```nova
var x = 2 + 3
```
Kompiler akan mengubahnya menjadi:
```nova
var x = 5
```
Ini membuat eksekusi lebih cepat karena tidak perlu menghitung ulang.

## Cara Menjalankan

```bash
python main.py examples/arithmetic.nova
```

## Output

```
30
-10
200
0.5
10
5
```

## Fitur yang Digunakan

- ✅ Binary Expressions
- ✅ Constant Folding
- ✅ Arithmetic Operators
