package com.luminar.nova.parser.ast;
public record IfNode(ExprNode condition, BlockNode thenBranch, Node elseBranch) implements Node {}