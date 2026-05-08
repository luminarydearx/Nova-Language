# Native Functions - Nova Language

Nova dapat memanggil **fungsi native Python** melalui *Native Function Bridge*.

## Kode

```nova
// native_functions.nova

// Fungsi waktu (dari time.time() Python)
print("Waktu sekarang: " + clock())

// Fungsi matematika (dari math.sqrt() Python)
print("Akar 16: " + sqrt(16))
print("Akar 25: " + sqrt(25))
```

## Penjelasan

Nova menyediakan **Native Function Bridge** yang memungkinkan bahasa ini memanggil fungsi Python langsung.

### Fungsi Bawaan (Built-in)

| Fungsi | Deskripsi | Contoh |
|--------|-------------|--------|
| `clock()` | Mengembalikan waktu saat ini (detik) | `clock()` → `1623456789.123` |
| `sqrt(x)` | Akar kuadrat dari x | `sqrt(16)` → `4.0` |

### Cara Kerja

1. Di dalam `Interpreter.__init__()`, fungsi Python didaftarkan sebagai `NativeFunction`
2. Saat Nova memanggil `sqrt(16)`, interpreter akan:
   - Mencari `sqrt` di Symbol Table
   - Mendapatkan object `NativeFunction`
   - Memanggil `call(args)` → menjalankan `math.sqrt(16)`

## Cara Menjalankan

```bash
python main.py examples/native_functions.nova
```

## Output

```
Waktu sekarang: 1.71123456789
Akar 16: 4.0
Akar 25: 5.0
```

## Menambah Fungsi Baru

Untuk menambah fungsi native, edit `nova/interpreter/interpreter.py`:

```python
def _register_natives(self):
    # Fungsi string length
    len_fn = NativeFunction("len", 1, len)
    self.scope.define("len", "native", len_fn, True, "public")
    
    # Fungsi lainnya...
```

## Fitur yang Digunakan

- ✅ Native Function Bridge
- ✅ Symbol Table Integration
- ✅ Python Interoperability
