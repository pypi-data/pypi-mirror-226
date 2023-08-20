import numpy as np
import math

class complex:
  def __init__(self, a, bi):
    self.a = a
    self.bi = bi

  def conjugate(self):
    return np.array([self.a, -self.bi])

  def mod(self):
    return math.sqrt(self.a ** 2 + self.bi ** 2)

  def arg(self):
    return math.atan(self.bi/self.a)

def cmultiply(num1, num2):
  a = -(num1[1]*num2[1]) + num1[0]*num2[0]
  bi = num1[1]*num2[0] + num1[0]*num2[1]
  return np.array([a, bi])