import argparse
import logging
import os
from src.sampling import FixedFrequencySampler, AdaptiveSampler
from src.utils import mean_absolute_error, preprocess_data, truncate_df, pointwise_absolute_error, mean_absolute_percentage_error, compression_ratio
from src.visualization import plot_timeseries, plot_error_timeseries, plot_distribution, plot_error_distribution, plot_psd, plot_error_timeseries_smooth, plot_timeseries_v2
import src.config as config
import yaml

def run(df, sampler):
    """Run the sampling algorithm on the dataset."""
    log_interval = 1000  # Log every N rows
    for i, (timestamp, value) in enumerate(df.iterrows()):
        sampler.sample(timestamp, value["value"])

        if i % log_interval == 0:
            logging.info(f"Processed {i} rows.")
    return sampler.get_sampled_df()

def load_dataset(file_path, truncate=False, truncate_date="2023-12-06 18:45:00", truncate_size=500):
    """Load the dataset and preprocess it."""
    df = preprocess_data(file_path, normalize=False)
    if truncate:
        df = truncate_df(df, truncate_date, truncate_size)

    logging.info(f"Loaded dataset with {df.shape[0]} rows.")
    return df

 
def main(kpi_name, kpi_config):

    file_path = kpi_config["path"]
    figures_dir = f"figures/{kpi_name}"
    os.makedirs(figures_dir, exist_ok=True)

    logging.basicConfig(level=logging.INFO)
    df = load_dataset(file_path, truncate=True, truncate_size=300)

    sampled_dfs = {}
    sampled_mae = {}
    sampled_pointwise_errors = {}
    sampled_mape = {}
    compression_ratios = {}

    scale_factor = kpi_config["scale_factor"]
    y_label = kpi_config["unit"]

    if settings["schemes"]["ff5"]:
        logging.info("Using Fixed Frequency Sampler (5s)...")
        ff5_sampler = FixedFrequencySampler(frequency=5)
        df_ff5 = run(df, ff5_sampler)
        mean_ff5_error = mean_absolute_error(df, df_ff5, scale_factor)
        sampled_dfs["ff5"] = df_ff5
        sampled_mae["ff5"] = mean_ff5_error
        sampled_pointwise_errors["ff5"] = pointwise_absolute_error(df, df_ff5, scale_factor)
        mape_ff5 = mean_absolute_percentage_error(df, df_ff5, scale_factor)
        sampled_mape["ff5"] = mape_ff5
        compression_ratios["ff5"] = compression_ratio(df, df_ff5)

    if settings["schemes"]["ff10"]:
        logging.info("Using Fixed Frequency Sampler (10s)...")
        ff10_sampler = FixedFrequencySampler(frequency=10)
        df_ff10 = run(df, ff10_sampler)
        mean_ff10_error = mean_absolute_error(df, df_ff10, scale_factor)
        sampled_dfs["ff10"] = df_ff10
        sampled_mae["ff10"] = mean_ff10_error
        sampled_pointwise_errors["ff10"] = pointwise_absolute_error(df, df_ff10, scale_factor)
        mape_ff10 = mean_absolute_percentage_error(df, df_ff10, scale_factor)
        sampled_mape["ff10"] = mape_ff10
        compression_ratios["ff10"] = compression_ratio(df, df_ff10)


    if settings["schemes"]["adaptive"]:
        logging.info("Using Adaptive Sampler...")
        adaptive_push_sampler = AdaptiveSampler(threshold=0.01)  # increase == more compression
        df_adaptive_push = run(df, adaptive_push_sampler)
        mean_adaptive_push_error = mean_absolute_error(df, df_adaptive_push, scale_factor)
        sampled_dfs["adaptive"] = df_adaptive_push
        sampled_mae["adaptive"] = mean_adaptive_push_error
        sampled_pointwise_errors["adaptive"] = pointwise_absolute_error(df, df_adaptive_push, scale_factor)
        mape_adaptive_push = mean_absolute_percentage_error(df, df_adaptive_push, scale_factor)
        sampled_mape["adaptive"] = mape_adaptive_push
        compression_ratios["adaptive"] = compression_ratio(df, df_adaptive_push)

    

    for sampling_strategy, sampled_df in sampled_dfs.items():
        print(f"MAE: {sampling_strategy: >10}: {sampled_mae[sampling_strategy]:.4f}")

    for sampling_strategy, sampled_df in sampled_dfs.items():
        print(f"MAPE: {sampling_strategy: >10}: {sampled_mape[sampling_strategy]:.4f}")

    for sampling_strategy, sampled_df in sampled_dfs.items():
        print(f"Data Savings Ratio: {sampling_strategy: >10}: {compression_ratios[sampling_strategy]:.2f}")

    for sampling_strategy, sampled_df in sampled_dfs.items():
        cr = compression_ratios[sampling_strategy]
        mape = sampled_mape[sampling_strategy]
        eru = cr / mape   # higher is better
        print(f"ERU: {sampling_strategy: >10}: {eru:.4f}")


    with open(f"{figures_dir}/mae.txt", "w") as f:
        for sampling_strategy, sampled_df in sampled_dfs.items():
            f.write(f"{sampling_strategy: >15}: {sampled_mae[sampling_strategy]:.4f}")
            f.write("\n")
    with open(f"{figures_dir}/compression.txt", "w") as f:
        for sampling_strategy, sampled_df in sampled_dfs.items():
            f.write(f"{sampling_strategy: >15}: {df.shape[0] / sampled_df.shape[0]:.2f}")
            f.write("\n")


    if sampled_dfs:

        if settings["plots"]["timeseries"]:
            plot_timeseries_v2(
            original_df=df, 
            sampled_df_list=sampled_dfs.values(), 
            sampled_df_labels=sampled_dfs.keys(), 
            x_label="Time (seconds)", 
            y_label=y_label, 
            title="Timeseries Comparison", 
            filename=f'{figures_dir}/timeseries.pdf',
            scale_factor=scale_factor)

        if settings["plots"]["distribution"]:
            plot_distribution(
            original_df=df,
            sampled_df_list=sampled_dfs.values(),
            sampled_df_labels=sampled_dfs.keys(),
            x_label="Sampling Strategy",
            y_label=y_label,
            title="Distribution Comparison",
            filename=f'{figures_dir}/distribution.png',
            scale_factor=scale_factor)

        if settings["plots"]["error_timeseries"]:
            plot_error_timeseries(
            error_list=sampled_pointwise_errors.values(),
            error_labels=sampled_pointwise_errors.keys(),
            x_label="Time (seconds)",
            y_label="Absolute Error",
            title="Error Comparison",
            filename=f'{figures_dir}/error_timeseries.png')

        if settings["plots"]["error_timeseries_smooth"]:
            plot_error_timeseries_smooth(
            error_list=sampled_pointwise_errors.values(),
            error_labels=sampled_pointwise_errors.keys(),
            x_label="Time (seconds)",
            y_label="Absolute Error",
            title="Error Comparison",
            filename=f'{figures_dir}/error_timeseries_smooth.pdf',
            smoothing_window=5,
            subplots=False
            )
        
        if settings["plots"]["error_distribution"]:
            plot_error_distribution(
            error_list=sampled_pointwise_errors.values(),
            error_labels=sampled_pointwise_errors.keys(),
            x_label="Sampling Strategy",
            y_label="Absolute Error",
            title="Error Distribution Comparison",
            filename=f'{figures_dir}/error_distribution.png')

        if settings["plots"]["psd"]:
            plot_psd(
            original_df=df,
            sampled_df_list=sampled_dfs.values(),
            sampled_df_labels=sampled_dfs.keys(),
            x_label="Frequency (Hz)",
            y_label="Power/Frequency (dB/Hz)",
            title="Power Spectral Density Comparison",
            filename=f'{figures_dir}/psd.png',
            scale_factor=scale_factor) 
        


if __name__ == "__main__":

    with open("settings.yaml", "r") as f:
        settings = yaml.safe_load(f)

    for kpi_name, kpi_config in settings["kpi"].items():
        if kpi_config["enabled"]:
            print(f"Running experiments for {kpi_name}...")
            main(kpi_name, kpi_config)
    
    