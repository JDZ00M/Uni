#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class JointPublisher(Node):
    def __init__(self):
        super().__init__('joint_publisher')
        self.publisher_ = self.create_publisher(JointState, '/joint_states', 10)

        # 🔹 Joints de tu URDF
        self.joint_names = [
            'pieza1_joint',
            'pieza2_joint',
            'pieza3_joint',
            'pieza4_joint',
            'pieza5_joint',
            'pieza6_joint'
        ]
        pi=3.141592
        # 🔹 Rutina de posiciones (rad)
        self.positions = [
            [pi, pi/2, 0.0, 0.0, 0.0, 0.0],   # posición inicial
            [pi/6, -pi/4, -pi/4, pi/6, pi/3, 0.0],  # otra pose
            [-30*pi/180, -45*pi/180, -90*pi/180, 20*pi/180, 30*pi/180, 15*pi/180], # otra pose
        ]
        self.index = 0
        self.timer = self.create_timer(2.0, self.timer_callback)

    def timer_callback(self):
        msg = JointState()
        msg.name = self.joint_names
        msg.position = self.positions[self.index]
        msg.header.stamp = self.get_clock().now().to_msg()
        self.publisher_.publish(msg)

        self.get_logger().info(f'Pose {self.index+1}: {msg.position}')
        self.index = (self.index + 1) % len(self.positions)


def main(args=None):
    rclpy.init(args=args)
    node = JointPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
