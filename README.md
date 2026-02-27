# ✦ Nova Language

Nova adalah bahasa pemrograman dinamis (dynamically typed) yang didesain untuk menjadi sederhana, ekspresif, dan mudah dipelajari. Proyek ini merupakan interpreter berbasis Java (Tree-walking interpreter) yang memberikan kebebasan dalam menulis kode tanpa boilerplate yang berlebihan.

---

## 🚀 Fitur Utama

- **Variabel Dinamis:** Dukungan untuk `var` (mutable) dan `const` (immutable).
- **Struktur Data Bawaan:** Mendukung Arrays `[...]` dan Objects/Dictionaries `{...}`.
- **Fungsi & Closures:** Mendukung pembuatan fungsi kustom menggunakan `func` dengan dukungan lexically scoped closures.
- **Kontrol Alur:** `if`/`else`, `while`, dan `for...in` dengan rentang (range) seperti `0..10`.
- **Ekspresi Bertenaga:** Operator ternary, aritmatika lengkap (`**` untuk eksponen), dan compound assignments (`+=`, `-=`, dll).
- **Method Bawaan:** Dukungan pemanggilan metode langsung pada tipe data (misal: `[1, 2].push(3)` atau `"hello".upper()`).

---

## 💻 Memulai (Getting Started)

### Prasyarat
- Java 21 atau versi yang lebih baru.
- Gradle (termasuk via Gradle Wrapper `gradlew`).

### Menjalankan File Nova
Kamu bisa menulis kode Nova di dalam file berektensi `.nv` atau `.nova`.

Lalu jalankan menggunakan CLI Nova:
```bash
./gradlew run --args="run contoh.nv"
```

---

## 📖 Sintaks dan Contoh Penggunaan

Berikut adalah contoh bagaimana kode Nova bekerja di berbagai kasus:

### 1. Variabel dan Tipe Data
```nova
var nama = "Nova"
const versi = 0.2
var isKeren = true

print "Bahasa: " + nama + " v" + str(versi)
```

### 2. Logika Kondisional (If / Else)
```nova
var umur = 20

if (umur >= 18) {
    print "Sudah dewasa"
} else {
    print "Masih di bawah umur"
}
```

### 3. Perulangan (Loops)
**For Loop (dengan Range):**
```nova
// Mencetak angka 1 sampai 5
for i in 1..6 {
    print i
}
```

**While Loop:**
```nova
var counter = 0
while (counter < 3) {
    print "Counter: " + str(counter)
    counter += 1
}
```

### 4. Arrays
Arrays di Nova mensupport metode seperti `push`, `pop`, `len()`, dsb.
```nova
var buah = ["Apel", "Mangga", "Jeruk"]
buah.push("Pisang")
print buah[0] // Ouput: Apel

for b in buah {
    print "- " + b
}
```

### 5. Objects / Dictionaries
```nova
var user = {
    "nama": "Dearly",
    "role": "Developer"
}

// Bisa diakses via bracket atau dot notation
print user.nama
user.role = "Admin"
print user["role"]
```

### 6. Fungsi (Functions)
```nova
func sapa(nama) {
    return "Halo, " + nama + "!"
}

print sapa("Dunia")
```

---

## 🛠 Fungsi Bawaan (Built-ins)
Nova datang dengan berbagai fungsi bawaan:
- Konversi: `int(x)`, `float(x)`, `str(x)`, `bool(x)`
- Array/Object: `len(x)`, `push(arr, val)`, `pop(arr)`, `keys(obj)`, `values(obj)`
- Matematika: `abs(n)`, `max(a, b)`, `min(a, b)`, `sqrt(n)`, `floor(n)`, `ceil(n)`, `round(n)`
- Utilitas Tambahan: `print(x)`, `input(prompt)`, `type(x)`, `exit(code)`

---

*The universe compiles in Nova.* ✦