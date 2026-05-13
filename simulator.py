import random


class Attacker:
   def __init__(self, attack_type='random'):
       self.attack_type = attack_type

   def substitute_share(self, share, prime):
       x, y = share

       if self.attack_type == 'random':
           return (x, random.randint(0, prime - 1))
       elif self.attack_type == 'zero':
           return (x, 0)
       elif self.attack_type == 'increment':
           return (x, (y + 1) % prime)
       elif self.attack_type == 'noop':
           # Не меняем долю вообще
           return share

       # На всякий случай fallback
       return share

