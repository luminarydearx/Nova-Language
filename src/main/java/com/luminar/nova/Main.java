package com.luminar.nova;

import com.luminar.nova.cli.CommandDispatcher;
import com.luminar.nova.cli.NovaConsole;

public final class Main {
    public static void main(String[] args) {
        if (args.length == 0) {
            NovaConsole.printLogo();
            NovaConsole.info("Run " + NovaConsole.cyan("nova help") + " to see all commands.");
            System.exit(0);
        }
        String   command = args[0];
        String[] rest    = new String[args.length - 1];
        System.arraycopy(args, 1, rest, 0, rest.length);
        System.exit(CommandDispatcher.dispatch(command, rest));
    }
}