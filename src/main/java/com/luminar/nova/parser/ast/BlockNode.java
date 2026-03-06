package com.luminar.nova.parser.ast;
import java.util.List;
public record BlockNode(List<Node> statements) implements Node {}