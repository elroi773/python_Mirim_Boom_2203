#1부터 100까지 숫자에 3,6,9가 포함된 갯수 만큼 박수를 치는 369 게임을 만든다고 할 때 
# 박수를 친 횟수에는 모두 몇번인지 구하는 코드를 작성하시오 
#예를 들어 13은 박수를 한 번 치고 33은 박수를 두번 친다 단 문자열은 이중 for 문을 사용한다 

clap_count = 0

for num in range(1, 101):
    num_str = str(num)
    for ch in num_str:
        if ch in "369":
            clap_count += 1
            
print("총 박수 횟수:", clap_count)

