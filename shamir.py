import random

class ShamirSecretSharing:
   def __init__(self, prime=10007):
       self.prime = prime

   def _random_polynomial(self, secret, threshold):
       return [secret] + [random.randint(1, self.prime // 2) for _ in range(threshold - 1)]

   def _evaluate_polynomial(self, coeffs, x):
       result = 0
       for i, c in enumerate(coeffs):
           result = (result + c * pow(x, i, self.prime)) % self.prime
       return result

   def generate_shares(self, secret, n, threshold):
       coeffs = self._random_polynomial(secret, threshold)
       shares = [(i, self._evaluate_polynomial(coeffs, i)) for i in range(1, n + 1)]
       return shares, coeffs

   def recover_secret(self, shares, threshold):
       if len(shares) < threshold:
           raise ValueError("Недостаточно долей")

       shares = shares[:threshold]
       secret = 0

       for j in range(threshold):
           xj, yj = shares[j]
           num, den = 1, 1

           for m in range(threshold):
               if m != j:
                   xm, _ = shares[m]
                   num = (num * (-xm)) % self.prime
                   den = (den * (xj - xm)) % self.prime

           inv = pow(den, self.prime - 2, self.prime)
           lj = (num * inv) % self.prime
           secret = (secret + yj * lj) % self.prime

       return secret
