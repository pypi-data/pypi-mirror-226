import numpy as np
import torch
import zero

from .gaussian_multinomial_diffusion import GaussianMultinomialDiffusion
from .lib import Transformations
from .utils_train import get_model, make_dataset


def to_good_ohe(ohe, X):
    indices = np.cumsum([0] + ohe._n_features_outs)
    Xres = []
    for i in range(1, len(indices)):
        x_ = np.max(X[:, indices[i - 1]:indices[i]], axis=1)
        t = X[:, indices[i - 1]:indices[i]] - x_.reshape(-1, 1)
        Xres.append(np.where(t >= 0, 1, 0))
    return np.hstack(Xres)


def sample(
        parent_dir,
        real_data_path='data/higgs-small',
        batch_size=2000,
        num_samples=0,
        model_type='mlp',
        model_params=None,
        model=None,
        model_path=None,
        num_timesteps=1000,
        gaussian_loss_type='mse',
        scheduler='cosine',
        T_dict=None,
        num_numerical_features=0,
        disbalance=None,
        device=torch.device('cuda:1'),
        seed=0,
        change_val=False
):
    zero.improve_reproducibility(seed)

    T = Transformations(**T_dict)
    D = make_dataset(
        real_data_path,
        T,
        num_classes=model_params['num_classes'],
        is_y_cond=model_params['is_y_cond'],
        change_val=change_val
    )

    K = np.array(D.get_category_sizes('train'))
    if len(K) == 0 or T_dict['cat_encoding'] == 'one-hot':
        K = np.array([0])

    num_numerical_features_ = D.X_num['train'].shape[1] if D.X_num is not None else 0
    d_in = np.sum(K) + num_numerical_features_
    model_params['d_in'] = int(d_in)

    if model is None:
        model = get_model(
            model_type,
            model_params,
            num_numerical_features_,
            category_sizes=D.get_category_sizes('train')
        )

        model.load_state_dict(
            torch.load(model_path, map_location="cpu")
        )

    diffusion = GaussianMultinomialDiffusion(
        K,
        num_numerical_features=num_numerical_features_,
        denoise_fn=model, num_timesteps=num_timesteps,
        gaussian_loss_type=gaussian_loss_type, scheduler=scheduler, device=device
    )

    diffusion.to(device)
    diffusion.eval()

    _, empirical_class_dist = torch.unique(torch.from_numpy(D.y['train']), return_counts=True)
    # empirical_class_dist = empirical_class_dist.float() + torch.tensor([-5000., 10000.]).float()
    if disbalance == 'fix':
        empirical_class_dist[0], empirical_class_dist[1] = empirical_class_dist[1], empirical_class_dist[0]
        x_gen, y_gen = diffusion.sample_all(num_samples, batch_size, empirical_class_dist.float(), ddim=False)

    elif disbalance == 'fill':
        ix_major = empirical_class_dist.argmax().item()
        val_major = empirical_class_dist[ix_major].item()
        x_gen, y_gen = [], []
        for i in range(empirical_class_dist.shape[0]):
            if i == ix_major:
                continue
            distrib = torch.zeros_like(empirical_class_dist)
            distrib[i] = 1
            num_samples = val_major - empirical_class_dist[i].item()
            x_temp, y_temp = diffusion.sample_all(num_samples, batch_size, distrib.float(), ddim=False)
            x_gen.append(x_temp)
            y_gen.append(y_temp)

        x_gen = torch.cat(x_gen, dim=0)
        y_gen = torch.cat(y_gen, dim=0)

    else:
        x_gen, y_gen = diffusion.sample_all(num_samples, batch_size, empirical_class_dist.float(), ddim=False)

    # try:
    # except FoundNANsError as ex:
    #     print("Found NaNs during sampling!")
    #     loader = lib.prepare_fast_dataloader(D, 'train', 8)
    #     x_gen = next(loader)[0]
    #     y_gen = torch.multinomial(
    #         empirical_class_dist.float(),
    #         num_samples=8,
    #         replacement=True
    #     )
    X_gen, y_gen = x_gen.numpy(), y_gen.numpy()

    return X_gen, y_gen
