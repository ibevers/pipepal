"""This module implements some utilities for the speech-to-text task."""
from typing import Any, Dict, Optional

from datasets import Dataset
from transformers import pipeline

from senselab.utils.functions import _select_device_and_dtype
from senselab.utils.hf import HFModel
from senselab.utils.tasks.input_output import _from_dict_to_hf_dataset, _from_hf_dataset_to_dict


def transcribe_dataset_with_hf(dataset: Dict[str, Any], 
                               audio_column: str = 'audio',
                               model_id: str = "openai/whisper-tiny", 
                               language: Optional[str] = None,
                               return_timestamps: Optional[str] = 'word',
                               max_new_tokens: int = 128,
                               chunk_length_s: int = 30,
                               batch_size: int = 16
                               ) -> Dict[str, Any]:
    """Transcribes all audio samples in the dataset."""
    _ = HFModel(model_id=model_id) # check HF model is valid
    hf_dataset = _from_dict_to_hf_dataset(dataset)

    def _prepare_hf_asr_pipeline(
        model_id: str,
        language: Optional[str] = None,
        return_timestamps: Optional[str] = 'word',
        max_new_tokens: int = 128,
        chunk_length_s: int = 30,
        batch_size: int = 16
    ) -> pipeline:
        """Prepare a Hugging Face ASR pipeline."""
        _ = HFModel(model_id=model_id) # check HF model is valid

        device, torch_dtype = _select_device_and_dtype(device_options=['cuda', 'cpu']) 
        # TODO: dinamically check if 'mps' is supported by the model before excluding it a priori

        pipe = pipeline("automatic-speech-recognition", 
                        model=model_id, 
                        return_timestamps=return_timestamps, 
                        max_new_tokens=max_new_tokens,
                        chunk_length_s=chunk_length_s,
                        batch_size=batch_size,
                        device=device, 
                        torch_dtype=torch_dtype)
        return pipe

    pipe = _prepare_hf_asr_pipeline(model_id=model_id, 
                                    language=language,
                                    return_timestamps=return_timestamps, 
                                    max_new_tokens=max_new_tokens,
                                    chunk_length_s=chunk_length_s,
                                    batch_size=batch_size)

    def _transcribe_batch_with_hf_asr_pipeline(batch: Dataset, pipe: pipeline, language: Optional[str] = None, audio_column_name: str = "audio") -> Dict[str, Any]:
        """Transcribes a batch of audio samples."""
        if language is None:
            transcriptions = pipe(batch[audio_column_name])
        else:
            transcriptions = pipe(batch[audio_column_name], generate_kwargs = {"language":f"<|{language}|>"})
        return {"asr": transcriptions}

    transcript_dataset = hf_dataset.map(_transcribe_batch_with_hf_asr_pipeline, batched=True, batch_size=16, fn_kwargs={"pipe": pipe})
    transcript_dataset = transcript_dataset.remove_columns([audio_column])
    print(transcript_dataset)
    return _from_hf_dataset_to_dict(transcript_dataset)
