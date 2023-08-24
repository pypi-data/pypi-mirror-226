import torch
from torch.utils.data import DataLoader
from .utils import sequence_padding


def param_groups_lrd(model, num_layers, lr, weight_decay=0.1, layer_decay=1.):
    param_group_names = {}
    param_groups = {}
    layer_scales = list(layer_decay ** (num_layers - i) for i in range(num_layers + 1))
    for n, p in model.named_parameters():
        if not p.requires_grad:
            continue
        # no decay: all 1D parameters and model specific ones
        if p.ndim == 1 or 'bias' in n.lower() or 'norm' in n.lower():
            g_decay = "no_decay"
            this_decay = 0.
        else:
            g_decay = "decay"
            this_decay = weight_decay

        layer_id = get_layer_id(n, num_layers)
        group_name = "layer_%d_%s" % (layer_id, g_decay)

        if group_name not in param_group_names:
            this_scale = layer_scales[layer_id]

            param_group_names[group_name] = {
                "lr": this_scale,
                "weight_decay": this_decay,
                "params": [],
            }
            param_groups[group_name] = {
                "lr_scale": this_scale,
                "weight_decay": this_decay,
                "params": [],
            }

        param_group_names[group_name]["params"].append(n)
        param_groups[group_name]["params"].append(p)

    # print("parameter groups: \n%s" % json.dumps(param_group_names, indent=2))
    param_groups = param_groups.values()
    for param_group in param_groups:
        if "lr_scale" in param_group:
            param_group["lr"] = lr * param_group["lr_scale"]
        else:
            param_group["lr"] = lr
    return param_groups


def get_layer_id(name, num_layers):
    if 'embedding' in name:
        return 0
    elif 'encoder.layer' in name:
        idx = name.find("encoder.layer.")
        layer_id = int(name[idx + len("encoder.layer."):].split('.')[0]) + 1
        return layer_id
    else:
        return num_layers


def create_optimizer(model, args, num_layers):
    param_groups = param_groups_lrd(model, num_layers, args.lr, weight_decay=args.weight_decay,
                                    layer_decay=args.layer_decay)
    optimizer = torch.optim.AdamW(param_groups, lr=args.lr)
    return optimizer


def dict_collate(batch, config=None):
    keys = list(batch[0].keys())
    kwargs = [dict(length=None, value=0, seq_dims=1, mode='post', dtype='int64') for _ in range(len(keys))]
    if config is not None:
        for k, v in config.items():
            kwargs[keys.index(k)].update(v)
    values = zip(*[_.values() for _ in batch])
    values = [torch.from_numpy(sequence_padding(x, **c)) for x, c in zip(values, kwargs)]
    return dict(zip(keys, values))


def list_collate(batch, config=None):
    batch = list(zip(*batch))
    kwargs = [dict(length=None, value=0, seq_dims=1, mode='post', dtype='int64') for _ in range(len(batch))]
    if config is not None:
        for idx, c in config.items():
            kwargs[idx].update(c)
    return [torch.from_numpy(sequence_padding(x, **c)) for x, c in zip(batch, kwargs)]


def create_dataloader(args, dataset, collate_config=None, sampler=None, shuffle=None):
    collate_fn = dict_collate
    if collate_config == 'list':
        collate_fn = list_collate
    elif isinstance(collate_config, dict):
        if 'type' in collate_config:
            collate_config.pop('type')
            collate_fn = list_collate
        from functools import partial
        collate_fn = partial(collate_fn, config=collate_config)

    return DataLoader(dataset, args.batch_size, shuffle, batch_sampler=sampler, collate_fn=collate_fn,
                      num_workers=args.num_workers)


def train_step(model, batch, criterion, accelerator, args):
    output = forward_model(model, batch)
    loss = criterion(output, batch)
    accelerator.backward(loss / args.accumulate_grad_batches)
    return loss


def forward_model(model, batch):
    if isinstance(batch, dict):
        output = model(**batch)
    else:
        output = model(*batch)
    return output
