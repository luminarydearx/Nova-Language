plugins {
    java
    application
}

java {
    toolchain { languageVersion.set(JavaLanguageVersion.of(21)) }
}

group = "com.luminar"
version = "0.5.7"

repositories {
    mavenCentral()
}

application {
    mainClass.set("com.luminar.nova.Main")
    applicationName = "nova"
}

tasks.named<org.gradle.jvm.tasks.Jar>("jar") {
    archiveBaseName.set("nova")
    manifest { attributes("Main-Class" to "com.luminar.nova.Main") }
    from(configurations.runtimeClasspath.get().map { if (it.isDirectory) it else zipTree(it) })
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE
}

// After installDist, create "nv" as alias for "nova"
tasks.named("installDist") {
    doLast {
        val bin = file("${layout.buildDirectory.get()}/install/nova/bin")
        val novaScript = File(bin, "nova")
        if (novaScript.exists()) {
            File(bin, "nv").also { it.writeText(novaScript.readText()); it.setExecutable(true, false) }
        }
        val novaBat = File(bin, "nova.bat")
        if (novaBat.exists()) File(bin, "nv.bat").writeText(novaBat.readText())
    }
}

tasks.withType<JavaCompile>().configureEach { options.release.set(21) }