#!/bin/bash

# 输入和输出根目录
INPUT_DIR="./upsampled"
OUTPUT_DIR="./events"

# 可用GPU列表（根据实际GPU ID修改）
GPUS=(4 5 6 7)  # 示例：4张GPU
NUM_GPUS=${#GPUS[@]}

# 获取所有需要处理的子目录列表（确保路径分隔符正确处理）
SUB_DIRS=()
while IFS= read -r -d $'\0' dir; do
    SUB_DIRS+=("$dir")
done < <(find "$INPUT_DIR" -type d -exec sh -c '
    if [ -d "$1/imgs" ] && [ -f "$1/timestamps.txt" ]; then
        printf "%s\0" "$1"
    fi
' _ {} \;)

# 检查是否找到子目录
if [ ${#SUB_DIRS[@]} -eq 0 ]; then
    echo "错误：未找到符合条件的子目录！"
    exit 1
fi

# 为每个子目录分配GPU并启动后台进程
declare -A PID_GPU_MAP
for i in "${!SUB_DIRS[@]}"; do
    GPU_IDX=$((i % NUM_GPUS))
    GPU=${GPUS[$GPU_IDX]}
    SUB_DIR="${SUB_DIRS[$i]}"
    
    # 使用字符串操作获取相对路径（替代realpath）
    REL_PATH="${SUB_DIR#$INPUT_DIR/}"  # 移除INPUT_DIR前缀
    OUT_SUBDIR="$OUTPUT_DIR/$REL_PATH"
    
    # 确保输出目录存在
    mkdir -p "$OUT_SUBDIR" || { echo "无法创建目录：$OUT_SUBDIR"; exit 1; }
    
    # 启动任务
    CUDA_VISIBLE_DEVICES=$GPU python esim_torch/scripts/generate_events.py \
        -i "$SUB_DIR" \
        -o "$OUT_SUBDIR" \
        -cn 0.2 \
        -cp 0.2 \
        -rp 0 &
    
    # 记录进程和GPU的对应关系
    PID_GPU_MAP[$!]=$GPU
    echo "任务 $((i+1))/${#SUB_DIRS[@]} 分配到 GPU $GPU：$SUB_DIR"
done

# 等待所有后台进程完成
wait
echo "所有任务已完成！"