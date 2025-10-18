# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
#
# # Read data from the Excel file
# df = pd.read_excel('query_performance_results.xlsx')
#
# # Set up the plot
# plt.figure(figsize=(12, 8))
# plt.style.use('seaborn-v0_8')  # Use a nice style
#
# # Define colors for each query line
# colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
# markers = ['o', 's', '^', 'D', 'v']
#
# # Plot each query as a separate line
# queries = df.columns[1:]  # Skip the 'Scale' column
#
# for i, query in enumerate(queries):
#     plt.plot(df['Scale'], df[query],
#              label=query,
#              color=colors[i % len(colors)],
#              marker=markers[i % len(markers)],
#              markersize=8,
#              linewidth=2.5,
#              markeredgecolor='white',
#              markeredgewidth=1)
#
# # Customize the plot
# plt.xscale('log')  # Use logarithmic scale for better visualization
# plt.yscale('log')   # Use logarithmic scale for time as well
#
# plt.xlabel('Data Size (records)', fontsize=12, fontweight='bold')
# plt.ylabel('Execution Time (milliseconds)', fontsize=12, fontweight='bold')
# plt.title('Query Performance vs. Data Scale', fontsize=14, fontweight='bold')
#
# # Format x-axis ticks to show human-readable labels
# x_ticks = df['Scale'].values
# x_labels = ['1k', '10k', '100k', '1M']
# plt.xticks(x_ticks, x_labels)
#
# # Add grid for better readability
# plt.grid(True, alpha=0.3, which='both')
# plt.minorticks_on()
#
# # Add legend
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
#
# # Add value annotations on each point
# for query in queries:
#     for scale, time in zip(df['Scale'], df[query]):
#         plt.annotate(f'{time:.1f}',
#                     (scale, time),
#                     textcoords="offset points",
#                     xytext=(0,10),
#                     ha='center',
#                     fontsize=8,
#                     alpha=0.7)
#
# # Adjust layout to prevent cutting off
# plt.tight_layout()
#
# # Save the plot as high-quality image
# plt.savefig('query_performance_chart.png', dpi=300, bbox_inches='tight')
# plt.savefig('query_performance_chart.pdf', bbox_inches='tight')
#
# # Show the plot
# plt.show()
#
# print("Chart created and saved as 'query_performance_chart.png' and 'query_performance_chart.pdf'")

import matplotlib.pyplot as plt
import numpy as np

# Data
queries = ['Q1_Simple_Filter', 'Q2_Simple_Join_Filter', 'Q3_MultiJoin_TextSearch',
           'Q4_Join_Aggregation', 'Q5_Complex_Top10']

with_indexes = [424.7, 671.16, 2.51, 1.17, 2312.97]
without_indexes = [1000000.7, 756.1, 4634.75, 24.15, 3957.74]

# Create the visualization
plt.figure(figsize=(12, 8))
x_pos = np.arange(len(queries))
bar_width = 0.35

plt.bar(x_pos - bar_width / 2, without_indexes, bar_width, label='Without Indexes', alpha=0.8, color='red')
plt.bar(x_pos + bar_width / 2, with_indexes, bar_width, label='With Indexes', alpha=0.8, color='green')

plt.xlabel('Queries')
plt.ylabel('Execution Time (ms) - Log Scale')
plt.title('Impact of Indexing on Query Performance (1 Million Records)')
plt.yscale('log')  # Using log scale due to huge differences
plt.xticks(x_pos, queries, rotation=45, ha='right')
plt.legend()
plt.tight_layout()

# Add value labels on bars
for i, v in enumerate(without_indexes):
    plt.text(i - bar_width / 2, v * 1.1, f'{v:.2f}', ha='center', fontsize=8)

for i, v in enumerate(with_indexes):
    plt.text(i + bar_width / 2, v * 1.1, f'{v:.2f}', ha='center', fontsize=8)

plt.show()

# Calculate performance improvement
improvement = [(without_indexes[i] - with_indexes[i]) / without_indexes[i] * 100 for i in range(len(queries))]

print("Performance Improvement by Query:")
for i, query in enumerate(queries):
    print(f"{query}: {improvement[i]:.2f}% improvement")