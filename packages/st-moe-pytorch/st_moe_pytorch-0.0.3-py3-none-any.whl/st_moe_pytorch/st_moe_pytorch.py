import math
from inspect import isfunction
from typing import Tuple

import torch
from torch.nn import Module
from torch import nn, einsum
import torch.nn.functional as F

from einops import rearrange, repeat, reduce, pack, unpack

from colt5_attention import topk as differentiable_topk

# constants

MIN_EXPERT_CAPACITY = 4

# helper functions

def exists(val):
    return val is not None

def default(val, default_val):
    default_val = default_val() if callable(default_val) else default_val
    return val if exists(val) else default_val

def cast_tuple(el):
    return el if isinstance(el, tuple) else (el,)

# tensor related helper functions

def top1(t):
    values, index = t.topk(k = 1, dim = -1)
    values, index = map(lambda x: rearrange(x, '... 1 -> ...'), (values, index))
    return values, index

def cumsum_exclusive(t, dim = -1):
    num_dims = len(t.shape)
    num_pad_dims = - dim - 1
    pre_padding = (0, 0) * num_pad_dims
    pre_slice   = (slice(None),) * num_pad_dims
    padded_t = F.pad(t, (*pre_padding, 1, 0)).cumsum(dim = dim)
    return padded_t[(..., slice(None, -1), *pre_slice)]

# pytorch one hot throws an error if there are out of bound indices.
# tensorflow, in contrast, does not throw an error

def safe_one_hot(indexes, max_length):
    max_index = indexes.max() + 1
    return F.one_hot(indexes, max(max_index + 1, max_length))[..., :max_length]

# expert class

class GEGLU(Module):
    def __init__(
        self,
        dim,
        mult_bias = True
    ):
        super().__init__()
        self.mult_bias = nn.Parameter(torch.ones(dim)) if mult_bias else 1.

    def forward(self, x):
        x, gate = x.chunk(2, dim = -1)
        return F.gelu(gate) * x * self.mult_bias

class Expert(Module):
    def __init__(
        self,
        dim,
        hidden_mult = 4,
        mult_bias = True,
        dropout = 0.,
    ):
        super().__init__()
        dim_hidden = int(dim * hidden_mult * 2 / 3)

        self.net = nn.Sequential(
            nn.Linear(dim, dim_hidden * 2),
            GEGLU(dim_hidden, mult_bias = mult_bias),
            nn.Dropout(dropout),
            nn.Linear(dim_hidden, dim)
        )

        self.apply(self.init_)

    def init_(self, module):
        if isinstance(module, nn.Linear):
            dim = module.weight.shape[0]
            std = dim ** -0.5

            module.weight.data.uniform_(-std, std)
            module.bias.data.uniform_(-std, std)

    def forward(self, x):
        return self.net(x)

class Experts(Module):
    def __init__(
        self,
        dim,
        num_experts = 16,
        hidden_mult = 4,
        dropout = 0.
    ):
        super().__init__()
        self.experts = nn.ModuleList([Expert(dim = dim, hidden_mult = hidden_mult, dropout = dropout) for _ in range(num_experts)])

    def forward(self, x):
        outputs = []

        for tokens, expert in zip(x, self.experts):
            outputs.append(expert(tokens))

        return torch.stack(outputs)

# the below code is almost all transcribed from the official tensorflow version, from which the papers are written
# https://github.com/tensorflow/tensor2tensor/blob/master/tensor2tensor/models/research/moe.py

# gating network

