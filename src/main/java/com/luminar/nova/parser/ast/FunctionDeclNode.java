package com.luminar.nova.parser.ast;

import java.util.List;

/**
 * [public|private|protected] [abstract] func name(params): returnType { body }
 *
 * visibility    : "public" | "private" | "protected"  (default "public")
 * isAbstract    : true → no body (body is null), used inside abstract classes
 * paramTypes    : type annotation per param, may contain null for untyped params
 * returnType    : return type annotation, null = untyped / void
 * body          : null for abstract methods
 */
public record FunctionDeclNode(
    String       visibility,
    boolean      isAbstract,
    String       name,
    List<String> params,
    List<String> paramTypes,
    String       returnType,
    BlockNode    body
) implements Node {}