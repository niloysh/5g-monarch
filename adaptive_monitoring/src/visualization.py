import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from itertools import cycle
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, zoomed_inset_axes, mark_inset

plt.rcParams.update({
    "axes.labelsize": 10,
    "font.size": 10,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "text.usetex": True,
    "font.family": "serif",
    "figure.figsize": [4.5, 4.5],
    "legend.fancybox": False,
    "legend.frameon": True,
    "legend.edgecolor": "black"
})

def plot_timeseries(original_df, sampled_df_list, sampled_df_labels, x_label, y_label, title, filename, scale_factor=1):

    fig_width = 6
    num_series = len(sampled_df_list) 
    fig_height = 2 * num_series

    original_seconds = (original_df.index - original_df.index[0]).total_seconds()

    fig, ax = plt.subplots(num_series, 1, sharex=True)
    for i, (sampled_series, label) in enumerate(zip(sampled_df_list, sampled_df_labels)):

        # Convert the sampled series index to seconds from start
        sampled_seconds = (sampled_series.index - original_df.index[0]).total_seconds()

        original_values = original_df['value'] / scale_factor
        sampled_values = sampled_series['value'] / scale_factor

        ax[i].plot(original_seconds, original_values, label='original', linestyle='-', color='blue')
        ax[i].plot(sampled_seconds, sampled_values, label=label, marker='.', linestyle='-', color='red')
        ax[i].set_ylabel(y_label)
        ax[i].legend(loc='best')
        ax[i].grid(True, linestyle='--', alpha=0.3)

    plt.xlabel(x_label)
    plt.tight_layout()
    plt.savefig(filename, format='pdf', bbox_inches='tight', dpi=300)

def plot_timeseries_v2(original_df, sampled_df_list, sampled_df_labels, x_label, y_label, title, filename, scale_factor=1, zoom_range=(75, 125)):

    fig_width = 6
    num_series = len(sampled_df_list)
    fig_height = 2 * num_series

    original_seconds = (original_df.index - original_df.index[0]).total_seconds()

    fig, ax = plt.subplots(num_series, 1, sharex=True, figsize=(fig_width, fig_height))
    for i, (sampled_series, label) in enumerate(zip(sampled_df_list, sampled_df_labels)):

        # Convert the sampled series index to seconds from start
        sampled_seconds = (sampled_series.index - original_df.index[0]).total_seconds()

        original_values = original_df['value'] / scale_factor
        sampled_values = sampled_series['value'] / scale_factor

        ax[i].plot(original_seconds, original_values, label='original', linestyle='-', color='blue')
        ax[i].plot(sampled_seconds, sampled_values, label=label, marker='.', linestyle='--', color='red', alpha=0.8)
        # ax[i].set_ylabel(y_label)
        ax[i].legend(loc='best')
        ax[i].grid(True, linestyle='--', alpha=0.3)

        if zoom_range:  # Add zoomed-in inset to the first subplot
            axins = zoomed_inset_axes(ax[i], zoom=3, loc='upper center')
            # axins = inset_axes(ax[i], width="40%", height="40%", loc='upper center', borderpad=2)
            axins.plot(original_seconds, original_values, color='blue')
            axins.plot(sampled_seconds, sampled_values, marker='.', linestyle='--', color='red', alpha=0.7)

            # Determine the range and add padding
            ymin, ymax = min(original_values[zoom_range[0]:zoom_range[1]]), max(original_values[zoom_range[0]:zoom_range[1]])
            ypadding = (ymax - ymin) * 0.1  # 10% padding on each side

            axins.set_xlim(zoom_range[0], zoom_range[1])  # Set the limits of the zoomed-in portion
            axins.set_ylim(ymin - ypadding, ymax + ypadding)  # Apply padded limits

            # axins.set_xlim(zoom_range[0], zoom_range[1])  # Set the limits of the zoomed-in portion
            # axins.set_ylim(min(original_values[zoom_range[0]:zoom_range[1]]), max(original_values[zoom_range[0]:zoom_range[1]]))  # Optional: adjust the y-axis limits
            axins.grid(True, linestyle='--', alpha=0.3)
            axins.xaxis.label.set_visible(False)  # Hide the x-axis label

            mark_inset(ax[i], axins, loc1=2, loc2=4, fc="none", ec="0.5")  # Mark the zoomed-in region

    fig.supxlabel(x_label)
    fig.supylabel(y_label)
    # ax.xaxis.label.set_visible(True)  # Show the x-axis label
    plt.tight_layout()
    plt.savefig(filename, format='pdf', bbox_inches='tight', dpi=300)

