def updatecoeff(oldcoeff, intemp, outtemp):
   # this algorithm will not update the coefficient effectively
   new=.9*oldcoeff+.1*(outtemp-intemp)
   print .1*(outtemp-intemp)
   return new
   
