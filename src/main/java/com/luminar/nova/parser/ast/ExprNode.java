package com.luminar.nova.parser.ast;

import java.util.List;
import java.util.Map;

public sealed interface ExprNode permits
    ExprNode.Lit, ExprNode.Id, ExprNode.Binary, ExprNode.Unary, ExprNode.Grouping,
    ExprNode.Call, ExprNode.ArrayLit, ExprNode.ObjLit,
    ExprNode.IndexGet, ExprNode.MemberGet,
    ExprNode.IndexSet, ExprNode.MemberSet,
    ExprNode.CmpIdSet, ExprNode.CmpMemberSet, ExprNode.CmpIndexSet,
    ExprNode.Postfix, ExprNode.Prefix,
    ExprNode.NewExpr, ExprNode.ThisExpr, ExprNode.SuperCall,
    ExprNode.Ternary, ExprNode.Await, ExprNode.FuncExpr, ExprNode.Match
{
    record Lit(Object value)                                                    implements ExprNode {}
    record Id(String name)                                                      implements ExprNode {}
    record Binary(ExprNode left, String op, ExprNode right)                     implements ExprNode {}
    record Unary(String op, ExprNode operand)                                   implements ExprNode {}
    record Grouping(ExprNode expr)                                              implements ExprNode {}
    record Call(ExprNode callee, List<ExprNode> args)                           implements ExprNode {}
    record ArrayLit(List<ExprNode> elements)                                    implements ExprNode {}
    record ObjLit(List<Map.Entry<String,ExprNode>> entries)                     implements ExprNode {}
    record IndexGet(ExprNode obj, ExprNode index)                               implements ExprNode {}
    record MemberGet(ExprNode obj, String member)                               implements ExprNode {}
    record IndexSet(ExprNode obj, ExprNode index, ExprNode value)               implements ExprNode {}
    record MemberSet(ExprNode obj, String member, ExprNode value)               implements ExprNode {}
    /** name += value */
    record CmpIdSet(String name, String op, ExprNode value)                     implements ExprNode {}
    /** obj.member += value */
    record CmpMemberSet(ExprNode obj, String member, String op, ExprNode value) implements ExprNode {}
    /** arr[i] += value */
    record CmpIndexSet(ExprNode obj, ExprNode index, String op, ExprNode value) implements ExprNode {}
    /** expr++ / expr-- */
    record Postfix(ExprNode operand, String op)                                 implements ExprNode {}
    /** ++expr / --expr */
    record Prefix(String op, ExprNode operand)                                  implements ExprNode {}
    /** new ClassName(args) */
    record NewExpr(String className, List<ExprNode> args)                       implements ExprNode {}
    /** this */
    record ThisExpr()                                                           implements ExprNode {}
    /** super.method(args) */
    record SuperCall(String method, List<ExprNode> args)                        implements ExprNode {}
    /** cond ? then : else */
    record Ternary(ExprNode condition, ExprNode thenExpr, ExprNode elseExpr)     implements ExprNode {}
    /** await expr */
    record Await(ExprNode expr)                                                 implements ExprNode {}
    /** func(params) { body } */
    record FuncExpr(List<String> params, List<String> paramTypes, String returnType, BlockNode body) implements ExprNode {}
    record Match(ExprNode expr, List<Map.Entry<ExprNode, ExprNode>> arms, ExprNode defaultArm) implements ExprNode {}
}