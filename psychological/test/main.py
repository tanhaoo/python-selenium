# This is a sample Python script.
from typing import List

from lxml import etree
import requests


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def test1(prerequisites: List[List[int]]):
    preMap = {i: [] for i in range(5)}
    for crs, pre in prerequisites:
        print(str(crs) + " " + str(pre))
        preMap[crs].append(pre)
    print(preMap)


def test2(words: List[str]):
    adj = {c: set() for w in words for c in w}
    print(adj)
    for i in adj:
        print(i)
        adj[i].add('w')
        adj[i].add('1')
        adj[i].add('2')
        print(adj)
        for j in adj[i]:
            print(i + " " + j)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test1([[1, 2], [4, 8], [4, 5]])
    test2(["wrt", "wrf", "er", "ett", "rftt"])
