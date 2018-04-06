#include <iostream>
#include <thread>
#include <vector>
#include "tools.hpp"

long threadAmount, startInt, endInt;

using namespace std;

int main() {
  threadAmount = inputData("Threads: ");
  startInt = inputData("Start: ");
  if (startInt < 2) {startInt = 2;}
  endInt = inputData("End: ");
  if (endInt < startInt) {return 0;}
  
  long delta = endInt - startInt, smallDelta = delta / threadAmount;
  long r = (delta % threadAmount) + 1;
  
  vector<vector<long>> results(threadAmount);
  vector<thread> threads;
  for (int i = 0; i < threadAmount; i++) {
    threads.emplace_back([i, smallDelta, r, &results] {
      long s = startInt + i * smallDelta, e = s + smallDelta;
      if (i < r) {e += i;}
      if (i < (r + 1) && i > 0) {s += i;}
      if (i == threadAmount - 1) {e = endInt;}
      
      vector<long> found;
      found.reserve(primeNT(e) - primeNT(s));
      for (long j = s; j <= e; j++) {
        if (isPrime(j)) {found.emplace_back(j);}
      }// Sieve of Eratosthenes?
      results[i]=move(found);
    });
  }
  for (auto &t : threads) {t.join();}
  cout << "\nResults:" << endl;
  int i = 0;
  for (auto &t : results) {
    cout << "\nThread " << i << ":" << endl;
    for (auto &prime : t) {cout << prime << ", " << endl;}
    i++;
  }
  cout << endl;
  return 0;
}