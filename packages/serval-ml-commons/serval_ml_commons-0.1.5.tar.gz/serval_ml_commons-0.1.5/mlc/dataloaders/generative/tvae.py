from sdv.metadata import SingleTableMetadata
from sdv.single_table import TVAESynthesizer

from mlc.dataloaders.generative.ctgan import CTGANDataLoader
from mlc.dataloaders.sdv import SDVDataLoader
from mlc.datasets.dataset import Dataset


class GaussianCopulaDataLoader(CTGANDataLoader):
    def __init__(self, num_workers: int = 4, original_dataset: Dataset = None, scaler=None, vae_params: dict = {},
                 filter_constraints: bool = False, pretrained_path: str = None, save_path: str = None) -> None:
        self.dataset = original_dataset
        self.scaler = scaler
        self.filter_constraints = filter_constraints

        metadata = SingleTableMetadata()
        metadata.detect_from_dataframe(data=self.dataset.get_data())

        self.generator = TVAESynthesizer(metadata, **vae_params)
        SDVDataLoader.__init__(num_workers, pretrained_path, save_path)
