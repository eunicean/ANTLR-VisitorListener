from SimpleLangListener import SimpleLangListener
from SimpleLangParser import SimpleLangParser
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckListener(SimpleLangListener):

  def __init__(self):
    self.errors = []
    self.types = {}

  def enterMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    pass

  def exitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(f"Unsupported operand types for * or /: {left_type} and {right_type}")
    if ctx.op.text == '/':
            if ctx.expr(1).getText() in ["0", "0.0"]:
                self.errors.append("Division by zero is not allowed")
    if ctx.op.text == '%':
            if not (isinstance(left_type, IntType) and isinstance(right_type, IntType)):
                self.errors.append("Mod operator is only supported for integers")
    self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def enterAddSub(self, ctx: SimpleLangParser.AddSubContext):
    pass

  def exitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(f"Unsupported operand types for + or -: {left_type} and {right_type}")
    if ctx.op.text == '^':
        if ctx.expr(0).getText().startswith('-') and isinstance(right_type, FloatType):
            self.errors.append("Negative base with non-integer exponent is not allowed")
    self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def exitUnaryMinus(self, ctx: SimpleLangParser.UnaryMinusContext):
    expr_type = self.types.get(ctx.expr())
    if not isinstance(expr_type, (IntType, FloatType)):
        self.errors.append(f"Unary minus not supported for type {expr_type}")
    self.types[ctx] = expr_type

  def visitUnaryMinus(self, ctx: SimpleLangParser.UnaryMinusContext):
    expr_type = self.visit(ctx.expr())
    if not isinstance(expr_type, (IntType, FloatType)):
        raise TypeError(f"Unary minus not supported for type {expr_type}")
    return expr_type

  def enterInt(self, ctx: SimpleLangParser.IntContext):
    self.types[ctx] = IntType()

  def enterFloat(self, ctx: SimpleLangParser.FloatContext):
    self.types[ctx] = FloatType()

  def enterString(self, ctx: SimpleLangParser.StringContext):
    self.types[ctx] = StringType()

  def enterBool(self, ctx: SimpleLangParser.BoolContext):
    self.types[ctx] = BoolType()

  def enterParens(self, ctx: SimpleLangParser.ParensContext):
    pass

  def exitParens(self, ctx: SimpleLangParser.ParensContext):
    self.types[ctx] = self.types[ctx.expr()]

  def is_valid_arithmetic_operation(self, left_type, right_type):
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
      return True
    return False
