#!/bin/bash

# 提示用户选择是否在后台运行
read -p "Do you want to run the script in the background? (y/n): " choice

if [ "$choice" = "y" ]; then
    # 在后台运行 Python 程序 main.py 并隐藏输出
    nohup python main.py > /dev/null 2>&1 &
    echo "Script is running in the background."
else
    # 在前台运行 Python 程序 main.py
    python main.py
fi

read -p "Press any key to continue..."