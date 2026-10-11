# BST vs Hash Table: Performance Comparison

Yernar Kuanyshbek

## Objective

Implement an **ordinary (unbalanced) Binary Search Tree (BST)** and a **Hash Table**, then compare how long it takes to insert, search for, and delete 100, 1,000, and 10,000 integers.

## Implementation

**BST:** Every node stores one integer and references to its left and right children. Smaller values go left, larger values go right. Duplicate keys are ignored. Deletion handles (1) a leaf, (2) a node with one child, and (3) a node with two children (replace its key with the in-order successor). The tree **does not rebalance itself**.

**Hash Table:** Uses `key % capacity` to select a bucket. Each bucket is a Python list (**separate chaining**) so different keys can share an index. Duplicate keys are ignored. The capacity is fixed when the table is created; **there is no automatic resizing**.

Both structures implement `insert(key)`, `search(key)`, and `delete(key)`. Search returns a Boolean, and delete returns whether the key was found.

## Time complexity

Here `n` is the number of stored keys. “Average” for the BST assumes a reasonably balanced shape; for the Hash Table it assumes a good distribution of keys and a controlled load factor.

| Operation | BST best | BST average (balanced shape) | BST worst (skewed) | Hash best | Hash average | Hash worst |
|---|---|---|---|---|---|---|
| Insert | O(1) | O(log n) | O(n) | O(1) | O(1) | O(n) |
| Search | O(1) | O(log n) | O(n) | O(1) | O(1) | O(n) |
| Delete | O(1) | O(log n) | O(n) | O(1) | O(1) | O(n) |

**Why?** A BST visits one node per level. If it is balanced, its height grows approximately as `log n`; inserting already-sorted values can make it a chain of height `n`. A Hash Table normally goes directly to one bucket, but a large number of collisions can force a linear scan of up to `n` keys. Our Hash Table checks for duplicates during insertion, so insertion can also be O(n) in the worst case.

Space complexity: **O(n)** for the BST; **O(n + m)** for the Hash Table with `m` buckets. In this experiment `m = 2n + 1`, so both use **O(n)** space.

## Experimental method

1. Use the same unique, randomly ordered integers for both structures, generated with a fixed random seed (`42`).
2. Test `n = 100`, `1,000`, and `10,000`.
3. For insertion, create an empty structure, then insert all `n` keys.
4. For searching, first populate a new structure, then search for all `n` existing keys.
5. For deletion, first populate a new structure, then delete all `n` keys.
6. Repeat each timed operation **7 times**, taking the **median** total time in milliseconds (`time.perf_counter()`). Both structures use exactly the same keys and operation order.
7. Create the data and initialize each structure **outside** the timed section. The Hash Table has `2n + 1` buckets for each experiment. This avoids timing table allocation, but means the reported times are **operation times, not complete setup-to-finish times**.

`main.py` runs a short correctness check before the benchmark. The implementation uses Python 3 and only the standard library.

## Results

The following are actual measurements from one run using **Python 3.13.5**. Each table entry is the **total time for `n` operations**, not the time of one operation. Lower is faster; times will vary by computer.

| Elements | Structure | Insert (ms) | Search (ms) | Delete (ms) |
|---:|-----------|------------:|------------:|------------:|
| 100 | BST       |      0.0431 |      0.0343 |      0.0428 |
| 100 | Hash Table |      0.0168 |      0.0124 |      0.0176 |
| 1,000 | BST       |      0.6727 |      0.5831 |      0.6470 |
| 1,000 | Hash Table |      0.1394 |      0.0981 |      0.1392 |
| 10,000 | BST       |     10.1608 |      7.6975 |      8.5219 |
| 10,000 | Hash Table |      1.6086 |      1.1747 |      1.5938 |

The current output from the benchmark is also saved in [`results.png`](results.png).

## Discussion and conclusion

In these tests, the Hash Table completed all three operations faster. The largest difference comes from how each structure finds a key: the BST compares values while traveling from node to node, but the Hash Table uses an index calculated from the key. The randomized insertion order generally prevents the BST from becoming a long sorted chain, but the tree still needs multiple comparisons.

In practice, performance also depends on the input order, tree height, number of hash collisions, bucket count, cache behavior, memory allocation, and Python interpreter overhead. These measurements are specific to this implementation and test setup, not a guarantee for every BST or Hash Table.

**Conclusion:** A Hash Table is usually a good choice for quick exact-key lookups and updates. A BST is useful when **sorted order or range queries** matter; a self-balancing BST such as an AVL or red-black tree can guarantee O(log n) worst-case search, insert, and delete. This assignment implements neither self-balancing nor hash-table resizing.
