package com.luminar.nova.parser.ast;

import java.util.List;

public record ClassDeclNode(
    String       name,
    String       superclassName,
    List<String> interfaceNames,
    boolean      isAbstract,
    List<VarDeclNode>      fields,
    List<FunctionDeclNode> methods
) implements Node {}