class Player:
   def __init__( self, name="None", age=0, ranking=0, hand="None", backhand="None"):
       self.name = name
       self.age = age
       self.ranking = ranking
       self.hand = hand
       self.backhand = backhand
   
   def __del__(self):
       class_name = self.__class__.__name__
   
   def setName(self,name):
       Player.name = name
       
   def setAge(self,age):
       Player.age = age

   def setRanking(self,ranking):
       Player.ranking = ranking

   def setHand(self,hand):
       Player.hand = hand

   def setBackhand(self,hand):
       Player.backhand =backhand
