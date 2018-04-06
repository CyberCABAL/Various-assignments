#include <iostream>
#include <string>
#include <cmath>

using namespace std;

long inputData(string desc) {
  cout << desc;
  long result;
  cin >> result;
  return result;
}

long primeNT(long n) {// Prime number theorem approximation.
  return n / (log(n) - 1);
}// Li(x) ?

bool isPrime(long value) {// (n+2)*(n+2) = n²+4n + 4
  if (value < 2) {return false;}
  if (value == 2 || value == 3) {return true;}
  if ((value % 2) == 0) {return false;}
  for (long n = 3, nn = 9; nn <= value; n += 2) {
    if (value % n == 0) {return false;}
    nn += 4 * n + 4;
  }
  return true;
}