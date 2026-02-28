package com.luminar.nova.parser.ast;



public sealed interface Node permits
    ProgramNode, PrintNode, VarDeclNode,
    ExprStmtNode, BlockNode, FunctionDeclNode, ClassDeclNode, InterfaceDeclNode,
    EnumDeclNode, StructDeclNode,
    ReturnNode, IfNode, WhileNode, DoWhileNode, ForNode, BreakNode, ContinueNode,
    TryCatchNode, ThrowNode {}