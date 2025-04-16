import serial
import time

CMD_START = 0xF5
CMD_END = 0xF5
BAUDRATE = 19200
# SERIAL_PORT = 'COM2'  # Change this to your correct COM port
SERIAL_PORT = '/dev/ttyUSB0'  # For Linux or MacOS, change as needed

# ACK codes
ACK_SUCCESS = 0x00
ACK_FAIL = 0x01
ACK_FULL = 0x04
ACK_NOUSER = 0x05
ACK_USER_OCCUPIED = 0x06
ACK_FINGER_OCCUPIED = 0x07
ACK_TIMEOUT = 0x08

def checksum(packet):
    return packet[1] ^ packet[2] ^ packet[3] ^ packet[4] ^ packet[5]

def build_command(cmd, p1=0, p2=0, p3=0):
    pkt = [CMD_START, cmd, p1, p2, p3, 0, 0, CMD_END]
    pkt[6] = checksum(pkt)
    return bytearray(pkt)

def send_command(ser, cmd, p1=0, p2=0, p3=0):
    pkt = build_command(cmd, p1, p2, p3)
    ser.write(pkt)
    return ser.read(8)

def parse_ack(resp):
    if len(resp) != 8 or resp[0] != CMD_START or resp[-1] != CMD_END:
        return "❌ Invalid or malformed response"

    q3 = resp[4]
    return {
        ACK_SUCCESS: "✅ Success",
        ACK_FAIL: "❌ Fail",
        ACK_FULL: "⚠️ Database Full",
        ACK_NOUSER: "❌ No User",
        ACK_USER_OCCUPIED: "⚠️ User ID Exists",
        ACK_FINGER_OCCUPIED: "⚠️ Fingerprint Exists",
        ACK_TIMEOUT: "⌛ Timeout"
    }.get(q3, f"❓ Unknown response: {hex(q3)}")

def enroll(ser, user_id, permission):
    uid_h = (user_id >> 8) & 0xFF
    uid_l = user_id & 0xFF
    cmds = [0x01, 0x02, 0x03]
    for i, cmd in enumerate(cmds, start=1):
        input(f">> Step {i}: Press Enter and place your finger...")
        res = send_command(ser, cmd, uid_h, uid_l, permission)
        print(parse_ack(res))
        time.sleep(1.5)

def verify_1n(ser):
    print(">> Place finger to verify (1:N)...")
    res = send_command(ser, 0x0C)
    if len(res) != 8:
        print("❌ Invalid response")
        return
    if res[4] == ACK_NOUSER:
        print("❌ No match")
    elif res[4] == ACK_TIMEOUT:
        print("⌛ Timeout")
    else:
        uid = (res[2] << 8) | res[3]
        perm = res[4]
        print(f"✅ Match! User ID: {uid}, Permission: {perm}")

def verify_1_1(ser, user_id):
    uid_h = (user_id >> 8) & 0xFF
    uid_l = user_id & 0xFF
    print(">> Place finger to verify against specific ID...")
    res = send_command(ser, 0x0B, uid_h, uid_l)
    print(parse_ack(res))

def delete_user(ser, user_id):
    uid_h = (user_id >> 8) & 0xFF
    uid_l = user_id & 0xFF
    res = send_command(ser, 0x04, uid_h, uid_l)
    print(parse_ack(res))

def delete_all_users(ser):
    res = send_command(ser, 0x05)
    print(parse_ack(res))

def query_user_count(ser):
    res = send_command(ser, 0x09)
    if len(res) == 8 and res[4] == ACK_SUCCESS:
        count = (res[2] << 8) | res[3]
        print(f"👥 Total Users: {count}")
    else:
        print(parse_ack(res))

def query_permission(ser, user_id):
    uid_h = (user_id >> 8) & 0xFF
    uid_l = user_id & 0xFF
    res = send_command(ser, 0x0A, uid_h, uid_l)
    if len(res) == 8 and res[4] != ACK_NOUSER:
        print(f"🧾 User {user_id} Permission: {res[4]}")
    else:
        print(parse_ack(res))

def main():
    with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=2) as ser:
        while True:
            print("\n=== Fingerprint Sensor Menu ===")
            print("1. Register Fingerprint")
            print("2. Verify Fingerprint (1:N)")
            print("3. Verify against User ID (1:1)")
            print("4. Delete User")
            print("5. Delete All Users")
            print("6. Query User Count")
            print("7. Query User Permission")
            print("8. Exit")

            choice = input("Select an option (1–8): ").strip()

            if choice == '1':
                uid = int(input("Enter user ID (1–4095): "))
                perm = int(input("Enter permission (1–3): "))
                enroll(ser, uid, perm)
            elif choice == '2':
                verify_1n(ser)
            elif choice == '3':
                uid = int(input("Enter user ID to verify: "))
                verify_1_1(ser, uid)
            elif choice == '4':
                uid = int(input("Enter user ID to delete: "))
                delete_user(ser, uid)
            elif choice == '5':
                delete_all_users(ser)
            elif choice == '6':
                query_user_count(ser)
            elif choice == '7':
                uid = int(input("Enter user ID to query: "))
                query_permission(ser, uid)
            elif choice == '8':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid selection!")

if __name__ == "__main__":
    main()
