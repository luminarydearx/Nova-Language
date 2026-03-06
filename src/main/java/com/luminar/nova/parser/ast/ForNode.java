package com.luminar.nova.parser.ast;
public record ForNode(String varName, ExprNode iterable, BlockNode body) implements Node {}