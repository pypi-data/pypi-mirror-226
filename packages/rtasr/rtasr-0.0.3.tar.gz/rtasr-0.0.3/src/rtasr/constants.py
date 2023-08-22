"""Define all the constants used in rtasr."""

from typing import OrderedDict

DATASETS = OrderedDict(
    [
        (
            "ami",
            {
                "splits": ["test", "dev", "train"],
                "audio_types": ["Mix-Headset", "Array1-01"],
                "urls": {
                    "rttm": "https://raw.githubusercontent.com/BUTSpeechFIT/AMI-diarization-setup/main/only_words/rttms/{}/{}.rttm",
                    "uem": "https://raw.githubusercontent.com/BUTSpeechFIT/AMI-diarization-setup/main/uems/{}/{}.uem",
                    "list": "https://raw.githubusercontent.com/BUTSpeechFIT/AMI-diarization-setup/main/lists/{}.meetings.txt",
                },
                "exclude_ids": ["IS1007d", "IS1003b"],
                "manifest_filepaths": {
                    "test": [
                        "test/manifest_Array1-01.json",
                        "test/manifest_Mix-Headset.json",
                    ],
                    "dev": [
                        "dev/manifest_Array1-01.json",
                        "dev/manifest_Mix-Headset.json",
                    ],
                    "train": [
                        "train/manifest_Array1-01.json",
                        "train/manifest_Mix-Headset.json",
                    ],
                },
            },
        ),
        (
            "voxconverse",
            {
                "splits": ["dev", "test"],
                "zip_urls": {
                    "rttm": "https://github.com/joonson/voxconverse/archive/refs/heads/master.zip",
                    "dev": "https://www.robots.ox.ac.uk/~vgg/data/voxconverse/data/voxconverse_dev_wav.zip",
                    "test": "https://www.robots.ox.ac.uk/~vgg/data/voxconverse/data/voxconverse_test_wav.zip",
                },
                "filepaths": {
                    "dev": "dev/audio",
                    "test": "test/voxconverse_test_wav",
                    "rttm": "rttm/voxconverse-master",
                },
                "manifest_filepaths": {
                    "dev": ["dev_manifest.json"],
                    "test": ["test_manifest.json"],
                },
            },
        ),
    ]
)
PROVIDERS = OrderedDict(
    [
        (
            "assemblyai",
            {
                "url": "https://api.assemblyai.com/v2",
                "engine": "AssemblyAI",
                "concurrency_limit": 5,
                "options": {
                    "speaker_labels": True,
                    "punctuate": True,
                },
            },
        ),
        (
            "aws",
            {
                "url": "",
                "engine": "Aws",
            },
        ),
        (
            "azure",
            {
                "url": "",
                "engine": "Azure",
            },
        ),
        (
            "deepgram",
            {
                "url": "https://api.deepgram.com/v1/listen",
                "engine": "Deepgram",
                "options": {
                    "diarize": True,
                    "model": "nova",
                    "punctuate": True,
                    "utterances": True,
                },
            },
        ),
        (
            "google",
            {
                "url": "",
                "engine": "Google",
            },
        ),
        (
            "revai",
            {
                "url": "",
                "engine": "RevAI",
            },
        ),
        (
            "speechmatics",
            {
                "url": "",
                "engine": "Speechmatics",
            },
        ),
        (
            "wordcab",
            {
                "url": "https://wordcab.com/api/v1",
                "engine": "Wordcab",
                "options": {
                    "alignment": False,
                    "diarize": True,
                    "dual_channel": False,
                    "only_api": False,
                    "source": "audio",
                },
            },
        ),
    ]
)
