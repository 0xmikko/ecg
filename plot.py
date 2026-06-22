import csv
import matplotlib.pyplot as plt

time_s = []
ecg_uv = []

with open("ecg.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        time_s.append(float(row["time_s"]))
        ecg_uv.append(float(row["ecg_uv"]))

plt.figure(figsize=(14, 4))
plt.plot(time_s, ecg_uv, linewidth=0.5)
plt.xlabel("Time (s)")
plt.ylabel("ECG (µV)")
plt.title("ECG Recording")
plt.tight_layout()
plt.show()
