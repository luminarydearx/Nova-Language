package com.luminar.nova.cli;

import com.luminar.nova.interpreter.Interpreter;
import com.luminar.nova.interpreter.NovaRuntimeError;
import com.luminar.nova.lexer.Lexer;
import com.luminar.nova.parser.Parser;
import com.luminar.nova.parser.ast.ProgramNode;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public final class CommandDispatcher {
    private CommandDispatcher() {}

    public static int dispatch(String command, String[] args) {
        return switch (command.toLowerCase()) {
            case "run"                        -> runCmd(args);
            case "version", "-v", "--version" -> versionCmd();
            case "help",    "-h", "--help"    -> helpCmd();
            default -> { NovaConsole.err("Unknown command '" + command + "'. Try: nova help"); yield 1; }
        };
    }

    private static int runCmd(String[] args) {
        if (args.length == 0) {
            NovaConsole.err("No file specified. Usage: nova run <file.nv>");
            return 1;
        }
        String path = args[0];
        Path p = Path.of(path);
        if (!Files.exists(p)) { NovaConsole.err("File not found: " + path); return 1; }
        try {
            return runSource(Files.readString(p), path);
        } catch (IOException e) {
            NovaConsole.err("Cannot read file: " + e.getMessage()); return 1;
        }
    }

    public static int runSource(String source, String fileName) {
        Lexer lexer = new Lexer(source);
        var tokens  = lexer.tokenize();
        if (lexer.hasErrors()) {
            NovaConsole.err("Lexer errors in " + fileName + ":");
            lexer.getErrors().forEach(e -> System.err.println("    " + e));
            return 1;
        }

        Parser parser = new Parser(tokens);
        ProgramNode ast = parser.parse();
        if (parser.hasErrors()) {
            NovaConsole.err("Syntax errors in " + fileName + ":");
            parser.getErrors().forEach(e -> System.err.println("    " + e));
            return 1;
        }

        try {
            new Interpreter().execute(ast);
            return 0;
        } catch (NovaRuntimeError e) {
            NovaConsole.err("Runtime error: " + e.getMessage()); return 1;
        } catch (Exception e) {
            NovaConsole.err("Internal error: " + e.getMessage());
            if ("1".equals(System.getenv("NOVA_DEBUG"))) e.printStackTrace();
            return 1;
        }
    }

    private static int versionCmd() {
        NovaConsole.println();
        NovaConsole.println(NovaConsole.cyan("  Nova Language") + NovaConsole.gray(" · v0.5.7"));
        NovaConsole.println(NovaConsole.gray("  Types · Exceptions · OOP · Enum · Struct"));
        NovaConsole.println(NovaConsole.gray("  JVM: " + System.getProperty("java.version")));
        NovaConsole.println();
        return 0;
    }

    private static int helpCmd() {
        NovaConsole.printLogo();
        NovaConsole.println(NovaConsole.bold(NovaConsole.white("USAGE")));
        NovaConsole.println("  " + NovaConsole.cyan("nova run <file.nv>"));
        NovaConsole.println("  " + NovaConsole.cyan("nova version"));
        NovaConsole.println("  " + NovaConsole.cyan("nova help"));
        NovaConsole.println();
        NovaConsole.println(NovaConsole.bold(NovaConsole.white("FEATURES in v0.5.7")));
        NovaConsole.println("  " + NovaConsole.cyan("+= -= *= /= %=") + "    compound assign on var, member, index");
        NovaConsole.println("  " + NovaConsole.cyan("var x: int = 5") + "    type annotations (int float string bool)");
        NovaConsole.println("  " + NovaConsole.cyan("try/catch/finally") + " exception handling");
        NovaConsole.println("  " + NovaConsole.cyan("throw expr") + "        throw any value");
        NovaConsole.println("  " + NovaConsole.cyan("public/private/protected") + " method visibility");
        NovaConsole.println("  " + NovaConsole.cyan("abstract class / func") + " abstract OOP");
        NovaConsole.println("  " + NovaConsole.cyan("interface / implements") + " interfaces");
        NovaConsole.println("  " + NovaConsole.cyan("do { } while (cond)") + " do-while loop");
        NovaConsole.println("  " + NovaConsole.cyan("enum Color { R, G, B }") + " enumerations");
        NovaConsole.println("  " + NovaConsole.cyan("struct Point { x: float }") + " value structs");
        NovaConsole.println();
        return 0;
    }
}