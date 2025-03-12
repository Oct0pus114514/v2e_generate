#!/bin/bash

# 基础配置
INPUT_DIR="./input"   # 总输入目录
OUTPUT_BASE="./upsampled"   # 总输出目录
GPUS=(4 5 6 7)              # 指定要使用的GPU编号（默认值，可通过命令行覆盖）

# 解析命令行参数（支持覆盖默认GPU列表）
while [[ $# -gt 0 ]]; do
    case $1 in
        --gpus)
            GPUS=("${@:2}")
            break
            ;;
        *)
            shift
            ;;
    esac
done

# 获取所有输入子目录
input_subdirs=($(find "$INPUT_DIR" -maxdepth 1 -type d | tail -n +2))

# 并行任务启动
for gpu_idx in "${!GPUS[@]}"; do
    (
        # 设置当前GPU
        target_gpu=${GPUS[$gpu_idx]}
        export CUDA_VISIBLE_DEVICES=$target_gpu
        
        # 创建GPU专用输出目录
        output_dir="${OUTPUT_BASE}"
        mkdir -p "$output_dir"
        
        # 任务分配策略（轮询分配）
        task_idx=$gpu_idx
        while [ $task_idx -lt ${#input_subdirs[@]} ]; do
            input_sub="${input_subdirs[$task_idx]}"
            echo "[GPU $target_gpu] Processing: $input_sub"
            
            # 执行程序
            python upsampling/upsample.py \
                --input_dir "$input_sub" \
                --output_dir "$output_dir/$(basename $input_sub)" \
                >> "./upsampled/gpu${target_gpu}.log" 2>&1
            
            task_idx=$((task_idx + ${#GPUS[@]}))
        done
    ) &
done

# 等待所有后台任务
wait
echo "All tasks completed on specified GPUs: ${GPUS[@]}"