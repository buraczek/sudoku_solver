from lxml import html
from requests import get

RANGE = range(9)
SUDOKU_PAGE = 'https://nine.websudoku.com/'


class BoardParser(object):

    def __init__(self, board_id=None, difficulty=None):
        tree = None

        if difficulty in range(1, 5):
            id_part = f'&set_id={board_id}' if board_id is not None else ''
            url = f'{SUDOKU_PAGE}?level={difficulty}{id_part}'
            content = get(url).content
            tree = html.fromstring(content)
        else:
            exit(1)

        self.board = []
        for postfix in RANGE:
            row = []
            for prefix in RANGE:
                result = tree.xpath(f'//*[@id="f{prefix}{postfix}"]')
                value = result[0].get('value')
                row.append(str(value) if value is not None else '0')
            self.board.append(''.join(row))

        self.board = '\n'.join(self.board)


def get_next_line(test=None, difficulty=1, board_id=None):
    sudoku_test = test if test is not None else BoardParser(difficulty=difficulty, board_id=board_id).board

    for line in sudoku_test.splitlines():
        yield line
