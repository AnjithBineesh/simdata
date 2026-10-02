from pathlib import Path


class DatasetManager:

    def __init__(self):
        self.builtin_path = (
            Path(__file__).parent / "builtin"
        )

    def get_builtin(self, name: str) -> Path:

        dataset_path = self.builtin_path / f"{name}.bag"

        if not dataset_path.exists():
            raise FileNotFoundError(
                f"Built-in dataset not found: {name}"
            )

        return dataset_path