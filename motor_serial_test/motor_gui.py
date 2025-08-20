import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from tkinter import *

class MotorGui(Node):
    def __init__(self):
        super().__init__('motor_gui')

        self.pub = self.create_publisher(String, 'motor_command', 10)
        self.sub = self.create_subscription(String, 'encoder_vals', self.enc_callback, 10)

        # GUI
        self.tk = Tk()
        self.tk.title("Motor Test GUI")

        Label(self.tk, text="Motor 1").pack()
        self.m1 = Scale(self.tk, from_=-255, to=255, orient=HORIZONTAL)
        self.m1.pack()

        Label(self.tk, text="Motor 2").pack()
        self.m2 = Scale(self.tk, from_=-255, to=255, orient=HORIZONTAL)
        self.m2.pack()

        Button(self.tk, text="Send", command=self.send).pack()
        Button(self.tk, text="Stop", command=self.stop).pack()

        self.enc_label = Label(self.tk, text="Encoders: ---")
        self.enc_label.pack()

    def send(self):
        cmd = f"o {self.m1.get()} {self.m2.get()}"
        self.pub.publish(String(data=cmd))
        self.get_logger().info(f"➡️ Published: {cmd}")

    def stop(self):
        self.pub.publish(String(data="o 0 0"))
        self.get_logger().info("🛑 Published stop command")

    def enc_callback(self, msg):
        self.enc_label.config(text=f"Encoders: {msg.data}")

    def update(self):
        self.tk.update()

def main(args=None):
    rclpy.init(args=args)
    gui = MotorGui()
    try:
        while rclpy.ok():
            rclpy.spin_once(gui, timeout_sec=0.01)
            gui.update()
    except KeyboardInterrupt:
        pass
    gui.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
