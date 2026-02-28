package com.luminar.nova.parser.ast;
/** 
 * var / const declaration with optional type annotation.
 * visibility: "public" | "private" | "protected"
 */
public record VarDeclNode(
    String   visibility,
    String   name, 
    boolean  isConst, 
    String   typeAnno, 
    ExprNode initializer
) implements Node {}