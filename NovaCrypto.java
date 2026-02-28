import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;
import java.io.*;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.security.SecureRandom;
import java.security.spec.KeySpec;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;
import java.util.zip.ZipOutputStream;

/**
 * NovaCrypto
 * Alat untuk mengenkripsi (dan mendekripsi) folder 'src/' milik proyek Nova
 * menggunakan AES-256 dan password agar kode tertutup secara rahasia.
 */
public class NovaCrypto {

    private static final String SRC_DIR = "src";
    private static final String TEMP_ZIP = "src_temp.zip";
    private static final String ENCRYPTED_FILE = "nova_source.enc";

    private static final byte[] SALT = "NovaLangSalt2024".getBytes();
    private static final int ITERATIONS = 65536;
    private static final int KEY_LENGTH = 256;

    public static void main(String[] args) {
        if (args.length != 1 || (!args[0].equals("encrypt") && !args[0].equals("decrypt"))) {
            System.out.println("Penggunaan:");
            System.out.println("  java NovaCrypto encrypt  -> Akan mengenkripsi folder src/ dan menghapusnya.");
            System.out.println("  java NovaCrypto decrypt  -> Akan mendekripsi file nova_source.enc kembali menjadi folder src/.");
            System.exit(1);
        }

        try {
            if (args[0].equals("encrypt")) {
                if (!Files.exists(Path.of(SRC_DIR))) {
                    System.err.println("Folder 'src' tidak ditemukan. Mungkin sudah dienkripsi?");
                    return;
                }
                
                System.out.println("====== PROSES ENKRIPSI KODE ======");
                System.out.println("Buat password rahasia (contoh: secretcode123):");
                String inputPw = readPassword();

                System.out.println("1. Mengkompresi folder src/ ...");
                zipFolder(Path.of(SRC_DIR), Path.of(TEMP_ZIP));

                System.out.println("2. Mengenkripsi menjadi " + ENCRYPTED_FILE + " ...");
                encryptFile(TEMP_ZIP, ENCRYPTED_FILE, inputPw);

                System.out.println("3. Membersihkan file asli ...");
                Files.delete(Path.of(TEMP_ZIP));
                deleteDirectory(Path.of(SRC_DIR));

                System.out.println("\nBerhasil! Kode proyek berhasil dienkripsi dan diproteksi.");
                System.out.println("KINI ANDA BISA MENGHAPUS FILE 'NovaCrypto.java' INI ATAU MEMASUKKANNYA KE .gitignore AGAR AMAN!");

            } else if (args[0].equals("decrypt")) {
                if (!Files.exists(Path.of(ENCRYPTED_FILE))) {
                    System.err.println("File '" + ENCRYPTED_FILE + "' tidak ditemukan.");
                    return;
                }
                
                System.out.println("====== PROSES DEKRIPSI KODE ======");
                System.out.println("Tolong masukkan password untuk membuka kunci:");
                String inputPw = readPassword();

                System.out.println("1. Mendekripsi file " + ENCRYPTED_FILE + " ...");
                decryptFile(ENCRYPTED_FILE, TEMP_ZIP, inputPw);

                System.out.println("2. Mengekstrak kembali ke folder src/ ...");
                unzip(TEMP_ZIP, new File("."));

                System.out.println("3. Membersihkan kunci sementara ...");
                Files.delete(Path.of(TEMP_ZIP));

                System.out.println("\nBerhasil! Folder 'src/' kembali seperti sedia kala.");
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.err.println("Terjadi kesalahan (Mungkin Password Salah / File Rusak): " + e.getMessage());
        }
    }

    private static String readPassword() {
        return System.console() != null 
            ? new String(System.console().readPassword()) 
            : new java.util.Scanner(System.in).nextLine();
    }

    private static SecretKey getAESKeyFromPassword(String password) throws Exception {
        SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        KeySpec spec = new PBEKeySpec(password.toCharArray(), SALT, ITERATIONS, KEY_LENGTH);
        SecretKey secret = new SecretKeySpec(factory.generateSecret(spec).getEncoded(), "AES");
        return secret;
    }

    private static void encryptFile(String inputFile, String outputFile, String password) throws Exception {
        SecretKey secretKey = getAESKeyFromPassword(password);
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        
        byte[] iv = new byte[16];
        new SecureRandom().nextBytes(iv);
        IvParameterSpec ivParameterSpec = new IvParameterSpec(iv);
        cipher.init(Cipher.ENCRYPT_MODE, secretKey, ivParameterSpec);

        try (FileInputStream fis = new FileInputStream(inputFile);
             FileOutputStream fos = new FileOutputStream(outputFile)) {
            fos.write(iv); // Simpan IV di awal file
            byte[] in = new byte[64 * 1024];
            int read;
            while ((read = fis.read(in)) != -1) {
                byte[] output = cipher.update(in, 0, read);
                if (output != null) fos.write(output);
            }
            byte[] outputBytes = cipher.doFinal();
            if (outputBytes != null) fos.write(outputBytes);
        }
    }

    private static void decryptFile(String inputFile, String outputFile, String password) throws Exception {
        SecretKey secretKey = getAESKeyFromPassword(password);
        
        try (FileInputStream fis = new FileInputStream(inputFile);
             FileOutputStream fos = new FileOutputStream(outputFile)) {
            
            byte[] iv = new byte[16];
            fis.read(iv); // Baca IV dari awal file
            
            Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
            cipher.init(Cipher.DECRYPT_MODE, secretKey, new IvParameterSpec(iv));

            byte[] in = new byte[64 * 1024];
            int read;
            while ((read = fis.read(in)) != -1) {
                byte[] output = cipher.update(in, 0, read);
                if (output != null) fos.write(output);
            }
            byte[] outputBytes = cipher.doFinal();
            if (outputBytes != null) fos.write(outputBytes);
        }
    }

    // --- ZIP UTILS ---
    private static void zipFolder(Path sourceFolderPath, Path zipPath) throws Exception {
        try (ZipOutputStream zos = new ZipOutputStream(new FileOutputStream(zipPath.toFile()))) {
            Files.walkFileTree(sourceFolderPath, new java.nio.file.SimpleFileVisitor<>() {
                @Override
                public java.nio.file.FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
                    Path base = sourceFolderPath.getParent();
                    String entryName = (base != null ? base.relativize(file) : file).toString().replace("\\", "/");
                    zos.putNextEntry(new ZipEntry(entryName));
                    Files.copy(file, zos);
                    zos.closeEntry();
                    return java.nio.file.FileVisitResult.CONTINUE;
                }
            });
        }
    }

    private static void unzip(String zipFilePath, File destDir) throws Exception {
        try (ZipInputStream zis = new ZipInputStream(new FileInputStream(zipFilePath))) {
            ZipEntry zipEntry = zis.getNextEntry();
            while (zipEntry != null) {
                File newFile = new File(destDir, zipEntry.getName());
                if (zipEntry.isDirectory()) {
                    newFile.mkdirs();
                } else {
                    new File(newFile.getParent()).mkdirs();
                    try (FileOutputStream fos = new FileOutputStream(newFile)) {
                        byte[] buffer = new byte[1024];
                        int len;
                        while ((len = zis.read(buffer)) > 0) fos.write(buffer, 0, len);
                    }
                }
                zipEntry = zis.getNextEntry();
            }
            zis.closeEntry();
        }
    }

    private static void deleteDirectory(Path path) throws IOException {
        Files.walk(path)
            .sorted(java.util.Comparator.reverseOrder())
            .map(Path::toFile)
            .forEach(File::delete);
    }
}
