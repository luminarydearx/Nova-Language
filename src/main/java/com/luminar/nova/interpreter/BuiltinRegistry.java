package com.luminar.nova.interpreter;

import java.awt.Component;
import java.awt.FlowLayout;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import javax.swing.*;

/**
 * Memisahkan logika registrasi builtin untuk maintenance yang lebih mudah.
 */
public final class BuiltinRegistry {

    public static void register(Interpreter interp, Environment globals) {
        // ── Core I/O ──
        globals.define("print", new NativeFunction((i, args) -> { System.out.println(interp.str(args.isEmpty() ? null : args.get(0))); return null; }));
        globals.define("readLine", new NativeFunction((i, args) -> {
            if (!args.isEmpty()) System.out.print(interp.str(args.get(0)));
            try { return new java.io.BufferedReader(new java.io.InputStreamReader(System.in)).readLine(); } catch (Exception e) { return null; }
        }));

        // ── Type conversion ──
        globals.define("int", new NativeFunction((i, args) -> interp.toLong(args.isEmpty() ? 0L : args.get(0))));
        globals.define("float", new NativeFunction((i, args) -> interp.num(args.isEmpty() ? 0.0 : args.get(0))));
        globals.define("str", new NativeFunction((i, args) -> interp.str(args.isEmpty() ? null : args.get(0))));
        globals.define("bool", new NativeFunction((i, args) -> interp.truthy(args.isEmpty() ? null : args.get(0))));
        globals.define("typeOf", new NativeFunction((i, args) -> interp.typeName(args.isEmpty() ? null : args.get(0))));
        globals.define("len", new NativeFunction((i, args) -> {
            if (args.isEmpty()) return 0L;
            Object v = args.get(0);
            if (v instanceof String s) return (long) s.length();
            if (v instanceof List<?> l) return (long) l.size();
            if (v instanceof Map<?,?> m) return (long) m.size();
            return 0L;
        }));

        // ── Namespaces ──
        registerMath(interp, globals);
        registerJSON(interp, globals);
        registerDate(interp, globals);

        // ── System ──
        globals.define("range", new NativeFunction((i, a) -> {
            long from = a.isEmpty() ? 0 : interp.toLong(a.get(0));
            long to = a.size() < 2 ? from : interp.toLong(a.get(1));
            return new NovaRange(a.size() < 2 ? 0 : from, to);
        }));
        globals.define("sleep", new NativeFunction((i, a) -> { try { Thread.sleep(interp.toLong(a.get(0))); } catch (Exception e) {} return null; }));
        globals.define("exit", new NativeFunction((i, a) -> { System.exit(a.isEmpty() ? 0 : (int)interp.toLong(a.get(0))); return null; }));
        globals.define("time", new NativeFunction((i, a) -> System.currentTimeMillis()));
        globals.define("readFile", new NativeFunction((i, a) -> { try { return Files.readString(Path.of(interp.str(a.get(0)))); } catch (Exception e) { return null; } }));
        globals.define("writeFile", new NativeFunction((i, a) -> { try { Files.writeString(Path.of(interp.str(a.get(0))), interp.str(a.get(1))); } catch (Exception e) {} return null; }));
        globals.define("spawn", new NativeFunction((i, a) -> java.util.concurrent.CompletableFuture.supplyAsync(() -> ((NovaCallable)a.get(0)).call(interp, new ArrayList<>()))));

        // ── Engines ──
        registerGUISupport(interp, globals);
        registerWebServer(interp, globals);

        globals.define("VERSION", "0.5.7");
    }

    private static void registerMath(Interpreter interp, Environment globals) {
        Map<String, Object> math = new LinkedHashMap<>();
        math.put("PI", Math.PI); math.put("E", Math.E);
        math.put("abs", new NativeFunction((i, a) -> Math.abs(interp.num(a.get(0)))));
        math.put("sqrt", new NativeFunction((i, a) -> Math.sqrt(interp.num(a.get(0)))));
        math.put("floor", new NativeFunction((i, a) -> (long)Math.floor(interp.num(a.get(0)))));
        math.put("ceil", new NativeFunction((i, a) -> (long)Math.ceil(interp.num(a.get(0)))));
        math.put("pow", new NativeFunction((i, a) -> Math.pow(interp.num(a.get(0)), interp.num(a.get(1)))));
        math.put("random", new NativeFunction((i, a) -> Math.random()));
        globals.define("Math", math);
        globals.define("PI", Math.PI);
    }

