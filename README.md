# Programming Assignment 2

## Student Info

Cole Anderton: 1429-5810
## How to Run

Make sure to be using Python 3.6 or higher.

In the base directory (./Programming-Assignment-2/), run:
```
python src/cache_sim.py <input_file>
```

### Example

```
python src/cache_sim.py data/example.in
```

Expected output to the terminal (this will matche `data/example.out`):

```
FIFO  : 10
LRU   : 10
OPTFF : 6
```


## Input Format

```
k m
r1 r2 r3 ... rm
```

k = cache capacity
m = number of requests
r1 ... rm = sequence of integer item IDs



## Output Format

```
FIFO  : <misses>
LRU   : <misses>
OPTFF : <misses>
```


## Assumptions

- Input: k >= 1, m >= 1, with exactly integer IDs follow on the second line.
- Item IDs are positive integers.
- All tokens may be separated by spaces or newlines.

---

## Written Component

### Question 1: Empirical Comparison

Results across three nontrivial input files (each with 50+ requests):

| Input File  | k | m  | FIFO | LRU | OPTFF |
|-------------|---|----|------|-----|-------|
| `input1.in` | 4 | 60 | 40   | 40  | 19    |
| `input2.in` | 3 | 60 | 50   | 50  | 29    |
| `input3.in` | 5 | 75 | 25   | 15  | 12    |

**Does OPTFF have the fewest misses?**

Yes, OPTFF had the fewest misses every time. It knows the full request sequence ahead of time so
it always evicts the item needed farthest in the future, which is the best possible choice.

**How does FIFO compare to LRU?**

For input1 and input2 they got the same number of misses since both policies thrash on cyclic
patterns. For input3 LRU did better (15 vs 25 misses) because it keeps recently used items
around, while FIFO just evicts whatever was inserted first regardless of how often it gets used.


### Question 2: Bad Sequence for FIFO and LRU

For k=3, the sequence 1 2 3 4 1 2 3 4 1 2 gives:

| Policy | Misses |
|--------|--------|
| FIFO   | 10     |
| LRU    | 10     |
| OPTFF  | 6      |

FIFO and LRU both miss every single request because the sequence cycles through k+1=4 distinct
items, which causes them to always evict whatever gets requested next. OPTFF avoids this by
looking ahead and evicting item 3 on the first conflict (since its next use is farthest out),
keeping 1 and 2 in cache to hit on requests 5 and 6. It ends up with 4 hits total instead of 0.


### Question 3: Proof That OPTFF Is Optimal

We use an exchange argument. Let A be any offline algorithm and let t be the first step where A
and OPTFF make different eviction choices. Since they agreed on everything before t, they have the
same cache contents C at step t. Both miss on request r_t and must evict something.

OPTFF evicts e*, the item in C whose next occurrence is farthest in the future. A evicts some
other item e, where next(e) = l and next(e*) = j, and by OPTFF's choice j >= l.

Modify A to evict e* instead of e at step t, calling this A'. Now A' has e in cache but not e*,
while A has e* but not e. Between t+1 and l-1 neither item appears, so both algorithms behave
identically. At step l, A misses on e (it evicted it) while A' hits. A' avoids that miss entirely.

After step l, A inserts e back and evicts some new item e''. At this point the caches differ by
e* vs e'', and we can apply the same argument again. Each swap either saves a miss outright (if
e* is never requested again) or defers a potential miss to a later time (since j >= l). Either
way the total miss count for A' never exceeds that of A.

Repeating this across every divergence point transforms A into OPTFF without increasing misses,
so misses(OPTFF) <= misses(A) for any offline algorithm A. ∎
