#!/bin/bash

# 设置Python脚本的路径
PYTHON_SCRIPT_PATH="main.py"

# 设置超时时间，单位为秒
TIMEOUT=90

# 设置执行次数
NUM_EXECUTIONS=100

for ((i=1; i<=NUM_EXECUTIONS; i++)); do
  echo "开始执行Python脚本（第 $i 次执行）... history_2 iteration study 2 for chatgpt"
  # 在后台启动Python脚本
  python "$PYTHON_SCRIPT_PATH" --subject history --dataset ../data/history/2_ProblemSetWithAnalysis_1000_new.json --num 10 --iteration_study --last_iteration_path ../res/history_2/chatgpt_cot.json --web_LLM gpt-3.5-turbo --save_dir ../res/history_2/chatgpt_iteration_2.json &
  # 获取Python进程的PID
  PID=$!
  
  # 等待3分钟
  sleep $TIMEOUT

  # 检查Python进程是否仍在运行
  if ps -p $PID > /dev/null; then
    echo "Python脚本已超时，准备终止进程..."
    # 终止Python进程
    kill $PID
    wait $PID 2>/dev/null
    echo "Python脚本已终止"
    let i--
  else
    echo "Python脚本已成功执行"
  fi
done


for ((i=1; i<=NUM_EXECUTIONS; i++)); do
  echo "开始执行Python脚本（第 $i 次执行）... history_2 iteration study 3 for chatgpt"
  # 在后台启动Python脚本
  python "$PYTHON_SCRIPT_PATH" --subject history --dataset ../data/history/2_ProblemSetWithAnalysis_1000_new.json --num 10 --iteration_study --last_iteration_path ../res/history_2/chatgpt_iteration_2.json --web_LLM gpt-3.5-turbo --save_dir ../res/history_2/chatgpt_iteration_3.json &
  # 获取Python进程的PID
  PID=$!
  
  # 等待3分钟
  sleep $TIMEOUT

  # 检查Python进程是否仍在运行
  if ps -p $PID > /dev/null; then
    echo "Python脚本已超时，准备终止进程..."
    # 终止Python进程
    kill $PID
    wait $PID 2>/dev/null
    echo "Python脚本已终止"
    let i--
  else
    echo "Python脚本已成功执行"
  fi
done


for ((i=1; i<=NUM_EXECUTIONS; i++)); do
  echo "开始执行Python脚本（第 $i 次执行）... history_2 iteration study 4 for chatgpt"
  # 在后台启动Python脚本
  python "$PYTHON_SCRIPT_PATH" --subject history --dataset ../data/history/2_ProblemSetWithAnalysis_1000_new.json --num 10 --iteration_study --last_iteration_path ../res/history_2/chatgpt_iteration_3.json --web_LLM gpt-3.5-turbo --save_dir ../res/history_2/chatgpt_iteration_4.json &
  # 获取Python进程的PID
  PID=$!
  
  # 等待3分钟
  sleep $TIMEOUT

  # 检查Python进程是否仍在运行
  if ps -p $PID > /dev/null; then
    echo "Python脚本已超时，准备终止进程..."
    # 终止Python进程
    kill $PID
    wait $PID 2>/dev/null
    echo "Python脚本已终止"
    let i--
  else
    echo "Python脚本已成功执行"
  fi
done


for ((i=1; i<=NUM_EXECUTIONS; i++)); do
  echo "开始执行Python脚本（第 $i 次执行）... history_2 iteration study 5 for chatgpt"
  # 在后台启动Python脚本
  python "$PYTHON_SCRIPT_PATH" --subject history --dataset ../data/history/2_ProblemSetWithAnalysis_1000_new.json --num 10 --iteration_study --last_iteration_path ../res/history_2/chatgpt_iteration_4.json --web_LLM gpt-3.5-turbo --save_dir ../res/history_2/chatgpt_iteration_5.json &
  # 获取Python进程的PID
  PID=$!
  
  # 等待3分钟
  sleep $TIMEOUT

  # 检查Python进程是否仍在运行
  if ps -p $PID > /dev/null; then
    echo "Python脚本已超时，准备终止进程..."
    # 终止Python进程
    kill $PID
    wait $PID 2>/dev/null
    echo "Python脚本已终止"
    let i--
  else
    echo "Python脚本已成功执行"
  fi
