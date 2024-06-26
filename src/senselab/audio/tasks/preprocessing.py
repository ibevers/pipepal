"""This module implements some utilities for the preprocessing task."""
from typing import Any, Dict

import torch
import torchaudio.functional as F
from datasets import Dataset

from senselab.utils.tasks.input_output import _from_dict_to_hf_dataset, _from_hf_dataset_to_dict


def resample_hf_dataset(dataset: Dict[str, Any], resample_rate: int, rolloff: float = 0.99) -> Dict[str, Any]:
    """Resamples a Hugging Face `Dataset` object."""
    hf_dataset = _from_dict_to_hf_dataset(dataset)

    def _resample_hf_row(row: Dataset, resample_rate: int, rolloff: float = 0.99) -> Dict[str, Any]:
        """Resamples audio data in a hf dataset row.
        
        A lower rolloff will therefore reduce the amount of aliasing, but it will also reduce some of the higher frequencies.
        """
        waveform = row['audio']['array']
        # Ensure waveform is a PyTorch tensor
        if not isinstance(waveform, torch.Tensor):
            waveform = torch.tensor(waveform)
        sampling_rate = row['audio']['sampling_rate']

        resampled_waveform = F.resample(waveform, sampling_rate, resample_rate, rolloff=rolloff)

        return {'audio': {'array': resampled_waveform, 'sampling_rate': resample_rate}}

    resampled_hf_dataset = hf_dataset.map(lambda x: _resample_hf_row(x, resample_rate, rolloff))
    return _from_hf_dataset_to_dict(resampled_hf_dataset)