class Top2Gating(nn.Module):
    def __init__(
        self,
        dim,
        num_gates,
        eps = 1e-9,
        outer_expert_dims = tuple(),
        second_policy_train = 'random',
        second_policy_eval = 'random',
        second_threshold_train = 0.2,
        second_threshold_eval = 0.2,
        capacity_factor_train = 1.25,
        capacity_factor_eval = 2.):
        super().__init__()

        self.eps = eps
        self.num_gates = num_gates
        self.w_gating = nn.Parameter(torch.randn(*outer_expert_dims, dim, num_gates))

        self.second_policy_train = second_policy_train
        self.second_policy_eval = second_policy_eval
        self.second_threshold_train = second_threshold_train
        self.second_threshold_eval = second_threshold_eval
        self.capacity_factor_train = capacity_factor_train
        self.capacity_factor_eval = capacity_factor_eval

    def forward(self, x, importance = None):
        *_, b, group_size, dim = x.shape
        num_gates = self.num_gates

        if self.training:
            policy = self.second_policy_train
            threshold = self.second_threshold_train
            capacity_factor = self.capacity_factor_train
        else:
            policy = self.second_policy_eval
            threshold = self.second_threshold_eval
            capacity_factor = self.capacity_factor_eval

        gate_logits = einsum('... b n d, ... d e -> ... b n e', x, self.w_gating)
        raw_gates = gate_logits.softmax(dim=-1)

        # FIND TOP 2 EXPERTS PER POSITON
        # Find the top expert for each position. shape=[batch, group]

        gate_1, index_1 = top1(raw_gates)
        mask_1 = F.one_hot(index_1, num_gates).float()
        density_1_proxy = raw_gates

        if exists(importance):
            equals_one_mask = (importance == 1.).float()
            mask_1 *= equals_one_mask[..., None]
            gate_1 *= equals_one_mask
            density_1_proxy = density_1_proxy * equals_one_mask[..., None]
            del equals_one_mask

        gates_without_top_1 = raw_gates * (1. - mask_1)

        gate_2, index_2 = top1(gates_without_top_1)
        mask_2 = F.one_hot(index_2, num_gates).float()

        if exists(importance):
            greater_zero_mask = (importance > 0.).float()
            mask_2 *= greater_zero_mask[..., None]
            del greater_zero_mask

        # normalize top2 gate scores
        denom = gate_1 + gate_2 + self.eps
        gate_1 /= denom
        gate_2 /= denom

        # BALANCING LOSSES
        # shape = [batch, experts]
        # We want to equalize the fraction of the batch assigned to each expert
        density_1 = mask_1.mean(dim=-2)
        # Something continuous that is correlated with what we want to equalize.
        density_1_proxy = density_1_proxy.mean(dim=-2)
        loss = (density_1_proxy * density_1).mean() * float(num_gates ** 2)

        # Depending on the policy in the hparams, we may drop out some of the
        # second-place experts.
        if policy == "all":
            pass
        elif policy == "none":
            mask_2 = torch.zeros_like(mask_2)
        elif policy == "threshold":
            mask_2 *= (gate_2 > threshold).float()
        elif policy == "random":
            probs = torch.zeros_like(gate_2).uniform_(0., 1.)
            mask_2 *= (probs < (gate_2 / max(threshold, self.eps))).float().unsqueeze(-1)
        else:
            raise ValueError(f"Unknown policy {policy}")

        # Each sequence sends (at most?) expert_capacity positions to each expert.
        # Static expert_capacity dimension is needed for expert batch sizes
        expert_capacity = min(group_size, int((group_size * capacity_factor) / num_gates))
        expert_capacity = max(expert_capacity, MIN_EXPERT_CAPACITY)
        expert_capacity_f = float(expert_capacity)

        # COMPUTE ASSIGNMENT TO EXPERTS
        # [batch, group, experts]
        # This is the position within the expert's mini-batch for this sequence
        position_in_expert_1 = cumsum_exclusive(mask_1, dim=-2) * mask_1
        # Remove the elements that don't fit. [batch, group, experts]
        mask_1 *= (position_in_expert_1 < expert_capacity_f).float()
        # [batch, experts]
        # How many examples in this sequence go to this expert
        mask_1_count = mask_1.sum(dim=-2, keepdim=True)
        # [batch, group] - mostly ones, but zeros where something didn't fit
        mask_1_flat = mask_1.sum(dim=-1)
        # [batch, group]
        position_in_expert_1 = position_in_expert_1.sum(dim=-1)
        # Weight assigned to first expert.  [batch, group]
        gate_1 *= mask_1_flat

        position_in_expert_2 = cumsum_exclusive(mask_2, dim=-2) + mask_1_count
        position_in_expert_2 *= mask_2
        mask_2 *= (position_in_expert_2 < expert_capacity_f).float()
        mask_2_flat = mask_2.sum(dim=-1)

        position_in_expert_2 = position_in_expert_2.sum(dim=-1)
        gate_2 *= mask_2_flat
        
        # [batch, group, experts, expert_capacity]
        combine_tensor = (
            gate_1[..., None, None]
            * mask_1_flat[..., None, None]
            * F.one_hot(index_1, num_gates)[..., None]
            * safe_one_hot(position_in_expert_1.long(), expert_capacity)[..., None, :] +
            gate_2[..., None, None]
            * mask_2_flat[..., None, None]
            * F.one_hot(index_2, num_gates)[..., None]
            * safe_one_hot(position_in_expert_2.long(), expert_capacity)[..., None, :]
        )

        dispatch_tensor = combine_tensor.bool().to(combine_tensor)

        # calculate the router z-loss proposed in paper

        router_z_loss = torch.logsumexp(gate_logits, dim = -1)
        router_z_loss = reduce(router_z_loss, '... n -> ...', 'sum')

        return dispatch_tensor, combine_tensor, loss, router_z_loss.mean()

# plain mixture of experts

