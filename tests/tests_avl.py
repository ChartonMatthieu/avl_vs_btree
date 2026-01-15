from src.avl_tree import AVLTree

def test_avl_insert_search():
    avl = AVLTree()
    vals = [3, 1, 4, 2]
    for v in vals:
        avl.insert(v)
    for v in vals:
        assert avl.search(v)
