from copy import deepcopy
from itertools import product, combinations
from pprint import pformat
from string import digits
from sys import stderr

from board_parser import get_next_line, RANGE


class SudokuSolve(object):
    STRIKES = 0
    BOARD = {}
    DIGITS = digits[1:]
    TYPE_RANGES = {
        'LINE_RANGES': list(product(list([int(digit)] for digit in digits[:9]), [list(RANGE)], repeat=1)),
        'COLUMN_RANGES': list(product([list(RANGE)], list([int(digit)] for digit in digits[:9]), repeat=1)),
        'SQUARE_RANGES': list(product([[0, 1, 2], [3, 4, 5], [6, 7, 8]], [[0, 1, 2], [3, 4, 5], [6, 7, 8]], repeat=1)),
    }
    COMBINATIONS = {u: 0 for u in [item for z in range(1, 9) for item in combinations([int(a) for a in digits[1:]], z)]}

    def __init__(self, test=False, difficulty=1, board_id=None):
        board_line = get_next_line(test=test, difficulty=difficulty, board_id=board_id)
        for x in RANGE:
            line = next(board_line)
            for y in RANGE:
                self.BOARD[(x, y)] = set(self.DIGITS) if line[y] == '0' else line[y]

        self.__log('loaded board:')
        self.__log(self.__print_board())

    @staticmethod
    def __log(item):
        # print('\n', file=stderr, flush=True)
        print(pformat(item), file=stderr, flush=True)

    def __is_empty(self, x, y):
        return isinstance(self.BOARD[(x, y)], set)

    def __pending_dict(self):
        return {x: sorted(y) for x, y in self.BOARD.items() if isinstance(y, set)}

    def __log_pending(self):
        self.__log('PENDING FIELDS:')
        self.__log(self.__pending_dict())

    def __count_pending(self):
        return len(self.__pending_dict().keys())

    def __print_board(self):
        output = []
        for x in RANGE:
            output.append(''.join([self.BOARD[(x, y)] if not self.__is_empty(x, y) else '0' for y in RANGE]))
        return '\n'.join(output)

    def __pretty_print_board(self):
        output = []
        for x in RANGE:
            items = [self.BOARD[(x, y)] if not self.__is_empty(x, y) else ('[' + ''.join(sorted(self.BOARD[(x, y)])) + ']') for y in RANGE]
            items.insert(3, '|')
            items.insert(7, '|')
            output.append(''.join([item.zfill(9 + 2) for item in items]).replace('0', ' '))
            if x in [2, 5]:
                output.append('-' * (9 + 2) * (9 + 2))
        return '\n'.join(output) + '\n'

    @staticmethod
    def __template(type_ranges, indices_template, method_a, method_b):
        for y_range, x_range in type_ranges:
            indices = deepcopy(indices_template)

            for x, y in product(x_range, y_range):
                indices = method_a(y, x, indices)

            for x, y in product(x_range, y_range):
                method_b(y, x, indices)

    def __get_missing_numbers(self, x, y, numbers):
        if not self.__is_empty(x, y):
            numbers.remove(self.BOARD[(x, y)])
        return numbers

    def __update_candidates(self, x, y, numbers):
        if self.__is_empty(x, y):
            self.BOARD[(x, y)] = self.BOARD[(x, y)].intersection(numbers)

    def __count_missing_numbers(self, x, y, numbers):
        if self.__is_empty(x, y):
            for number in self.BOARD[(x, y)]:
                numbers[number] += 1
        return numbers

    def __set_hidden_single(self, x, y, numbers):
        for key in numbers.keys():
            if numbers[key] == 1 and self.__is_empty(x, y) and key in self.BOARD[(x, y)]:
                self.BOARD[(x, y)] = key

    def __count_repeated_missing_numbers(self, x, y, number_combinations):
        if self.__is_empty(x, y):
            tmp = tuple(sorted([int(z) for z in self.BOARD[(x, y)]]))
            number_combinations[tmp] += 1
        return number_combinations

    def __remove_repeated_missing_numbers(self, x, y, number_combinations):
        found = [key for key in number_combinations.keys() if number_combinations[key] == len(key)]
        if found and self.__is_empty(x, y) and tuple(self.BOARD[(x, y)]) not in found:
            for item in found:
                if set(str(x) for x in item) == set(self.BOARD[(x, y)]):
                    break
                for number in item:
                    if str(number) in self.BOARD[(x, y)]:
                        self.BOARD[(x, y)].remove(str(number))

    def checks(self):
        for type_range in self.TYPE_RANGES.values():
            self.__template(type_range, set(self.DIGITS), self.__get_missing_numbers, self.__update_candidates)

    def obvious_singles(self):
        for x, y in product(RANGE, RANGE):
            if self.__is_empty(x, y) and len(self.BOARD[(x, y)]) == 1:
                self.BOARD[(x, y)] = self.BOARD[(x, y)].pop()
        self.checks()

    def hidden_singles(self):
        for type_range in self.TYPE_RANGES.values():
            self.__template(type_range, {str(z + 1): 0 for z in RANGE}, self.__count_missing_numbers, self.__set_hidden_single)
            self.checks()

    def nakeds(self):
        for type_range in self.TYPE_RANGES.values():
            self.__template(type_range, self.COMBINATIONS, self.__count_repeated_missing_numbers, self.__remove_repeated_missing_numbers)
            self.checks()

    def main(self):
        while self.__count_pending() != 0:
            pre_pending = self.__count_pending()
            self.checks()
            self.obvious_singles()
            self.hidden_singles()
            self.nakeds()

            self.checks()

            if self.__count_pending() == pre_pending:
                self.STRIKES += 1
                if self.STRIKES == 2:
                    print(self.__pretty_print_board())
                    exit(1)
            else:
                self.STRIKES = 0

        self.__log('solved board:')
        self.__log(self.__print_board())

        return self.__print_board()
