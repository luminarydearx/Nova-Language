# Scope (Lingkup) Variabel - Nova Language

Nova memiliki sistem **Scope Stack** yang mengatur lingkup variabel (global, lokal, blok).

## Kode

```nova
// scope_test.nova

var x = "global"  // Variabel global

{
    // Ini blok baru - lingkup lokal
    var x = "local"  // Menimpa x hanya di blok ini
    print(x)  // Output: "local"
}

// Di luar blok, x kembali ke nilai global
print(x)  // Output: "global"
```

## Penjelasan

Nova menggunakan **Scope Stack** (tumpukan lingkup):

1. **Global Scope**: Variabel yang dideklarasikan di luar blok `{}` bisa diakses di mana saja.
2. **Local Scope**: Variabel di dalam blok `{}` hanya ada di dalam blok tersebut.
3. **Shadowing**: Variabel lokal bisa memiliki nama sama dengan global, dan akan menimpa (shadow) untuk sementara.

### Ilustrasi Stack

```
[Global]  : x = "global"
   ↓ masuk blok
[Local]   : x = "local"  ← yang ini yang aktif
   ↓ keluar blok
[Global]  : x = "global"  ← kembali ke sini
```

## Cara Menjalankan

```bash
python main.py examples/scope_test.nova
```

## Output

```
local
global
```

## Fitur yang Digunakan

- ✅ Symbol Table
- ✅ Scope Stack (Nested Scope)
- ✅ Block Statements
