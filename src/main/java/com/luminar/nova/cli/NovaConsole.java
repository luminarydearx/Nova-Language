package com.luminar.nova.cli;

public final class NovaConsole {
    private NovaConsole() {}

    private static final boolean ANSI;
    static {
        boolean notWin = !System.getProperty("os.name","").toLowerCase().contains("win");
        String term    = System.getenv("TERM");
        ANSI = notWin && term != null && !term.equalsIgnoreCase("dumb");
    }

    private static String c(String code, String s) { return ANSI ? code + s + "\u001B[0m" : s; }

    public static String cyan(String s)   { return c("\u001B[96m", s); }
    public static String purple(String s) { return c("\u001B[95m", s); }
    public static String green(String s)  { return c("\u001B[92m", s); }
    public static String yellow(String s) { return c("\u001B[93m", s); }
    public static String red(String s)    { return c("\u001B[91m", s); }
    public static String white(String s)  { return c("\u001B[97m", s); }
    public static String gray(String s)   { return c("\u001B[90m", s); }
    public static String bold(String s)   { return c("\u001B[1m",  s); }

    public static void println(String s) { System.out.println(s); }
    public static void println()         { System.out.println(); }

    public static void err(String msg)   { System.err.println(red("  ✖ ") + msg); }
    public static void info(String msg)  { System.out.println(cyan("  ✦ ") + msg); }

    public static void printLogo() {
        println();
        println(bold(white("    ███╗   ██╗ ██████╗ ██╗   ██╗  █████╗")));
        println(bold(white("    ████╗  ██║██╔═══██╗██║   ██║ ██╔══██╗")));
        println(bold(cyan( "    ██╔██╗ ██║██║   ██║██║   ██║ ███████║")));
        println(bold(purple("    ██║╚████║╚██████╔╝╚██╗ ██╔╝ ██╔══██║")));
        println(bold(gray(  "    ╚═╝ ╚═══╝ ╚═════╝  ╚═══╝   ╚═╝  ╚═╝")));
        println();
        println(cyan("    ✦ v0.5.7") + gray("  ·  Types · Exceptions · OOP · Enum · Struct"));
        println();
    }
}