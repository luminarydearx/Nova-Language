# Exception Handling (Try-Catch) - Nova Language

Nova menyediakan sistem **Exception Handling** dengan `try-catch-finally` yang *robust*.

## Kode

```nova
// try_catch.nova

try {
    print("Mencoba blok try...")
    // throw "Something went wrong"  // Uncomment untuk test
} catch (Error e) {
    print("Tangkap: " + e)
} finally {
    print("Blok finally selalu dieksekusi")
}
```

## Penjelasan

### Struktur Try-Catch

| Keyword | Keterangan |
|---------|-------------|
| `try` | Blok yang mungkin memicu error |
| `catch` | Blok penangkap error (bisa beberapa) |
| `finally` | Blok yang selalu dijalankan (bersih-bersih) |
| `throw` | Melempar exception secara manual |

### Cara Kerja

1. Kode di dalam `try` dijalankan
2. Jika ada error → pindah ke `catch`
3. Setelah semua, `finally` dieksekusi (baik ada error atau tidak)

## Cara Menjalankan

```bash
python main.py examples/try_catch.nova
```

## Output (Normal)

```
Mencoba blok try...
Blok finally selalu dieksekusi
```

## Output (Jika throw aktif)

```
Mencoba blok try...
Tangkap: Something went wrong
Blok finally selalu dieksekusi
```

## Fitur yang Digunakan

- ✅ Exception Handling System
- ✅ TryCatchNode & ThrowNode
- ✅ Runtime Error Management
