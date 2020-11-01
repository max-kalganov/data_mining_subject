"""
Description     : Simple Python implementation of the Apriori Algorithm

Usage:
    $python apriori.py -f DATASET.csv -s minSupport  -c minConfidence

    $python apriori.py -f DATASET.csv -s 0.15 -c 0.6
"""

import sys

from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser
from typing import Iterable


def subsets(arr):
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def return_items_with_min_support(item_set, transaction_list, min_support, freq_set):
    _item_set = set()
    local_set = defaultdict(int)
    for item in item_set:
        for transaction in transaction_list:
            if item.issubset(transaction):
                freq_set[item] += 1
                local_set[item] += 1

    for item, count in local_set.items():
        support = float(count) / len(transaction_list)
        if support >= min_support:
            _item_set.add(item)

    return _item_set


def join_set(item_set: Iterable, length: int):
    return set([i.union(j) for i in item_set for j in item_set if len(i.union(j)) == length])


def get_item_set_transaction_list(data_iterator: Iterable):
    transaction_list = list()
    item_set = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transaction_list.append(transaction)
        for item in transaction:
            item_set.add(frozenset([item]))  # Generate 1-itemSets
    return item_set, transaction_list


def get_support(item, freq_set, transaction_list):
    return float(freq_set[item]) / len(transaction_list)


def run_apriori(data: Iterable, min_support: float, min_confidence: float):
    item_set, transaction_list = get_item_set_transaction_list(data)
    freq_set = defaultdict(int)
    large_set = dict()
    one_c_set = return_items_with_min_support(item_set, transaction_list, min_support, freq_set)
    current_l_set = one_c_set
    k = 2
    while current_l_set:
        large_set[k - 1] = current_l_set
        current_l_set = join_set(current_l_set, k)
        current_c_set = return_items_with_min_support(current_l_set, transaction_list, min_support, freq_set)
        current_l_set = current_c_set
        k = k + 1

    to_ret_items = []
    for key, value in large_set.items():
        to_ret_items.extend([(tuple(item), get_support(item, freq_set, transaction_list))
                             for item in value])

    to_ret_rules = []
    for key, value in list(large_set.items())[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = get_support(item, freq_set, transaction_list) / get_support(element,
                                                                                             freq_set,
                                                                                             transaction_list)
                    if confidence >= min_confidence:
                        to_ret_rules.append(((tuple(element), tuple(remain)),
                                             confidence))
    return to_ret_items, to_ret_rules


def print_results(items, rules):
    for item, support in sorted(items, key=lambda x: x[1]):
        print(f"item - {item}, support - {support}")
    print()
    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        print(f"rule - {pre} -> {post}, confidence - {confidence}")


if __name__ == "__main__":
    data = [
        frozenset(["Ф", "А", "К", "У", "Л"]),
        frozenset(["И", "Н", "Ф", "О", "Р", "М"]),
        frozenset(["К", "А", "Л", "Н", "О"]),
        frozenset(["М", "А", "К", "И"]),
    ]

    minSupport = 2/5
    minConfidence = 2/5

    items, rules = run_apriori(data, minSupport, minConfidence)

    print_results(items, rules)
