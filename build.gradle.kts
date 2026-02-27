plugins {
    java
    application
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}

group   = "com.luminar"
version = "0.2.2"

application {
    mainClass.set("com.luminar.nova.Main")
    applicationName = "nova"
}

repositories {
    mavenCentral()
}

dependencies {
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.2")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

tasks.test {
    useJUnitPlatform()
}

tasks.named<org.gradle.jvm.tasks.Jar>("jar") {
    archiveBaseName.set("nova")
    archiveVersion.set(version.toString())
    manifest {
        attributes(
            "Main-Class"             to "com.luminar.nova.Main",
            "Implementation-Title"   to "Nova Language",
            "Implementation-Version" to version,
            "Built-By"               to "Luminar"
        )
    }
    from(configurations.runtimeClasspath.get()
        .map { if (it.isDirectory) it else zipTree(it) })
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE
}

tasks.named("installDist") {
    doLast {
        val bin = file("${layout.buildDirectory.get()}/install/nova/bin")
        val novaScript = File(bin, "nova")
        val novaBat    = File(bin, "nova.bat")

        if (novaScript.exists()) {
            File(bin, "nv").also {
                it.writeText(novaScript.readText())
                it.setExecutable(true, false)
            }
            println("  ✦ nv script ready")
        }
        if (novaBat.exists()) {
            File(bin, "nv.bat").writeText(novaBat.readText())
            println("  ✦ nv.bat ready")
        }
    }
}

tasks.withType<JavaCompile>().configureEach {
    options.compilerArgs.addAll(listOf("-Xlint:-serial"))
    options.release.set(21)
}