done




for ((i=1; i<=NUM_EXECUTIONS; i++)); do
  echo "开始执行Python脚本（第 $i 次执行）... history_3 iteration study 2 for chatgpt"
  # 在后台启动Python脚本
  python "$PYTHON_SCRIPT_PATH" --subject history --dataset ../data/history/3_ProblemSetWithAnalysis_1000_new.json --num 10 --iteration_study --last_iteration_path ../res/history_3/chatgpt_cot.json --web_LLM gpt-3.5-turbo --save_dir ../res/history_3/chatgpt_iteration_2.json &
  # 获取Python进程的PID
  PID=$!
  
  # 等待3分钟
  sleep $TIMEOUT

  # 检查Python进程是否仍在运行
  if ps -p $PID > /dev/null; then
    echo "Python脚本已超时，准备终止进程..."
    # 终止Python进程
    kill $PID
    wait $PID 2>/dev/null
    echo "Python脚本已终止"
    let i--
  else
    echo "Python脚本已成功执行"
  fi
done


for ((i=1; i<=NUM_EXECUTIONS; i++)); do
  echo "开始执行Python脚本（第 $i 次执行）... history_3 iteration study 3 for chatgpt"
  # 在后台启动Python脚本
  python "$PYTHON_SCRIPT_PATH" --subject history --dataset ../data/history/3_ProblemSetWithAnalysis_1000_new.json --num 10 --iteration_study --last_iteration_path ../res/history_3/chatgpt_iteration_2.json --web_LLM gpt-3.5-turbo --save_dir ../res/history_3/chatgpt_iteration_3.json &
  # 获取Python进程的PID
  PID=$!
  
  # 等待3分钟
  sleep $TIMEOUT

  # 检查Python进程是否仍在运行
  if ps -p $PID > /dev/null; then
    echo "Python脚本已超时，准备终止进程..."
    # 终止Python进程
    kill $PID
    wait $PID 2>/dev/null
    echo "Python脚本已终止"
    let i--
  else
    echo "Python脚本已成功执行"
  fi
done


for ((i=1; i<=NUM_EXECUTIONS; i++)); do
  echo "开始执行Python脚本（第 $i 次执行）... history_3 iteration study 4 for chatgpt"
  # 在后台启动Python脚本
  python "$PYTHON_SCRIPT_PATH" --subject history --dataset ../data/history/3_ProblemSetWithAnalysis_1000_new.json --num 10 --iteration_study --last_iteration_path ../res/history_3/chatgpt_iteration_3.json --web_LLM gpt-3.5-turbo --save_dir ../res/history_3/chatgpt_iteration_4.json &
  # 获取Python进程的PID
  PID=$!
  
  # 等待3分钟
  sleep $TIMEOUT

  # 检查Python进程是否仍在运行
  if ps -p $PID > /dev/null; then
    echo "Python脚本已超时，准备终止进程..."
    # 终止Python进程
    kill $PID
    wait $PID 2>/dev/null
    echo "Python脚本已终止"
    let i--
  else
    echo "Python脚本已成功执行"
  fi
done


for ((i=1; i<=NUM_EXECUTIONS; i++)); do
  echo "开始执行Python脚本（第 $i 次执行）... history_3 iteration study 5 for chatgpt"
  # 在后台启动Python脚本
  python "$PYTHON_SCRIPT_PATH" --subject history --dataset ../data/history/3_ProblemSetWithAnalysis_1000_new.json --num 10 --iteration_study --last_iteration_path ../res/history_3/chatgpt_iteration_4.json --web_LLM gpt-3.5-turbo --save_dir ../res/history_3/chatgpt_iteration_5.json &
  # 获取Python进程的PID
  PID=$!
  
  # 等待3分钟
  sleep $TIMEOUT

  # 检查Python进程是否仍在运行
  if ps -p $PID > /dev/null; then
    echo "Python脚本已超时，准备终止进程..."
    # 终止Python进程
    kill $PID
    wait $PID 2>/dev/null
    echo "Python脚本已终止"
    let i--
  else
    echo "Python脚本已成功执行"
  fi
done