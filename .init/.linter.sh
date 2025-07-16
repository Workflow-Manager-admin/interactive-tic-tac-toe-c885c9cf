#!/bin/bash
cd /home/kavia/workspace/code-generation/interactive-tic-tac-toe-c885c9cf/backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

