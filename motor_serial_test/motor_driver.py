import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class MotorDriver(Node):
    def __init__(self):
        super().__init__('motor_driver')
        
        # Parameters
        self.declare_parameter('serial_port', '/dev/ttyACM0')
        self.declare_parameter('baud_rate', 57600)

        port = self.get_parameter('serial_port').value
        baud = self.get_parameter('baud_rate').value

        try:
            self.ser = serial.Serial(port, baud, timeout=1)
            self.get_logger().info(f"✅ Connected to {port} at {baud}")
        except Exception as e:
            self.get_logger().error(f"❌ Could not open serial port: {e}")
            raise e

        # Subscriber for motor commands
        self.subscription = self.create_subscription(
            String,
            'motor_command',
            self.listener_callback,
            10)

        # Publisher for encoder values
        self.encoder_pub = self.create_publisher(String, 'encoder_vals', 10)

        # Poll encoders
        self.timer = self.create_timer(0.5, self.read_encoders)

    def listener_callback(self, msg):
        cmd = msg.data.strip() + "\r"
        self.ser.write(cmd.encode('utf-8'))
        self.get_logger().info(f"➡️ Sent: {cmd.strip()}")

    def read_encoders(self):
        self.ser.write(b"e\r")
        resp = self.ser.readline().decode('utf-8').strip()
        if resp:
            self.encoder_pub.publish(String(data=resp))
            self.get_logger().info(f"⬅️ Encoders: {resp}")

def main(args=None):
    rclpy.init(args=args)
    node = MotorDriver()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
