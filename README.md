# Top-K-LARA-NRA-

Implementation of Top-K query with LARA and NRA algorithm. The files are the stats from the NBA 2017 season. For any player a score is computed based on the stats the query is about. The program has 2 phases (growing and shrinking). In the first phase the candidates are located with LARA algorithm. Then, in the second phase, the top-K are located with NRA algorithm. The correctness of the result is tested using a naive approch for computing the query.  
