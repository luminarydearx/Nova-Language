package com.luminar.nova.parser.ast;

import java.util.List;

/**
 * enum Name { VALUE1, VALUE2, VALUE3 }
 */
public record EnumDeclNode(String name, List<String> values) implements Node {}