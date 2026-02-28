package com.luminar.nova.parser.ast;

import java.util.List;

/**
 * interface Name [extends OtherIface, ...] {
 *     func method(params): ReturnType;
 * }
 */
public record InterfaceDeclNode(
    String                  name,
    List<String>            parentInterfaces,
    List<InterfaceMethodSig> methods
) implements Node {}