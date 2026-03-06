package com.luminar.nova.parser.ast;

/** A single field declaration inside a struct: name: type */
public record StructField(String name, String type) {}