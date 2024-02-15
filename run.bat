@echo off

REM Start frontend in a new command prompt
start cmd.exe /k "cd components\frontend_user-interface && npm start"

REM Start Node.js server in a new command prompt
start cmd.exe /k "cd components/frontend_user-interface && node indexNode.js"

REM Start backend in a new command prompt
start cmd.exe /k "cd components/backend_model && python server.py"

echo All commands have been executed in separate command prompts.
