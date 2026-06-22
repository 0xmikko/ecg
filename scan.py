import asyncio
import csv
import time
from bleak import BleakClient

ADDRESS = "8918E97A-F845-4407-76DC-D280A6E00CD8"

PMD_CONTROL = "FB005C81-02E7-F387-1CAD-8ACD2D8DF0C8"
PMD_DATA = "FB005C82-02E7-F387-1CAD-8ACD2D8DF0C8"

ECG_SETTINGS = bytearray([0x01, 0x00])

ECG_START = bytearray([
    0x02, 0x00, 0x00, 0x01,
    0x82, 0x00, 0x01, 0x01,
    0x0E, 0x00
])

ecg_samples = []
start_time = None
ctrl_response = asyncio.Event()

def handle_control(sender, data):
    print("Control response:", data.hex())
    ctrl_response.set()

def handle_data(sender, data):
    global start_time
    if start_time is None:
        start_time = time.monotonic()
    if len(data) < 10:
        return
    # Skip first 10 bytes (timestamp + frame type header)
    payload = data[10:]
    # Each ECG sample is 3 bytes (signed 24-bit little-endian), resolution 14-bit
    sample_interval = 1.0 / 130.0
    base_time = time.monotonic() - start_time
    n_samples = len(payload) // 3
    for i in range(n_samples):
        raw = int.from_bytes(payload[i * 3 : i * 3 + 3], byteorder="little", signed=True)
        t = base_time + i * sample_interval
        ecg_samples.append((t, raw))
    print(f"  {n_samples} samples (total: {len(ecg_samples)})")

def handle_disconnect(client):
    print("Disconnected!")

async def main():
    async with BleakClient(ADDRESS, disconnected_callback=handle_disconnect) as client:
        print("Connected:", client.is_connected)

        await asyncio.sleep(2)

        await client.start_notify(PMD_CONTROL, handle_control)
        await client.start_notify(PMD_DATA, handle_data)

        print("Requesting ECG settings...")
        await client.write_gatt_char(PMD_CONTROL, ECG_SETTINGS, response=True)
        await asyncio.wait_for(ctrl_response.wait(), timeout=5)
        ctrl_response.clear()

        print("Starting ECG stream...")
        await client.write_gatt_char(PMD_CONTROL, ECG_START, response=True)

        print("Recording ECG for 30 seconds...")
        await asyncio.sleep(30)

        await client.stop_notify(PMD_DATA)

    with open("ecg.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time_s", "ecg_uv"])
        writer.writerows(ecg_samples)
    print(f"Saved {len(ecg_samples)} samples to ecg.csv")

asyncio.run(main())