import random
import os
import sys

random.seed(42)
SIZES = [1000, 5000, 10000, 50000]

def project_root_from_cwd():
    """
    We expect to run this script from the project root.
    It must contain a 'src' directory.
    """
    cwd = os.getcwd()
    if not os.path.isdir(os.path.join(cwd, "src")):
        print("ERROR: Please run this script from the project root (the folder that contains 'src').")
        print("Example:")
        print("  cd path\\to\\avl-vs-btree")
        print("  python src\\datasets.py")
        sys.exit(1)
    return cwd

def generate(size):
    return random.sample(range(size * 10), size)

if __name__ == "__main__":
    root = project_root_from_cwd()
    data_dir = os.path.join(root, "data")
    os.makedirs(data_dir, exist_ok=True)

    for s in SIZES:
        data = generate(s)
        path = os.path.join(data_dir, f"data_{s}.txt")
        with open(path, "w", encoding="utf-8") as f:
            for v in data:
                f.write(f"{v}\n")

    print(f"Datasets generated successfully in: {data_dir}")
