package com.luminar.nova.parser.ast;

import java.util.List;

/**
 * struct Name {
 *     field1: Type;
 *     field2: Type;
 * }
 * Auto-generates an init(field1, field2, ...) constructor.
 */
public record StructDeclNode(String name, List<StructField> fields) implements Node {}