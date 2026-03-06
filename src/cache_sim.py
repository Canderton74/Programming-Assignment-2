import sys
import bisect
from collections import deque, OrderedDict, defaultdict


def simulate_fifo(k, requests):
    cache = set()
    queue = deque()
    misses = 0

    for req in requests:
        if req in cache:
            pass
        else:
            misses += 1
            if len(cache) == k:
                evict = queue.popleft()
                cache.remove(evict)
            cache.add(req)
            queue.append(req)

    return misses


def simulate_lru(k, requests):
    cache = OrderedDict()
    misses = 0

    for req in requests:
        if req in cache:
            cache.move_to_end(req)
        else:
            misses += 1
            if len(cache) == k:
                cache.popitem(last=False)
            cache[req] = True

    return misses


def simulate_optff(k, requests):
    n = len(requests)

    occurrences = defaultdict(list)
    for i, req in enumerate(requests):
        occurrences[req].append(i)

    def next_occurrence(item, after_pos):
        occ = occurrences[item]
        idx = bisect.bisect_right(occ, after_pos)
        if idx < len(occ):
            return occ[idx]
        return float('inf')

    cache = set()
    misses = 0

    for i, req in enumerate(requests):
        if req in cache:
            pass
        else:
            misses += 1
            if len(cache) == k:
                evict_item = max(cache, key=lambda x: next_occurrence(x, i))
                cache.remove(evict_item)
            cache.add(req)

    return misses


def main():
    if len(sys.argv) != 2:
        print("Usage: python cache_sim.py <input_file>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        tokens = f.read().split()

    k = int(tokens[0])
    m = int(tokens[1])
    requests = [int(x) for x in tokens[2:2 + m]]

    fifo_misses  = simulate_fifo(k, requests)
    lru_misses   = simulate_lru(k, requests)
    optff_misses = simulate_optff(k, requests)

    print(f"FIFO  : {fifo_misses}")
    print(f"LRU   : {lru_misses}")
    print(f"OPTFF : {optff_misses}")


if __name__ == "__main__":
    main()
