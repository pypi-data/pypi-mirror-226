from sdv.metadata import SingleTableMetadata
from sdv.single_table import CopulaGANSynthesizer
from sdv.single_table import GaussianCopulaSynthesizer

from mlc.dataloaders.generative.ctgan import CTGANDataLoader
from mlc.dataloaders.sdv import SDVDataLoader
from mlc.datasets.dataset import Dataset


class GaussianCopulaDataLoader(CTGANDataLoader):
    def __init__(self, num_workers: int = 4, original_dataset: Dataset = None, scaler=None, copula_params: dict = {},
                 filter_constraints: bool = False, pretrained_path: str = None, save_path: str = None) -> None:
        self.num_workers = num_workers
        self.dataset = original_dataset
        self.scaler = scaler
        self.filter_constraints = filter_constraints

        metadata = SingleTableMetadata()
        metadata.detect_from_dataframe(data=self.dataset.get_data())

        self.generator = GaussianCopulaSynthesizer(metadata, **copula_params)
        SDVDataLoader.__init__(num_workers, pretrained_path, save_path)


class GANCopulaDataLoader(CTGANDataLoader):
    def __init__(self, num_workers: int = 4, original_dataset: Dataset = None, scaler=None, copula_params: dict = {},
                 filter_constraints: bool = False, pretrained_path: str = None, save_path: str = None) -> None:
        self.num_workers = num_workers
        self.dataset = original_dataset
        self.scaler = scaler
        self.filter_constraints = filter_constraints

        metadata = SingleTableMetadata()
        metadata.detect_from_dataframe(data=self.dataset.get_data())

        self.generator = CopulaGANSynthesizer(metadata, **copula_params)
        SDVDataLoader.__init__(num_workers, pretrained_path, save_path)
