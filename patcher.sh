#!/bin/bash

# 프로그램 이름 정의
PROGRAM_NAME="python3"
SCRIPT_NAME="adaline-bot.py"

# 1. 실행 중인 프로세스 찾기 및 종료
echo "찾는 중: $SCRIPT_NAME"
PID=$(ps aux | grep "$SCRIPT_NAME" | grep -v "grep" | awk '{print $2}')
if [ -n "$PID" ]; then
    echo "프로세스 종료: PID=$PID"
    kill -9 $PID
else
    echo "실행 중인 프로세스가 없습니다."
fi

# 2. 최신 코드 가져오기
echo "코드 업데이트 중..."
git pull

# 3. 프로그램 다시 실행
echo "프로그램 다시 실행 중..."
nohup python3 "$SCRIPT_NAME" > output.log 2>&1 &

echo "패치 완료!"