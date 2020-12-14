import unittest

from sudoku_solve import SudokuSolve


class SudokuSolverTest(unittest.TestCase):

    def _test_solution_for_difficulty(self, difficulty):
        test_data = {
            1: {
                'puzzle': '010000483\n290003007\n008001052\n509047000\n030105020\n000380506\n780500600\n900700048\n462000070\n',
                'solution': '615279483\n294853167\n378461952\n529647831\n836195724\n147382596\n783524619\n951736248\n462918375',
            },

            2: {
                'puzzle': '002017060\n690084001\n070900000\n200000007\n380050092\n500000008\n000005030\n100490075\n030820400\n',
                'solution': '852317964\n693584721\n471962583\n219648357\n384751692\n567239148\n948175236\n126493875\n735826419',
            },

            3: {
                'puzzle': '000360085\n506070020\n000048070\n700000502\n000000000\n105000009\n010950000\n050080307\n940027000\n',
                'solution': '471362985\n586179423\n239548671\n794816532\n368295714\n125734869\n817953246\n652481397\n943627158',
            },

            4: {
                'puzzle': '004087002\n902000300\n000050000\n509600080\n010000030\n020009507\n000030000\n006000805\n800740100\n',
                'solution': '164387952\n952164378\n387952614\n579623481\n618475239\n423819567\n241538796\n736291845\n895746123',
            },
        }

        self.assertEqual(
            first=SudokuSolve(test=test_data[difficulty]['puzzle'], difficulty=difficulty).main(),
            second=test_data[difficulty]['solution']
        )

    def test_easy_difficulty(self):
        self._test_solution_for_difficulty(1)

    def test_medium_difficulty(self):
        self._test_solution_for_difficulty(2)

    def test_hard_difficulty(self):
        self._test_solution_for_difficulty(3)

    def test_evil_difficulty(self):
        self._test_solution_for_difficulty(4)


if __name__ == '__main__':
    unittest.main()

    # TODO
    # SudokuSolve(test=False, difficulty=4, board_id=10122102494).main()
