from unittest import TestCase
import importlib.util

# Импорт модуля с именем, начинающимся с цифры
spec = importlib.util.spec_from_file_location("module_339D", "339D.py")
module_339D = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module_339D)
SegmentTree = module_339D.SegmentTree


class TestSegmentTree(TestCase):

    def test_01(self):
        n = 1
        input_list = [5, 3]
        tree = SegmentTree(n, input_list)
        expected_result = 7  # 5 | 3 = 7
        actual_result = tree.get_root()
        self.assertEqual(actual_result, expected_result)

    def test_02(self):
        n = 2
        input_list = [1, 2, 3, 4]
        tree = SegmentTree(n, input_list)
        expected_result = (1 | 2) ^ (3 | 4)  # 3 ^ 7 = 4
        actual_result = tree.get_root()
        self.assertEqual(actual_result, expected_result)

    def test_03(self):
        n = 0
        input_list = [42]
        tree = SegmentTree(n, input_list)
        expected_result = 42
        actual_result = tree.get_root()
        self.assertEqual(actual_result, expected_result)

    def test_04(self):
        n = 2
        input_list = [1, 2, 3, 4]
        tree = SegmentTree(n, input_list)
        expected_result = (1 | 2) ^ (3 | 4)
        actual_result = tree.update(1, 4)
        # После обновления первого элемента на 4: (4|2)^(3|4) = 6^7 = 1
        expected_result = (4 | 2) ^ (3 | 4)
        self.assertEqual(actual_result, expected_result)

    def test_05(self):
        n = 2
        input_list = [1, 2, 3, 4]
        tree = SegmentTree(n, input_list)
        tree.update(1, 4)
        expected_result = (4 | 2) ^ (3 | 4)
        actual_result = tree.update(3, 4)
        # После обновления третьего элемента на 4: (4|2)^(4|4) = 6^4 = 2
        expected_result = (4 | 2) ^ (4 | 4)
        self.assertEqual(actual_result, expected_result)

    def test_06(self):
        n = 2
        input_list = [1, 2, 3, 4]
        tree = SegmentTree(n, input_list)
        expected_result = 4  # Проверяем, что элемент в позиции 1 обновился
        tree.update(1, 4)
        actual_result = tree.tree[tree.N + 0]  # Позиция 1 (1-indexed) = индекс 0 (0-indexed)
        self.assertEqual(actual_result, expected_result)

    def test_07(self):
        n = 2
        input_list = [1, 2, 3, 4]
        tree = SegmentTree(n, input_list)
        initial_root = tree.get_root()
        tree.update(1, 1)  # Обновляем на то же значение
        expected_result = initial_root
        actual_result = tree.get_root()
        self.assertEqual(actual_result, expected_result)

    def test_08(self):
        n = 3
        input_list = [1, 2, 3, 4, 5, 6, 7, 8]
        tree = SegmentTree(n, input_list)
        level2_1 = 1 | 2
        level2_2 = 3 | 4
        level2_3 = 5 | 6
        level2_4 = 7 | 8
        level3_1 = level2_1 ^ level2_2
        level3_2 = level2_3 ^ level2_4
        expected_result = level3_1 | level3_2
        actual_result = tree.get_root()
        self.assertEqual(actual_result, expected_result)

    def test_09(self):
        n = 2
        input_list = [0, 0, 0, 0]
        tree = SegmentTree(n, input_list)
        expected_result = 0
        actual_result = tree.get_root()
        self.assertEqual(actual_result, expected_result)

    def test_10(self):
        n = 2
        input_list = [15, 15, 15, 15]
        tree = SegmentTree(n, input_list)
        expected_result = (15 | 15) ^ (15 | 15)  # 15 ^ 15 = 0
        actual_result = tree.get_root()
        self.assertEqual(actual_result, expected_result)

    def test_11(self):
        n = 1
        input_list = [0, 0]
        tree = SegmentTree(n, input_list)
        expected_result = 0
        actual_result = tree.get_root()
        self.assertEqual(actual_result, expected_result)

    def test_12(self):
        n = 2
        input_list = [1, 2, 3, 4]
        tree = SegmentTree(n, input_list)
        tree.update(1, 4)
        tree.update(3, 4)
        expected_result = (4 | 2) ^ (4 | 4)
        actual_result = tree.update(1, 2)
        # После обновления: (2|2)^(4|4) = 2^4 = 6
        expected_result = (2 | 2) ^ (4 | 4)
        self.assertEqual(actual_result, expected_result)

    def test_13(self):
        n = 0
        input_list = [100]
        tree = SegmentTree(n, input_list)
        expected_result = 100
        actual_result = tree.update(1, 100)
        self.assertEqual(actual_result, expected_result)

    def test_14(self):
        n = 2
        input_list = [1, 2, 3, 4]
        tree = SegmentTree(n, input_list)
        # Проверяем, что листья заполнены правильно
        expected_result = 1
        actual_result = tree.tree[tree.N + 0]
        self.assertEqual(actual_result, expected_result)

    def test_15(self):
        n = 2
        input_list = [1, 2, 3, 4]
        tree = SegmentTree(n, input_list)
        # Проверяем, что листья заполнены правильно
        expected_result = 4
        actual_result = tree.tree[tree.N + 3]
        self.assertEqual(actual_result, expected_result)