    private static void registerJSON(Interpreter interp, Environment globals) {
        Map<String, Object> json = new LinkedHashMap<>();
        json.put("stringify", new NativeFunction((i, a) -> interp.jsonStringify(a.get(0))));
        globals.define("JSON", json);
    }

    private static void registerDate(Interpreter interp, Environment globals) {
        Map<String, Object> date = new LinkedHashMap<>();
        date.put("now", new NativeFunction((i, a) -> System.currentTimeMillis()));
        date.put("format", new NativeFunction((i, a) -> {
            String fmt = a.size() > 1 ? interp.str(a.get(1)) : "yyyy-MM-dd HH:mm:ss";
            return new java.text.SimpleDateFormat(fmt).format(new java.util.Date(a.isEmpty() ? System.currentTimeMillis() : interp.toLong(a.get(0))));
        }));
        date.put("year", new NativeFunction((i, a) -> (long) java.time.LocalDate.now().getYear()));
        date.put("month", new NativeFunction((i, a) -> (long) java.time.LocalDate.now().getMonthValue()));
        date.put("day", new NativeFunction((i, a) -> (long) java.time.LocalDate.now().getDayOfMonth()));
        globals.define("Date", date);
    }

    private static void registerGUISupport(Interpreter interp, Environment globals) {
        globals.define("window", new NativeFunction((i, a) -> {
            String title = a.isEmpty() ? "Nova" : interp.str(a.get(0));
            int w = a.size() > 1 ? (int)interp.toLong(a.get(1)) : 500;
            int h = a.size() > 2 ? (int)interp.toLong(a.get(2)) : 400;
            JFrame f = new JFrame(title); f.setSize(w, h); f.setLayout(null); f.setLocationRelativeTo(null); f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            Map<String, Object> win = new LinkedHashMap<>();
            win.put("show", new NativeFunction((i2, a2) -> { f.setVisible(true); return win; }));
            win.put("add", new NativeFunction((i2, a2) -> { for(Object o : a2) if(o instanceof Component c) f.add(c); return win; }));
            win.put("setBackground", new NativeFunction((i2, a2) -> { f.getContentPane().setBackground((java.awt.Color)a2.get(0)); return win; }));
            return win;
        }));

        globals.define("label", new NativeFunction((i, a) -> new JLabel(interp.str(a.get(0)))));
        globals.define("button", new NativeFunction((i, a) -> {
            JButton b = new JButton(interp.str(a.get(0)));
            if(a.size() > 1 && a.get(1) instanceof NovaCallable fn) b.addActionListener(e -> fn.call(interp, List.of()));
            return b;
        }));
        globals.define("style", new NativeFunction((i, a) -> {
            Component c = (Component)a.get(0); Map<String,Object> p = (Map<String,Object>)a.get(1);
            if(p.containsKey("x")) c.setBounds((int)interp.toLong(p.get("x")), (int)interp.toLong(p.get("y")), (int)interp.toLong(p.get("width")), (int)interp.toLong(p.get("height")));
            if(p.containsKey("background")) c.setBackground((java.awt.Color)p.get("background"));
            if(p.containsKey("foreground")) c.setForeground((java.awt.Color)p.get("foreground"));
            return c;
        }));
        globals.define("Color", new NativeFunction((i, a) -> a.size() >= 3 ? new java.awt.Color((int)interp.toLong(a.get(0)), (int)interp.toLong(a.get(1)), (int)interp.toLong(a.get(2))) : java.awt.Color.decode(interp.str(a.get(0)))));
    }

    private static void registerWebServer(Interpreter interp, Environment globals) {
        globals.define("serve", new NativeFunction((i, a) -> {
            int port = a.isEmpty() ? 8080 : (int)interp.toLong(a.get(0));
            try {
                com.sun.net.httpserver.HttpServer server = com.sun.net.httpserver.HttpServer.create(new java.net.InetSocketAddress(port), 0);
                Map<String, Object> srv = new LinkedHashMap<>();
                srv.put("route", new NativeFunction((i2, a2) -> {
                    server.createContext(interp.str(a2.get(0)), ex -> {
                        String res = interp.str(((NovaCallable)a2.get(1)).call(interp, List.of()));
                        ex.sendResponseHeaders(200, res.length());
                        ex.getResponseBody().write(res.getBytes()); ex.getResponseBody().close();
                    });
                    return srv;
                }));
                srv.put("start", new NativeFunction((i2, a2) -> { server.start(); return srv; }));
                return srv;
            } catch (Exception e) { return null; }
        }));
    }
}