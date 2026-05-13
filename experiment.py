import time
import pandas as pd
from shamir import ShamirSecretSharing
from feldman import FeldmanVSS
from simulator import Attacker


def run_honest_experiment(n, t, prime=10007, secret=1234, iterations=5000):
   sss = ShamirSecretSharing(prime)
   fss = FeldmanVSS(prime)

   shamir_ok = 0
   feldman_ok = 0

   for _ in range(iterations):
       shares, _ = sss.generate_shares(secret, n, t)
       if sss.recover_secret(shares[:t], t) == secret:
           shamir_ok += 1

       shares, com = fss.generate_shares(secret, n, t)

       try:
           recovered = fss.recover_verified(shares, com, t) 
           if recovered == secret:
               feldman_ok += 1
       except ValueError:
           pass

   return {
       "shamir_correct_%": shamir_ok / iterations * 100,
       "feldman_correct_%": feldman_ok / iterations * 100
   }


def run_attack_experiment(n, t, attack_type, prime=10007, secret=1234, iterations=5000):
   sss = ShamirSecretSharing(prime)
   fss = FeldmanVSS(prime)
   attacker = Attacker(attack_type)

   shamir_broken = 0
   feldman_detect = 0

   for _ in range(iterations):
       shares, com = fss.generate_shares(secret, n, t)

       if attack_type != "noop":
           shares[0] = attacker.substitute_share(shares[0], prime)

       if sss.recover_secret(shares[:t], t) != secret:
           shamir_broken += 1

       try:
           fss.recover_verified(shares, com, t)
           detected = False
       except ValueError:
           detected = True

           if attack_type != "noop" and detected:
               feldman_detect += 1

   return {
       "attack": attack_type,
       "shamir_broken_%": shamir_broken / iterations * 100,
       "feldman_detect_%": feldman_detect / iterations * 100
   }