class MoE(nn.Module):
    def __init__(self,
        dim,
        num_experts = 16,
        expert_hidden_mult = 4,
        expert_dropout = 0.,
        second_policy_train = 'random',
        second_policy_eval = 'random',
        second_threshold_train = 0.2,
        second_threshold_eval = 0.2,
        capacity_factor_train = 1.25,
        capacity_factor_eval = 2.,
        loss_coef = 1e-2,
        router_z_loss_coef = 1e-3,
        experts = None
    ):
        super().__init__()
        self.num_experts = num_experts

        gating_kwargs = dict(
            second_policy_train = second_policy_train,
            second_policy_eval = second_policy_eval,
            second_threshold_train = second_threshold_train,
            second_threshold_eval = second_threshold_eval,
            capacity_factor_train = capacity_factor_train,
            capacity_factor_eval = capacity_factor_eval
        )

        self.gate = Top2Gating(dim, num_gates = num_experts, **gating_kwargs)
        self.experts = default(experts, lambda: Experts(dim, num_experts = num_experts, hidden_mult = expert_hidden_mult, dropout = expert_dropout))

        self.loss_coef = loss_coef
        self.router_z_loss_coef = router_z_loss_coef

    def forward(self, inputs, **kwargs):
        dispatch_tensor, combine_tensor, loss, router_z_loss = self.gate(inputs)
        expert_inputs = einsum('b n d, b n e c -> e b c d', inputs, dispatch_tensor)

        # Now feed the expert inputs through the experts.

        expert_inputs, ps = pack([expert_inputs], 'e * d')
        expert_outputs = self.experts(expert_inputs)
        expert_outputs, = unpack(expert_outputs, ps, 'e * d')

        output = einsum('e b c d, b n e c -> b n d', expert_outputs, combine_tensor)
        return output, loss * self.loss_coef, router_z_loss * self.router_z_loss_coef

# 2-level heirarchical mixture of experts

class HeirarchicalMoE(nn.Module):
    def __init__(self,
        dim,
        num_experts: Tuple[int, int] = (4, 4),
        expert_hidden_mult = 4,
        expert_dropout = 0.,
        second_policy_train = 'random',
        second_policy_eval = 'random',
        second_threshold_train = 0.2,
        second_threshold_eval = 0.2,
        capacity_factor_train = 1.25,
        capacity_factor_eval = 2.,
        loss_coef = 1e-2,
        router_z_loss_coef = 1e-3,
        experts = None
    ):
        super().__init__()
        assert len(num_experts) == 2, 'only 2 levels of heirarchy for experts allowed for now'

        num_experts_outer, num_experts_inner = num_experts
        self.num_experts_outer = num_experts_outer
        self.num_experts_inner = num_experts_inner

        gating_kwargs = dict(
            second_policy_train = second_policy_train,
            second_policy_eval = second_policy_eval,
            second_threshold_train = second_threshold_train,
            second_threshold_eval = second_threshold_eval,
            capacity_factor_train = capacity_factor_train,
            capacity_factor_eval = capacity_factor_eval
        )

        self.gate_outer = Top2Gating(dim, num_gates = num_experts_outer, **gating_kwargs)
        self.gate_inner = Top2Gating(dim, num_gates = num_experts_inner, outer_expert_dims = (num_experts_outer,), **gating_kwargs)

        num_experts_outer, num_experts_inner = num_experts
        self.experts = nn.ModuleList([Experts(dim, num_experts = num_experts_inner, hidden_mult = expert_hidden_mult, dropout = expert_dropout) for _ in range(num_experts_outer)])

        self.loss_coef = loss_coef
        self.router_z_loss_coef = router_z_loss_coef

    def forward(self, inputs, **kwargs):
        dispatch_tensor_outer, combine_tensor_outer, loss_outer, router_z_loss_outer = self.gate_outer(inputs)
        expert_inputs_outer = einsum('b n d, b n e c -> e b c d', inputs, dispatch_tensor_outer)

        # we construct an "importance" Tensor for the inputs to the second-level
        # gating.  The importance of an input is 1.0 if it represents the
        # first-choice expert-group and 0.5 if it represents the second-choice expert
        # group.  This is used by the second-level gating.

        importance = reduce(combine_tensor_outer, 'b n e c -> e b c', 'sum')
        importance = 0.5 * ((importance > 0.5).float() + (importance > 0.).float())

        dispatch_tensor_inner, combine_tensor_inner, loss_inner, router_z_loss_inner = self.gate_inner(expert_inputs_outer, importance = importance)
        expert_inputs = einsum('e b n d, e b n f c -> e f b c d', expert_inputs_outer, dispatch_tensor_inner)

        # Now feed the expert inputs through the experts.

        expert_inputs, ps = pack([expert_inputs], 'o i * d')

        expert_outputs = []

        for inputs, hierarchy_experts in zip(expert_inputs, self.experts):
            expert_outputs.append(hierarchy_experts(inputs))

        expert_outputs = torch.stack(expert_outputs)
        expert_outputs, = unpack(expert_outputs, ps, 'o i * d')

        # NOW COMBINE EXPERT OUTPUTS (reversing everything we have done)
        # expert_output has shape [y0, x1, h, d, n]

        expert_outputs_outer = einsum('e f b c d, e b n f c -> e b n d', expert_outputs, combine_tensor_inner)
        output = einsum('e b c d, b n e c -> b n d', expert_outputs_outer, combine_tensor_outer)

        return output, (loss_outer + loss_inner) * self.loss_coef, (router_z_loss_outer + router_z_loss_inner) * self.router_z_loss_coef
