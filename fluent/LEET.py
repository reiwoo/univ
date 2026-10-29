from typing import List

class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        flag = True
        for row in board:
            flag = flag and self.validrow(row)
        for i in range(len(board[0])):
            column = [row[i] for row in board]
            flag = flag and self.validrow(column)
        for box_r in range(3):
            for box_c in range(3):
                temp = []
                for i in range(3):
                    for j in range(3):
                        r = box_r * 3 + i
                        c = box_c * 3 + j
                        temp.append(board[r][c])
                flag = flag and self.validrow(temp)
        return flag
    def validrow(self, nums: list[int]) -> bool:
        nums = [int(x) for x in nums if x != "."]
        seen = set()
        for num in nums:
            if not (1 <= num <= 9) or num in seen:
                return False
            seen.add(num)
        return True
if __name__ == "__main__":
    sol = Solution()
    board =   [["5","3",".",".","7",".",".",".","."]
              ,["6",".",".","1","9","5",".",".","."]
              ,[".","9","8",".",".",".",".","6","."]
              ,["8",".",".",".","6",".",".",".","3"]
              ,["4",".",".","8",".","3",".",".","1"]
              ,["7",".",".",".","2",".",".",".","6"]
              ,[".","6",".",".",".",".","2","8","."]
              ,[".",".",".","4","1","9",".",".","5"]
              ,[".",".",".",".","8",".",".","7","9"]]
    print(sol.isValidSudoku(board))