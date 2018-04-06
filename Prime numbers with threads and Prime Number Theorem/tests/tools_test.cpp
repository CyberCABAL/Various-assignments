#include <cassert>
#include "tools.hpp"
#include <iostream>

using namespace std;

int main() {
  cout << "\nTest input";
  assert(inputData("\nWrite '5': ") == 5);
  cout << "Test success";
  
  cout << "\nTest Prime Number Theorem approximation";
  long approx = primeNT(100);
  assert(approx + approx/3 > 25 && approx - approx/3 < 25);
  cout << "\nTest success";
  
  cout << "\nTest Prime Numbers";
  assert(isPrime(2));
  assert(!isPrime(1));
  assert(isPrime(101));
  assert(!isPrime(169));
  cout << "\nTest success";
}