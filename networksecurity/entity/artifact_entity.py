# dataclasses act as a decorator which adds a variable for an empty class
from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file_path: str
    test_file_path:str