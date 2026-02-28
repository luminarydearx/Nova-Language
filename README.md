# ✦ Nova Language (v0.4.0)

Nova adalah bahasa pemrograman dinamis (dynamically typed) yang didesain untuk menjadi sederhana, ekspresif, dan bertenaga. Proyek ini merupakan interpreter berbasis Java (Tree-walking interpreter) yang menghadirkan fitur modern tanpa boilerplate yang berlebihan.

---

## 🚀 Fitur Baru (v0.4.0)

- **OOP Lanjutan:** Dukungan penuh untuk `class`, `interface`, `abstract` classes/methods, dan **Visibility Modifiers** (`public`, `private`, `protected`).
- **Exception Handling:** Blok `try`, `catch`, `finally`, serta keyword `throw` untuk penanganan error yang robust.
- **Struktur Data:** Pengenalan `struct` untuk data ringan dan `enum` untuk konstanta kategori.
- **Perulangan Baru:** Ditambahkan `do-while` loop.
- **Tipe Data & Coercion:** Dukungan eksplisit untuk tipe `int`, `float`, `string`, dan `bool`.
- **Compound assignments:** `+=`, `-=`, `*=`, `/=`, `%=`, `**=`.

---

## 🚀 Fitur Utama

- **Variabel Dinamis:** Dukungan untuk `var` (mutable) dan `const` (immutable).
- **Struktur Data Luas:** Mendukung Arrays `[...]`, Objects `{...}`, Structs, dan Enums.
- **Fungsi & Closures:** Dukungan pembuatan fungsi kustom menggunakan `func` dengan lexically scoped closures.
- **Kontrol Alur:** `if`/`else`, `while`, `do-while`, dan `for...in` dengan rentang (range) `0..10`.
- **Ekspresi Bertenaga:** Operator ternary, aritmatika lengkap (`**` untuk eksponen), dan compound assignments.
- **Method Bawaan:** Dukungan pemanggilan metode langsung pada tipe data (misal: `[1, 2].push(3)` atau `"hello".upper()`).

---

## 📖 Sintaks dan Contoh Penggunaan

### 1. Object Oriented Programming (OOP)

```nova
interface IPrintable {
    func printInfo(): void;
}

class User implements IPrintable {
    private var id: string;
    public var name: string;

    func init(id: string, name: string) {
        this.id = id;
        this.name = name;
    }

    public func printInfo(): void {
        print "User ID: " + this.id + " | Name: " + this.name;
    }
}

var u = new User("USR-001", "Dearly");
u.printInfo();
```

### 2. Exception Handling

```nova
try {
    print "Starting operation...";
    throw "Fatal Error Occurred";
} catch (e) {
    print "Caught exception: " + str(e);
} finally {
    print "System cleanup completed.";
}
```

### 3. Structs & Enums

```nova
struct Point {
    x: int;
    y: int;
}

enum Status { IDLE, RUNNING, ERROR }

var p = new Point(10, 20);
var s = Status.RUNNING;
print "Point: " + str(p);
print "Status: " + str(s);
```

### 4. Control Flow & Loops

```nova
// Ternary operator
var score = 85;
var status = score >= 75 ? "Passed" : "Failed";
print status; // Out: Passed

// Do-while & For
var count = 0;
do {
    count += 1;
} while (count < 3);

for i in 1..4 {
    print "Loop Index: " + str(i);
}
```

### 5. Concurrency (Async/Await)

Nova supports non-blocking execution using `spawn` and `await`.

```nova
var task = spawn(func() {
    // Background work
    return "Result from thread"
});

print "Main thread continues...";
var val = await task;
print val;
```

---

## 🛠 Fungsi Bawaan (Built-ins)

Nova datang dengan berbagai fungsi bawaan:

- **Konversi:** `int(x)`, `float(x)`, `str(x)`, `bool(x)`
- **Array/Object:** `len(x)`, `push(arr, val)`, `pop(arr)`, `keys(obj)`, `values(obj)`
- **Matematika:** `abs(n)`, `max(a, b)`, `min(a, b)`, `sqrt(n)`, `PI`
- **Utilitas:** `print(x)`, `input(prompt)`, `type(x)`, `exit(code)`

---

## 💻 Memulai (Getting Started)

### Prasyarat

- Java 21 atau versi yang lebih baru.
- Gradle (termasuk via Gradle Wrapper `gradlew`).

### Menjalankan File Nova

```bash
./gradlew run --args="run my_code.nv"
```

---

_The universe compiles in Nova._ ✦
