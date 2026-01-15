import time
import tracemalloc
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from src.avl_tree import AVLTree
from src.b_tree import BTree

# ---------------- CONFIG ----------------

DATASET_SIZES = [1000, 5000, 10000, 50000]
BTREE_T_VALUES = [2, 3, 5]

# ---------------------------------------


def load_dataset(size):
    """
    Load dataset from data/data_<size>.txt
    Must be executed from project root.
    """
    path = os.path.join(os.getcwd(), "data", f"data_{size}.txt")

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            "Run: python src/datasets.py first."
        )

    with open(path, encoding="utf-8") as f:
        return [int(line.strip()) for line in f if line.strip()]


# ---------------- MEASURE ----------------

def measure_insert(structure, values):
    tracemalloc.start()
    start = time.perf_counter()

    for v in values:
        structure.insert(v)

    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return elapsed, peak / 1024  # time (s), memory (KB)


def measure_search(structure, values):
    start = time.perf_counter()

    for v in values:
        structure.search(v)

    return time.perf_counter() - start


def measure_delete_avl(avl, values):
    """
    Delete half of the elements (AVL only)
    """
    to_delete = values[:len(values)//2]

    start = time.perf_counter()
    for v in to_delete:
        avl.delete(v)

    return time.perf_counter() - start


# ---------------- RUN ----------------

def benchmark_avl(values):
    avl = AVLTree()

    insert_t, mem = measure_insert(avl, values)
    search_t = measure_search(avl, values)
    delete_t = measure_delete_avl(avl, values)

    return insert_t, search_t, delete_t, mem


def benchmark_btree(values, t):
    btree = BTree(t=t)

    insert_t, mem = measure_insert(btree, values)
    search_t = measure_search(btree, values)

    return insert_t, search_t, mem


def run():
    print("\n====== BENCHMARK RESULTS ======\n")

    for size in DATASET_SIZES:
        print(f"\n--- Dataset size: {size} ---")

        values = load_dataset(size)

        # AVL
        avl_insert, avl_search, avl_delete, avl_mem = benchmark_avl(values)

        print("\nAVL Tree")
        print(f"Insert time : {avl_insert:.4f} s")
        print(f"Search time : {avl_search:.4f} s")
        print(f"Delete time : {avl_delete:.4f} s")
        print(f"Memory peak: {avl_mem:.2f} KB")

        # B-Trees
        for t in BTREE_T_VALUES:
            b_insert, b_search, b_mem = benchmark_btree(values, t)

            print(f"\nB-Tree (t={t}, m={2*t})")
            print(f"Insert time : {b_insert:.4f} s")
            print(f"Search time : {b_search:.4f} s")
            print(f"Memory peak: {b_mem:.2f} KB")


if __name__ == "__main__":
    run()
