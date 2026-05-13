from shamir import ShamirSecretSharing

class FeldmanVSS:
   def __init__(self, prime=10007, generator=5):
       self.prime = prime
       self.generator = generator

   def generate_commitments(self, coeffs):
       return [pow(self.generator, c, self.prime) for c in coeffs]

   def generate_shares(self, secret, n, threshold):
       sss = ShamirSecretSharing(self.prime)
       shares, coeffs = sss.generate_shares(secret, n, threshold)
       commitments = self.generate_commitments(coeffs)
       return shares, commitments

   def verify_share(self, share, commitments, threshold):
       x, y = share

       left = pow(self.generator, y, self.prime)

       right = 1
       for k, C in enumerate(commitments[:threshold]):
           exp = pow(x, k, self.prime - 1)
           right = (right * pow(C, exp, self.prime)) % self.prime

       return left == right

   def recover_verified(self, shares, commitments, threshold):
       valid_shares = []

       for share in shares:
           if self.verify_share(share, commitments, threshold):
               valid_shares.append(share)
           else:
               print(f"[!] Подозрительная доля отброшена: {share}")

       if len(valid_shares) < threshold:
           raise ValueError("Недостаточно корректных долей для восстановления")

       sss = ShamirSecretSharing(self.prime)
       return sss.recover_secret(valid_shares, threshold)
