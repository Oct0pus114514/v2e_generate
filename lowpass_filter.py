import numpy as np
from collections import defaultdict

class LowpassFilter:
    def __init__(self, tau=0.1):
        """
        初始化低通滤波器
        :param tau: 时间常数，控制滤波强度（秒）
        """
        self.tau = tau
        # 存储每个像素的滤波状态：(last_time, filtered_value)
        self.state = defaultdict(lambda: (0.0, 0.0))
        
    def process_event(self, event):
        """
        处理单个事件并直接修改其极性
        :param event: (x, y, p, t) 元组
        """
        x, y, p, t = event
        key = (x, y)
        last_time, last_value = self.state[key]
        
        # 计算时间差
        dt = t - last_time
        
        # 计算衰减因子
        alpha = np.exp(-dt / self.tau)
        
        # 更新滤波值并直接修改事件极性
        filtered_value = alpha * last_value + (1 - alpha) * p
        event[2] = filtered_value  # 直接修改p值
        
        # 更新状态
        self.state[key] = (t, filtered_value)
        
    def process_events(self, x, y, p, t):
        """
        处理单个事件
        :param x: x坐标
        :param y: y坐标 
        :param p: 极性
        :param t: 时间戳
        """
        self.process_event([x, y, p, t])
    
    def get_state(self):
        """
        获取当前所有像素的滤波状态
        :return: 包含所有像素滤波状态的字典
        """
        return {k: v[1] for k, v in self.state.items()}

# 示例用法
if __name__ == "__main__":
    # 创建滤波器，时间常数设为0.1秒
    filter = LowpassFilter(tau=0.1)
    
    # 模拟事件流（使用列表存储以便修改）
    events = [
        [10, 20, 1, 0.0],   # 事件1
        [10, 20, -1, 0.05], # 事件2
        [10, 20, 1, 0.15],  # 事件3
        [10, 20, -1, 0.25]  # 事件4
    ]
    
    # 处理事件
    for x, y, p, t in events:
        filter.process_events(x, y, p, t)
    
    # 打印结果
    print("Filtered events:")
    for x, y, p, t in events:
        print(f"Event at ({x}, {y}): filtered_p={p:.2f}, t={t:.2f}")
    
    # 获取最终状态
    print("\nFinal state:")
    state = filter.get_state()
    for (x,y), val in state.items():
            print(f"Pixel ({x}, {y}): {val:.2f}")
