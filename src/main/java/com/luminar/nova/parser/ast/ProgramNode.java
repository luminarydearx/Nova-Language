package com.luminar.nova.parser.ast;
import java.util.List;
public record ProgramNode(List<Node> statements) implements Node {}