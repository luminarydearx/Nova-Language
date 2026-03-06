package com.luminar.nova.parser.ast;

import java.util.List;

/** Method signature inside an interface (no body). */
public record InterfaceMethodSig(String name, List<String> params, String returnType) {}