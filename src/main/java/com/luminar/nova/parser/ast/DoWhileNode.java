package com.luminar.nova.parser.ast;

/**
 * do { body } while (condition);
 */
public record DoWhileNode(BlockNode body, ExprNode condition) implements Node {}