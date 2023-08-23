"""
This sorting module implements various sorting algorithms. Each algorithm function sorts an input
array of integers and has time and space complexity specified in its documentation.

This module is intended to be used for educational purposes, to understand and learn about the
different types of sorting algorithms and their implementations in Python.
"""

from itertools import chain, repeat


def insert_sort(array: list[int]) -> None:
    """
    Sort an array of integers via the insertion sort algorithm.

    Time complexity: O(n^2), where n is the length of the array.
    Extra space complexity: O(1)

    :param array: array of integers
    :return: None
    """
    for i in range(1, len(array)):
        current = array[i]
        j = i
        while j > 0 and array[j - 1] > current:
            array[j] = array[j - 1]
            j -= 1
        array[j] = current


def _merge(array_one: list[int], array_two: list[int]) -> list[int]:
    result = []
    while array_one and array_two:
        if array_one[0] < array_two[0]:
            result.append(array_one[0])
            array_one.pop(0)
        else:
            result.append(array_two[0])
            array_two.pop(0)

    result.extend(array_one)
    result.extend(array_two)
    return result


def merge_sort(array: list[int]) -> list[int]:
    """
    Sorts an array of integers using the merge sort algorithm.

    Time complexity: O(n*log(n)), where n is the length of the array.
    Extra space complexity: O(n), where n is the length of the array.

    :param array: array of integers
    :return: sorted array of integers
    """
    length = len(array)
    if length <= 1:
        return array

    mid = length // 2
    array_one = array[:mid]
    array_two = array[mid:]

    sorted_array_one = merge_sort(array_one)
    sorted_array_two = merge_sort(array_two)

    return _merge(sorted_array_one, sorted_array_two)


def quick_sort(array: list[int], left: int, right: int) -> None:
    """
    Sorts an array of integers using the quick sort algorithm.

    Time complexity: O(n*log(n)), where n is the length of the array.
    Extra space complexity: O(1)

    :param array: array of integers
    :param left: left index (inclusive)
    :param right: right index (inclusive)
    :return: None
    """
    if left < right:
        mid = _partition(array, left, right)
        quick_sort(array, left, mid - 1)
        quick_sort(array, mid + 1, right)


def _partition(array: list[int], left: int, right: int) -> int:
    pivot = array[right]
    i = left - 1
    for j in range(left, right):
        if array[j] <= pivot:
            i += 1
            array[i], array[j] = array[j], array[i]
    array[i + 1], array[right] = array[right], array[i + 1]
    return i + 1


def heap_sort(array: list[int]) -> None:
    """
    Sorts an array of integers using the heap sort algorithm.

    Time complexity: O(n*log(n)), where n is the length of the array.
    Extra space complexity: O(1).

    :param array: array of integers
    :return: None
    """
    _build_heap(array)

    for index in reversed(range(len(array))):
        array[index], array[0] = array[0], array[index]
        _heapify(array, index, 0)


def _left_child(index: int) -> int:
    return 2 * index + 1


def _right_child(index: int) -> int:
    return 2 * index + 2


def _heapify(array: list[int], size: int, index: int) -> None:
    largest = index
    if _left_child(index) < size and array[_left_child(index)] > array[largest]:
        largest = _left_child(index)
    if _right_child(index) < size and array[_right_child(index)] > array[largest]:
        largest = _right_child(index)
    if largest != index:
        array[index], array[largest] = array[largest], array[index]
        _heapify(array, size, largest)


def _build_heap(array: list[int]) -> None:
    for i in reversed(range(len(array))):
        _heapify(array, len(array), i)


def counting_sort(array: list[int], max_value: int) -> list[int]:
    """
    Sorts an array of integers using the counting sort algorithm.

    Time complexity: O(n+k), where:
     - n is the length of the array
     - k is the maximum value in the array

    Extra space complexity: O(n+k), where:
     - n is the length of the array
     - k is the maximum value in the array

    The function assumes that the array contains non-negative integers.

    :param array: array of integers
    :param max_value: maximum value in the array
    :return: sorted array of integers
    """
    count_of_each_integer = list(repeat(0, max_value + 1))
    for num in array:
        count_of_each_integer[num] += 1

    for i in range(1, max_value + 1):
        count_of_each_integer[i] += count_of_each_integer[i - 1]

    result = list(repeat(0, len(array)))
    for num in reversed(array):
        count_of_each_integer[num] -= 1
        result[count_of_each_integer[num]] = num

    return result


def radix_sort(array: list[int], max_digits: int, base: int = 10) -> list[int]:
    """
    Sorts an array of integers using the radix sort algorithm.

    Time complexity: O(d*(n+k)), where:
     - d is the number of digits in the largest number
     - n is the length of the array
     - k is the number of possible digits (the base)

    Extra space complexity: O(n+k), where:
     - n is the length of the array
     - k is the number of possible digits (the base)

    The function assumes that the array contains non-negative integers.

    :param array: array of integers
    :param max_digits: number of digits in the largest number
    :param base: base of the numbers, default is 10
    :return: sorted array of integers
    """
    for i in range(max_digits):
        bins: list[list[int]] = [[] for _ in range(base)]
        for num in array:
            digit = (num // base**i) % base
            bins[digit].append(num)

        array = list(chain.from_iterable(bins))

    return array
