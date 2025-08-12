from SimpleLangParser import SimpleLangParser
from SimpleLangVisitor import SimpleLangVisitor
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckVisitor(SimpleLangVisitor):

  def visitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
        return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
    if ctx.op.text == '/':
        if ctx.expr(1).getText() in ["0", "0.0"]:
            raise TypeError("Division by zero is not allowed")

    # Módulo solo entre enteros
    if ctx.op.text == '%':
        if not isinstance(left_type, IntType) or not isinstance(right_type, IntType):
            raise TypeError("Modulo operator is only supported for integers")

    return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def visitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
        return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
    if ctx.op.text == '^':
        if ctx.expr(0).getText().startswith('-') and isinstance(right_type, FloatType):
            raise TypeError("Negative base with non-integer exponent is not allowed")

    return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
  
  def visitInt(self, ctx: SimpleLangParser.IntContext):
    return IntType()

  def visitFloat(self, ctx: SimpleLangParser.FloatContext):
    return FloatType()

  def visitString(self, ctx: SimpleLangParser.StringContext):
    return StringType()

  def visitBool(self, ctx: SimpleLangParser.BoolContext):
    return BoolType()

  def visitParens(self, ctx: SimpleLangParser.ParensContext):
    return self.visit(ctx.expr())
