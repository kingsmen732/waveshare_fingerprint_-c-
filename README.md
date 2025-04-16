# Waveshare Fingerprint Sensor (C)

A Rust CLI tool to interface with the **Waveshare UART Fingerprint Sensor (C)** via serial communication. Supports full functionality including enrollment, verification, deletion, and querying of fingerprint data.

RAW implementation of this project is available in:
- RUST
- PYTHON

[ ⭐ Link to the Project](https://github.com/kingsmen732/waveshare_fingerprint_-c-)  
If the link doesn't redirect, use:  
https://github.com/kingsmen732/waveshare_fingerprint_-c-

---

## ✨ Features

- Register fingerprints with user ID and permission level.
- Verify fingerprints in 1:N and 1:1 mode.
- Delete individual or all users.
- Query total number of enrolled users.
- Retrieve permission level of specific user IDs.
- Built-in CLI interface for smooth interaction.

---

## 📦 Installation

Install Rust if you haven't already:  
https://www.rust-lang.org/tools/install

Clone the repository and build the project:

```bash
git clone https://github.com/kingsmen732/GROW_R502-A_fingerprint.git
cd GROW_R502-A_fingerprint
cargo build --release
```

To run the CLI app:

```bash
cargo run
```

---

## 🚀 Usage

### Rust Version

Edit the port and baudrate inside `main.rs` if needed:

```rust
const SERIAL_PORT: &str = "COM2"; // or "/dev/ttyUSB0" on Linux
const BAUDRATE: u32 = 19200;
```

Then run the app:

```bash
cargo run
```

### Python Version

1. Ensure Python is installed.
2. Install pyserial:
   ```bash
   pip install pyserial
   ```
3. Run the CLI:
   ```bash
   python main.py
   ```

---

## 💻 Menu Options

| Option | Description |
|--------|-------------|
| 1 | **Register Fingerprint** – Enroll fingerprint with User ID and Permission |
| 2 | **Verify Fingerprint (1:N)** – Match against all users |
| 3 | **Verify against User ID (1:1)** – Match against a specific ID |
| 4 | **Delete User** – Remove a fingerprint by ID |
| 5 | **Delete All Users** – Clear the fingerprint database |
| 6 | **Query User Count** – Show total enrolled |
| 7 | **Query User Permission** – Get permission level for a user |
| 8 | **Exit** – Quit the CLI tool |

---

## 📌 Example Output

```text
=== Fingerprint Sensor Menu ===
1. Register Fingerprint
2. Verify Fingerprint (1:N)
3. Verify against User ID (1:1)
4. Delete User
5. Delete All Users
6. Query User Count
7. Query User Permission
8. Exit
Select an option (1–8): 2
>> Place finger to verify (1:N)...
✅ Match! User ID: 1, Permission: 1
```

---

## 💡 Sensor Compatibility

Tested with:
- **Waveshare UART Fingerprint Sensor (C)**

Should work with other UART-based sensors that follow the same protocol (R502-A compatible).

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 👋 Contributions

Pull requests, issues, and feature suggestions are welcome. Let's make this better together!

```

---

Let me know if you'd like me to auto-generate the `Cargo.toml` as well, or prepare this for crates.io publishing!