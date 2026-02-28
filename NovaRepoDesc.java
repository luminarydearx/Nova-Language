import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;
import java.security.SecureRandom;
import java.security.spec.KeySpec;
import java.util.Base64;
import java.nio.charset.StandardCharsets;

/**
 * NovaRepoDesc Utility (Secure Edition)
 * Digunakan untuk mengenkripsi/mendekripsi teks deskripsi repositori.
 * Password diminta saat runtime agar tidak tersimpan di dalam kode.
 */
public class NovaRepoDesc {
    private static final byte[] SALT = "NovaLangDescSalt2024".getBytes();
    private static final int ITERATIONS = 65536;
    private static final int KEY_LENGTH = 256;

    public static void main(String[] args) throws Exception {
        if (args.length < 2) {
            System.out.println("Penggunaan:");
            System.out.println("  java NovaRepoDesc encrypt \"teks yang ingin dienkripsi\"");
            System.out.println("  java NovaRepoDesc decrypt \"kode_base64_hasil_enkripsi\"");
            return;
        }

        String mode = args[0];
        String input = args[1];

        // Meminta password secara aman tanpa menampilkannya di layar (jika didukung terminal)
        String password;
        if (System.console() != null) {
            char[] pwChars = System.console().readPassword("Masukkan Password: ");
            password = new String(pwChars);
        } else {
            System.out.print("Masukkan Password: ");
            password = new java.util.Scanner(System.in).nextLine();
        }

        if (password == null || password.isEmpty()) {
            System.err.println("Password tidak boleh kosong!");
            return;
        }

        try {
            if (mode.equalsIgnoreCase("encrypt")) {
                String encrypted = encrypt(input, password);
                System.out.println("\n--- HASIL ENKRIPSI ---");
                System.out.println(encrypted);
                System.out.println("----------------------");
            } else if (mode.equalsIgnoreCase("decrypt")) {
                String decrypted = decrypt(input, password);
                System.out.println("\n--- HASIL DEKRIPSI ---");
                System.out.println(decrypted);
                System.out.println("----------------------");
            }
        } catch (Exception e) {
            System.err.println("\n[ERROR] Gagal: Mungkin password salah atau data rusak.");
        }
    }

    public static String encrypt(String strToEncrypt, String password) throws Exception {
        byte[] iv = new byte[16];
        new SecureRandom().nextBytes(iv);
        IvParameterSpec ivspec = new IvParameterSpec(iv);

        SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        KeySpec spec = new PBEKeySpec(password.toCharArray(), SALT, ITERATIONS, KEY_LENGTH);
        SecretKey tmp = factory.generateSecret(spec);
        SecretKeySpec secretKey = new SecretKeySpec(tmp.getEncoded(), "AES");

        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey, ivspec);

        byte[] encrypted = cipher.doFinal(strToEncrypt.getBytes(StandardCharsets.UTF_8));
        byte[] combined = new byte[iv.length + encrypted.length];
        System.arraycopy(iv, 0, combined, 0, iv.length);
        System.arraycopy(encrypted, 0, combined, iv.length, encrypted.length);

        return Base64.getEncoder().encodeToString(combined);
    }

    public static String decrypt(String strToDecrypt, String password) throws Exception {
        byte[] combined = Base64.getDecoder().decode(strToDecrypt);
        byte[] iv = new byte[16];
        System.arraycopy(combined, 0, iv, 0, 16);
        IvParameterSpec ivspec = new IvParameterSpec(iv);

        byte[] encrypted = new byte[combined.length - 16];
        System.arraycopy(combined, 16, encrypted, 0, encrypted.length);

        SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        KeySpec spec = new PBEKeySpec(password.toCharArray(), SALT, ITERATIONS, KEY_LENGTH);
        SecretKey tmp = factory.generateSecret(spec);
        SecretKeySpec secretKey = new SecretKeySpec(tmp.getEncoded(), "AES");

        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.DECRYPT_MODE, secretKey, ivspec);

        return new String(cipher.doFinal(encrypted), StandardCharsets.UTF_8);
    }
}
