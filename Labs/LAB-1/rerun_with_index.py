import pandas as pd
from refresh import refresh
from data_insertion import main as insert_data, verify_insertion
from indexing import create_indexes
from queries import run_benchmarks  # reuse your existing benchmark function

if __name__ == "__main__":
    print("\n=== Preparing dataset: 1M students ===")
    refresh()
    insert_data(scale=1000000)
    verify_insertion()

    print("\n=== Creating indexes ===")
    create_indexes()

    print("\n=== Running benchmarks WITH indexes ===")
    results_with_index = run_benchmarks(runs=3)

    df = pd.DataFrame([results_with_index], index=["With Indexes"])
    print("\nResults (With Indexes):")
    print(df)

    df.to_excel("query_results_with_index.xlsx", sheet_name="With Index")
    print("\n✅ Results saved to 'query_results_with_index.xlsx'")