def plot_distribution(original_df, sampled_df_list, sampled_df_labels, x_label, y_label, title, filename, scale_factor=1):

    fig_height = 4
    fig_width = 6

    all_values = [original_df['value'] / scale_factor] + [sampled_df['value'] / scale_factor for sampled_df in sampled_df_list]
    # Include the label for the original dataframe
    all_labels = ['Original'] + list(sampled_df_labels)

    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=300)

    flierprops = dict(marker='o', color='red', markersize=5, linestyle='none', markeredgecolor='black')
    
    # Plotting all series vertically
    # Set vert=False for horizontal boxplots
    ax.boxplot(all_values, vert=False, labels=all_labels, patch_artist=True, flierprops=flierprops)  
    
    ax.set_ylabel(x_label, fontsize=14)  # Now y-axis will have what is conceptually x-axis labels
    ax.set_xlabel(y_label, fontsize=14)  # And vice-versa for x-axis
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    ax.grid(True, linestyle='--', alpha=0.6, which='both', axis='x')  # Enable grid on x-axis

    plt.tight_layout()
    plt.savefig(filename, format='png', bbox_inches='tight', dpi=300)
        

def plot_error_timeseries(error_list, error_labels, x_label, y_label, title, filename):

    num_series = len(error_list)
    fig_height = 2 * num_series
    fig_width = 6

    # Find global minimum and maximum across all error series
    global_min = min(min(errors) for errors in error_list)
    global_max = max(max(errors) for errors in error_list)

    fig, ax = plt.subplots(num_series, figsize=(fig_width, fig_height), dpi=300)
    for i, (errors, label) in enumerate(zip(error_list, error_labels)):
        ax[i].plot(errors, label=label)
        ax[i].set_xlabel(x_label)
        ax[i].set_ylabel(y_label)
        ax[i].set_title(title)
        ax[i].legend(loc='best')
        ax[i].grid(True, linestyle='--', alpha=0.6)

        # Set the same y-axis limits based on the global min and max
        ax[i].set_ylim([global_min, global_max])
    
    plt.tight_layout()
    plt.savefig(filename, format='png', bbox_inches='tight', dpi=300)


def plot_error_distribution(error_list, error_labels, x_label, y_label, title, filename):
    fig_height = 4
    fig_width = 6

    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=300)

    flierprops = dict(marker='o', color='red', markersize=5, linestyle='none', markeredgecolor='black')
    
    # Plotting all series vertically
    # Set vert=False for horizontal boxplots
    ax.boxplot(error_list, vert=False, labels=error_labels, patch_artist=True, flierprops=flierprops)  
    
    ax.set_ylabel(x_label, fontsize=14)  # Now y-axis will have what is conceptually x-axis labels
    ax.set_xlabel(y_label, fontsize=14)  # And vice-versa for x-axis
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    ax.grid(True, linestyle='--', alpha=0.6, which='both', axis='x')  # Enable grid on x-axis

    plt.tight_layout()
    plt.savefig(filename, format='png', bbox_inches='tight', dpi=300)

