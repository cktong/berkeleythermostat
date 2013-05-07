class coefficient(self, old, in_intemp, in_outtemp, ac_intemp, ac_outtemp):
   def update():
      # this algorithm will not update the coefficient effectively
      new=old+(ac_intemp-in_intemp)-(ac_outtemp-in_outtemp)
      return new