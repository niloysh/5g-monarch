from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

class BaseSampler(ABC):
    def __init__(self):
        self.sampled_df = pd.DataFrame(columns=['value'])

    @abstractmethod
    def sample(self, timestamp, value):
       pass

    def get_sampled_df(self):
        return self.sampled_df
    

class FixedFrequencySampler(BaseSampler):
    def __init__(self, frequency):
        super().__init__()
        self.frequency = frequency
        self.last_sampled_timestamp = None

    def sample(self, timestamp, value):
        if self.last_sampled_timestamp is None \
        or (timestamp - self.last_sampled_timestamp).total_seconds() >= self.frequency:
            self.sampled_df.loc[timestamp] = {'value': value}  # Set 'timestamp' as the index
            self.last_sampled_timestamp = timestamp


class AdaptiveSampler(BaseSampler):
    def __init__(self, threshold: float = 0.01) -> None:
        super().__init__()
        self.threshold = threshold
        self.last_sampled_timestamp = None
        self.last_sampled_value = None
        self.min_interval = 3
        self.max_interval = 10
        self.sampling_interval = self.min_interval
        self.max_value = -np.inf
        self.min_value = np.inf
        self.increase_factor = 1.5
        self.decrease_factor = 0.5

    def sample_datapoint(self, timestamp, value):

        # sample the data point
        self.sampled_df.loc[timestamp] = {'value': value}
        self.last_sampled_timestamp = timestamp
        self.last_sampled_value = value

        # update the min and max values
        self.max_value = max(self.max_value, value)
        self.min_value = min(self.min_value, value)
       
        
    def sample(self, timestamp, value):

        print(f"Sampling interval: {self.sampling_interval}")

        if self.last_sampled_timestamp is None:
            self.sample_datapoint(timestamp, value)
            return

        self.update_sampling_interval(value)
        if self.is_time_to_sample(timestamp):
            self.sample_datapoint(timestamp, value)

    def is_time_to_sample(self, timestamp):
        elapsed_time = (timestamp - self.last_sampled_timestamp).total_seconds()
        return elapsed_time >= self.sampling_interval
        
    def is_significant_change(self, value):
        change = abs(value - self.last_sampled_value)
        relative_change = change / value
        # print(f"Relative Change: {relative_change:.6f}, Threshold: {self.threshold:.6f}")
        return relative_change > self.threshold

    def update_sampling_interval(self, value):
        if self.is_significant_change(value):
            # self.sampling_interval = max(self.min_interval, self.sampling_interval - 1)
            self.sampling_interval = max(self.min_interval, int(self.sampling_interval * self.decrease_factor))
        else:
            # self.sampling_interval = min(self.max_interval, self.sampling_interval + 2)
            self.sampling_interval = min(self.max_interval, int(self.sampling_interval * self.increase_factor))


    


   
