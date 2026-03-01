import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import threading

class Joint2Plotter(Node):
    def __init__(self):
        super().__init__('joint2_plotter')

        # 구독
        self.sub_goal = self.create_subscription(Float64, '/joint2_goal', self.goal_callback, 10)
        self.sub_actual = self.create_subscription(Float64, '/joint2_actual', self.actual_callback, 10)

        # 데이터 저장
        self.goal_data = deque(maxlen=100)
        self.actual_data = deque(maxlen=100)
        self.time_data = deque(maxlen=100)
        self.counter = 0

        # Matplotlib 초기화
        self.fig, self.ax = plt.subplots()
        self.line_goal, = self.ax.plot([], [], label='Goal', color='r')
        self.line_actual, = self.ax.plot([], [], label='Actual', color='b')
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(-1.0, 1.0)  # 필요시 조정
        self.ax.set_xlabel('Sample')
        self.ax.set_ylabel('Joint2 Position')
        self.ax.legend()

        # 애니메이션
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=100)

    def goal_callback(self, msg):
        self.goal_data.append(msg.data)
        self._update_time_data()

    def actual_callback(self, msg):
        self.actual_data.append(msg.data)
        self._update_time_data()

    def _update_time_data(self):
        # time_data 길이를 goal/actual 길이에 맞춤
        max_len = max(len(self.goal_data), len(self.actual_data))
        while len(self.time_data) < max_len:
            self.time_data.append(self.counter)
            self.counter += 1

    def update_plot(self, frame):
        if len(self.time_data) == 0:
            return self.line_goal, self.line_actual

        # 길이 맞추기
        goal_plot = list(self.goal_data)
        actual_plot = list(self.actual_data)
        min_len = min(len(self.time_data), len(goal_plot), len(actual_plot))
        x = list(self.time_data)[-min_len:]
        goal_plot = goal_plot[-min_len:]
        actual_plot = actual_plot[-min_len:]

        self.line_goal.set_data(x, goal_plot)
        self.line_actual.set_data(x, actual_plot)

        self.ax.set_xlim(max(0, x[0]), x[-1]+1)
        return self.line_goal, self.line_actual

def main(args=None):
    rclpy.init(args=args)
    node = Joint2Plotter()

    # rclpy spin을 별도 스레드에서 실행
    spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spin_thread.start()

    # Matplotlib 이벤트 루프 실행
    plt.show()

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
