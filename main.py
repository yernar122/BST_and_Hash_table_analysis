import random
from statistics import median
from time import perf_counter


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
            return
        current = self.root
        while True:
            if key == current.key:
                return
            if key < current.key:
                if current.left is None:
                    current.left = Node(key)
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(key)
                    return
                current = current.right

    def search(self, key):
        current = self.root
        while current is not None:
            if key == current.key:
                return True
            current = current.left if key < current.key else current.right
        return False

    def delete(self, key):
        parent, current = None, self.root
        while current is not None and current.key != key:
            parent = current
            current = current.left if key < current.key else current.right
        if current is None:
            return False

        if current.left is not None and current.right is not None:
            successor_parent, successor = current, current.right
            while successor.left is not None:
                successor_parent, successor = successor, successor.left
            current.key = successor.key
            parent, current = successor_parent, successor

        child = current.left if current.left is not None else current.right
        if parent is None:
            self.root = child
        elif parent.left is current:
            parent.left = child
        else:
            parent.right = child
        return True


class HashTable:
    def __init__(self, capacity):
        self.buckets = [[] for _ in range(capacity)]

    def insert(self, key):
        bucket = self.buckets[key % len(self.buckets)]
        if key not in bucket:
            bucket.append(key)

    def search(self, key):
        return key in self.buckets[key % len(self.buckets)]

    def delete(self, key):
        bucket = self.buckets[key % len(self.buckets)]
        if key not in bucket:
            return False
        bucket.remove(key)
        return True


def test_correctness():
    for structure in (BST(), HashTable(3)):
        for key in (5, 3, 7, 2, 4, 6, 8, 7):
            structure.insert(key)
        assert all(structure.search(key) for key in range(2, 9))
        assert not structure.search(100)
        for key in (2, 3, 5, 7, 4, 6, 8):
            assert structure.delete(key)
            assert not structure.search(key)
        assert not structure.delete(5)


def measure(factory, operation, keys, repeats=7):
    times = []
    for _ in range(repeats):
        structure = factory()
        if operation != "insert":
            for key in keys:
                structure.insert(key)
        action = getattr(structure, operation)
        start = perf_counter()
        for key in keys:
            action(key)
        times.append((perf_counter() - start) * 1000)
    return median(times)



def main():
    test_correctness()
    rng = random.Random(42)

    results = [
        "# Actual benchmark results (milliseconds)",
        "# Median of 7 runs; n operations per cell; lower is better.",
        "Elements | Structure | Insert (ms) | Search (ms) | Delete (ms)",
        "---------|-----------|-------------|-------------|------------"
    ]

    for n in (100, 1_000, 10_000):
        keys = rng.sample(range(100_000_000), n)

        for name, factory in (
            ("BST", BST), ("Hash Table", lambda n=n: HashTable(2 * n + 1))
        ):
            times = [
                measure(factory, operation, keys)
                for operation in ("insert", "search", "delete")
            ]

            results.append(
                f"{n:,} | {name} | "  + " | ".join(f"{t:.4f}" for t in times)
            )

    print("\n".join(results))


if __name__ == "__main__":
    main()
