#!/bin/bash
# === 프롬프트 자동 로깅 스크립트 ===
#
# 이 스크립트는 Claude Code에서 프롬프트를 입력할 때마다 자동으로 실행됩니다.
# (UserPromptSubmit hook으로 등록)
#
# 기록 내용: 타임스탬프, 세션ID, 프롬프트 내용
# 저장 위치: .claude/prompt-log.jsonl
#
# 이 로그를 활용하여:
# 1. 자주 사용하는 프롬프트 패턴을 분석할 수 있습니다
# 2. 반복되는 패턴을 커스텀 Skill로 만들 수 있습니다
# 3. 학습 과정을 돌아볼 수 있습니다

LOG_FILE=".claude/prompt-log.jsonl"

# 로그 디렉토리 확인
mkdir -p "$(dirname "$LOG_FILE")"

# 현재 시각 (ISO 8601 형식)
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%SZ")

# stdin에서 프롬프트 내용 읽기
PROMPT=$(cat)

# JSONL 형식으로 저장 (한 줄에 하나의 JSON 객체)
# jq가 있으면 안전한 JSON 인코딩, 없으면 기본 처리
if command -v jq &> /dev/null; then
    echo "$PROMPT" | jq -c --arg ts "$TIMESTAMP" \
        '{timestamp: $ts, prompt: .}' >> "$LOG_FILE"
else
    # jq가 없는 경우 간단한 형식으로 저장
    echo "{\"timestamp\":\"$TIMESTAMP\",\"prompt\":\"$(echo "$PROMPT" | tr '\n' ' ' | sed 's/"/\\"/g')\"}" >> "$LOG_FILE"
fi
