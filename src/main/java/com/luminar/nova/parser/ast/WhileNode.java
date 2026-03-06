package com.luminar.nova.parser.ast;
public record WhileNode(ExprNode condition, BlockNode body) implements Node {}