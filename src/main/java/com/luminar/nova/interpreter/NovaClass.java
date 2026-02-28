package com.luminar.nova.interpreter;

import java.util.List;
import java.util.Map;
import com.luminar.nova.parser.ast.VarDeclNode;

public final class NovaClass implements NovaCallable {
    public  final String              name;
    public  final NovaClass           superclass;
    public  final boolean             isAbstract;
    public  final List<String>        interfaces;
    private final Map<String, NovaCallable> methods;
    private final Map<String, String>    visibilities; // member name → visibility
    private final List<VarDeclNode>      fieldDecls;

    public NovaClass(String name, Map<String, NovaCallable> methods,
                     Map<String, String> visibilities,
                     NovaClass superclass, boolean isAbstract, List<String> interfaces,
                     List<VarDeclNode> fieldDecls) {
        this.name         = name;
        this.methods      = methods;
        this.visibilities = visibilities;
        this.superclass   = superclass;
        this.isAbstract   = isAbstract;
        this.interfaces   = interfaces;
        this.fieldDecls   = fieldDecls;
    }

    public NovaCallable findMethod(String methodName) {
        if (methods.containsKey(methodName)) return methods.get(methodName);
        if (superclass != null) return superclass.findMethod(methodName);
        return null;
    }

    public String getVisibility(String memberName) {
        if (visibilities.containsKey(memberName)) return visibilities.get(memberName);
        if (superclass != null) return superclass.getVisibility(memberName);
        return "public";
    }

    public List<VarDeclNode> getFieldDecls() { return fieldDecls; }

    public boolean isSubclassOf(NovaClass other) {
        NovaClass k = this;
        while (k != null) { if (k == other) return true; k = k.superclass; }
        return false;
    }

    @Override public int arity() {
        NovaCallable init = findMethod("init");
        return init != null ? init.arity() : 0;
    }

    @Override public Object call(Interpreter interp, List<Object> args) {
        if (isAbstract) throw new NovaRuntimeError("Cannot instantiate abstract class '" + name + "'");
        NovaInstance inst = new NovaInstance(this);
        // Initialize fields from fieldDecls
        initializeFields(inst, interp);

        NovaCallable init = findMethod("init");
        if (init != null) {
            interp.thisStack.push(inst);
            try { init.bind(inst).call(interp, args); } finally { interp.thisStack.pop(); }
        }
        return inst;
    }

    private void initializeFields(NovaInstance inst, Interpreter interp) {
        if (superclass != null) superclass.initializeFields(inst, interp);
        for (VarDeclNode field : fieldDecls) {
            Object val = field.initializer() != null ? interp.eval(field.initializer()) : null;
            if (field.typeAnno() != null) val = interp.coerce(field.typeAnno(), val, "field '" + field.name() + "'");
            inst.set(field.name(), val);
        }
    }

    @Override public String toString() { return "<class " + name + ">"; }
}