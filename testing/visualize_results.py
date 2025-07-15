import matplotlib.pyplot as plt
import numpy as np
import os

# Model names
models = [
    "Llama-3.2 1B",
    "Llama-3.2 3B",
    "Gemma 2B",
    "Mistral 7B"
]

# Metric values
f1_full = [0.1921, 0.1588, 0.2758, 0.2732]
f1_names = [0.5099, 0.3937, 0.5658, 0.5885]
qty_accuracy = [0.4862, 0.5367, 0.8385, 0.8967]
unit_accuracy = [0.3961, 0.4758, 0.5233, 0.4981]
avg_time = [8.62, 14.79, 21.04, 41.01]

x = np.arange(len(models))  # the label locations
width = 0.35  # the width of the bars

# Create a directory to save plots if it doesn't exist
output_dir = "plots"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# === Plot 1: F1 Scores ===
fig1, ax1 = plt.subplots()
ax1.bar(x - width/2, f1_full, width, label='F1 Score (Full Tuple)')
ax1.bar(x + width/2, f1_names, width, label='F1 Score (Names Only)')
ax1.set_ylabel('F1 Score')
ax1.set_title('F1 Scores by Model (20 recipes)')
ax1.set_xticks(x)
ax1.set_xticklabels(models)
ax1.set_ylim(0, 1)
ax1.legend()
fig1.tight_layout()
f1_path = os.path.join(output_dir, "f1_scores.png")
fig1.savefig(f1_path, dpi=300)
print(f"Plot saved to {f1_path}")
plt.show()

# === Plot 2: Accuracy ===
fig2, ax2 = plt.subplots()
ax2.bar(x - width/2, qty_accuracy, width, label='Quantity Accuracy')
ax2.bar(x + width/2, unit_accuracy, width, label='Unit Accuracy')
ax2.set_ylabel('Accuracy')
ax2.set_title('Accuracy of Quantity and Unit by Model (20 recipes)')
ax2.set_xticks(x)
ax2.set_xticklabels(models)
ax2.set_ylim(0, 1)
ax2.legend()
fig2.tight_layout()
accuracy_path = os.path.join(output_dir, "accuracy.png")
fig2.savefig(accuracy_path, dpi=300)
print(f"Plot saved to {accuracy_path}")
plt.show()

# === Plot 3: Inference Time ===
fig3, ax3 = plt.subplots()
ax3.bar(x, avg_time, width, color='skyblue')
ax3.set_ylabel('Seconds')
ax3.set_title('Average Inference Time per Recipe (20 recipes)')
ax3.set_xticks(x)
ax3.set_xticklabels(models)
fig3.tight_layout()
time_path = os.path.join(output_dir, "inference_time.png")
fig3.savefig(time_path, dpi=300)
print(f"Plot saved to {time_path}")
plt.show()
