from mlc.dataloaders.dataloader import BaseDataLoader


class SDVDataLoader(BaseDataLoader):
    def __init__(self, num_workers: int = 4, pretrained_path: str = None, save_path: str = None) -> None:
        self.num_workers = num_workers
        if pretrained_path is None:
            print("fitting generator")
            self.generator.fit(self.data)
        else:
            self.load(pretrained_path)
        if save_path is not None:
            self.save(save_path)

    def load(self, pretrained_path: str):
        self.generator._model.load(pretrained_path)

    def save(self, save_path: str):
        self.generator._model.save(save_path)
