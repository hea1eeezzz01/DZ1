import sys
class SegmentTree:
    def __init__(self, n, a):
        self.n = n
        self.N = 1 << n
        self.tree = [0] * (2 * self.N)
        for i in range(self.N):
            self.tree[self.N + i] = a[i] if i < len(a) else 0
        self._build_tree()
    def _build_tree(self):
        is_or = (self.n % 2 == 1)
        length = self.N
        while length > 1:
            for i in range(length // 2):
                left = self.tree[length + 2 * i]
                right = self.tree[length + 2 * i + 1]
                if is_or:
                    self.tree[length // 2 + i] = left | right
                else:
                    self.tree[length // 2 + i] = left ^ right
            is_or = not is_or
            length //= 2
    def update(self, p, b):
        pos = self.N + p - 1
        self.tree[pos] = b
        pos //= 2
        is_or = True if self.n % 2 == 1 else False
        while pos > 0:
            if is_or:
                self.tree[pos] = self.tree[2 * pos] | self.tree[2 * pos + 1]
            else:
                self.tree[pos] = self.tree[2 * pos] ^ self.tree[2 * pos + 1]
            is_or = not is_or
            pos //= 2
        return self.tree[1]
    def get_root(self):
        return self.tree[1]
def main():
    input = sys.stdin.readline
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    tree = SegmentTree(n, a)
    for _ in range(m):
        p, b = map(int, input().split())
        result = tree.update(p, b)
        print(result)
if __name__ == "__main__":
    main()
