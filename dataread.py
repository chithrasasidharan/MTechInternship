import pickle
infile = open('datas','rb')

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
 
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
 
class RSA():
    def __init__(self, p=61, q=53, useConstantE=False):
        self.p = p
        self.q = q
        self.n = self.p * self.q
        self.tot = (self.p - 1 ) * (self.q - 1)
        if useConstantE:
            self.e = 17 if 17 < self.tot else 5
        else:
            es = [3,5,17,257,65537]
            self.e = [x for x in es if x<self.tot][-1]
        self.d = modinv(self.e, self.tot)
 
    def encrypt(self, msg):
        # encrypt with public key
        enc = []
        for c in msg:
            c = ord(c)
            enc.append(c**self.e%self.n)
        self.enc = enc
        return enc
    
    def decrypt(self, msg, d=None):
        # decrypt with private key
        if d is None:
            d = self.d
        dec = []
        for c in msg:
            dec.append(unichr(c**d%self.n))
        return ''.join(dec)
    
    def breakRSA(self, enc):
        # public key is n and e, we can use this information
        # find p
        if self.n%2==0:
            p = 2
        else:
            for i in primes:
                if self.n%i == 0:
                    p = i
        q = self.n / p
        d = modinv(self.e, (p - 1) * (q-1))
        return self.decrypt(enc, d)
    
    def time(self, plain):
        et1 = time.time()
        enc = self.encrypt(plain)
        et2 = time.time()
        dt1 = time.time()
        dec = self.breakRSA(enc)
        dt2 = time.time()
        et=et2-et1

        dt=dt2-dt1

        times = dt/et
        self.dt = dt
        self.et = et
        self.times = times
        return times
    
    def averageTime(self, plain, noOfTimes=10):
        times = []
        for x in range(noOfTimes):
            times.append(self.time(plain))
        self.avg = sum(times)/float(len(times))
        return sum(times) / float(len(times))
 
 
 
f = open("demo","r")
for x in f:
    x = x.rstrip('\n')
    print(x)
