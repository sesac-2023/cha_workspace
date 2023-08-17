# 토마토 문제 https://www.acmicpc.net/problem/7576

import sys
input = sys.stdin.readline

from collections import deque

dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

M, N = map(int,input().split())
board = [list(map(int,input().split())) for _ in range(N)]

queue = deque()
for r in range(N):
    for c in range(M):
        if board[r][c] == 1: queue.append((r, c))               # 익은 토마토는 큐에 넣기

while queue:                                                    # 큐가 빌 때까지
    r, c = queue.popleft()                                      # 큐에서 꺼내서
    for d in range(4):                                          # 4방 탐색하여
        nr, nc = r + dr[d], c + dc[d]

        if 0 <= nr < N and 0 <= nc < M and board[nr][nc] == 0:  # 범위 내에 있고 익지 않았다면
            board[nr][nc] = board[r][c] + 1                     # 해당 좌표의 값을 이전 좌표값 + 1로 바꾸고(익히고, visited)
            queue.append((nr, nc))                              # 큐에 산입

ans = -1

for row in board:                                               # 토마토 판의 각 행별로
    if row.count(0) > 0:                                        # 0이 남았다면(익지 않은 토마토)
        ans = 0                                                 # ans 0으로 바꾸고 break
        break
    ans = max(row + [ans])                                      # 열 돌며 최대값으로 최신화

print(ans - 1)                                                  # 답은 ans - 1


"""입력 예제
6 4
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 1

-> 8
"""