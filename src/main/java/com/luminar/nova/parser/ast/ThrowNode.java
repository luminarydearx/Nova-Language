package com.luminar.nova.parser.ast;

/**
 * throw expression;
 */
public record ThrowNode(ExprNode value) implements Node {}