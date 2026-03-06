package com.luminar.nova.parser.ast;

/**
 * try { tryBlock }
 * catch (catchVar) { catchBlock }
 * finally { finallyBlock }
 *
 * catchVar, catchBlock, and finallyBlock may all be null.
 */
public record TryCatchNode(
    BlockNode tryBlock,
    String    catchVar,
    BlockNode catchBlock,
    BlockNode finallyBlock
) implements Node {}