def plot_psd(original_df, sampled_df_list, sampled_df_labels, x_label, y_label, title, filename, scale_factor=1):
    fig_height = 4
    fig_width = 6

    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=300)

    original_values = original_df['value'] / scale_factor
    sampled_values = [sampled_df['value'] / scale_factor for sampled_df in sampled_df_list]
    
    # Plot the PSD of the original series on the specific Axes object
    ax.psd(original_values, NFFT=256, Fs=1, label='Original')  # Adjust NFFT and Fs as needed

    for sampled_series, label in zip(sampled_values, sampled_df_labels):
        # Plot the PSD of each sampled series on the same Axes object
        ax.psd(sampled_series, NFFT=256, Fs=1, label=label)  # Adjust NFFT and Fs as needed

    ax.set_xlabel(x_label)
    ax.set_ylabel('Power/Frequency (dB/Hz)')
    ax.set_title(title)
    ax.legend(loc='best')

    plt.tight_layout()
    plt.savefig(filename, format='png', bbox_inches='tight', dpi=300)

def moving_average(data, window_size):
    """Calculate the moving average using a simple sliding window approach."""
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

def plot_error_timeseries_smooth(error_list, error_labels, x_label, y_label, title, filename, smoothing_window=5, subplots=True):
    num_series = len(error_list)
    fig_height = 2 * num_series
    fig_width = 6

    def _with_subplots():
        custom_colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
        cycle_colors = cycle(custom_colors)

        # Smooth each error series based on the provided window size
        smoothed_error_list = []
        for errors in error_list:
            if smoothing_window > 1:
                smoothed_errors = moving_average(errors, smoothing_window)
            else:
                smoothed_errors = errors  # No smoothing applied
            smoothed_error_list.append(smoothed_errors)

        # Find global minimum and maximum across all smoothed error series
        global_min = min(min(errors) for errors in smoothed_error_list)
        global_max = max(max(errors) for errors in smoothed_error_list)

        fig, ax = plt.subplots(num_series, sharex=True)
        if num_series == 1:
            ax = [ax]  # Ensure ax is iterable for a single series case
        for i, (errors, label) in enumerate(zip(smoothed_error_list, error_labels)):
            current_color = next(cycle_colors)
            ax[i].plot(errors, label=label, color=current_color)
            ax[i].set_ylabel(y_label)
            ax[i].legend(loc='best')
            ax[i].grid(True, linestyle='--', alpha=0.6)

            # Set the same y-axis limits based on the global min and max
            ax[i].set_ylim([global_min, global_max])
        
        plt.xlabel(x_label)
        plt.tight_layout()
        plt.savefig(filename, format='pdf', bbox_inches='tight', dpi=300)
   
    def _without_subplots():
        # Define custom colors and markers
        custom_colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
        custom_linestyles = ['solid', 'dashed', 'dashdot', 'dotted']
        cycle_colors = cycle(custom_colors)
        cycle_linestyles = cycle(custom_linestyles)

        # Smooth each error series based on the provided window size
        smoothed_error_list = []
        for errors in error_list:
            if smoothing_window > 1:
                smoothed_errors = moving_average(errors, smoothing_window)
            else:
                smoothed_errors = errors  # No smoothing applied
            smoothed_error_list.append(smoothed_errors)

        # Create a single plot for all error series
        fig, ax = plt.subplots(figsize=(6, 4))  # Adjust the figure size as needed

        for errors, label in zip(smoothed_error_list, error_labels):
            current_color = next(cycle_colors)
            current_linestyle = next(cycle_linestyles)
            ax.plot(errors, label=label, color=current_color, linestyle=current_linestyle, markersize=5)

        ax.set_ylabel(y_label)
        ax.set_xlabel(x_label)
        ax.legend(loc='best', fontsize='small')
        ax.grid(True, linestyle='--', alpha=0.3)
        plt.tight_layout()
        plt.savefig(filename, format='pdf', bbox_inches='tight', dpi=300)

    if subplots:
        _with_subplots()
    else:
        _without_subplots()