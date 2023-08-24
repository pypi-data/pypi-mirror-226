from typing import Tuple

import torch
from torch import Tensor
from torch.testing import assert_close


def assert_grad_close(actual: Tensor, expected: Tensor, inputs, **kwargs) -> None:
    grad = torch.randn_like(actual)

    actual_grads = torch.autograd.grad(actual, inputs, grad, retain_graph=True, allow_unused=False)
    expected_grads = torch.autograd.grad(expected, inputs, grad, retain_graph=True, allow_unused=False)

    for actual_grad, expected_grad in zip(actual_grads, expected_grads):
        assert_close(actual=actual_grad, expected=expected_grad, **kwargs)


def assert_sequence_close(actual: Tuple[Tensor, ...], expected: Tuple[Tensor, ...], **kwargs) -> None:
    assert type(actual) == type(expected), f'{type(actual)} != {type(expected)}'
    assert len(actual) == len(expected), f'{len(actual)} == {len(expected)}'

    for index, (actual, expected) in enumerate(zip(actual, expected)):
        if actual is None:
            assert expected is None
        else:
            assert_close(actual=actual, expected=expected, **kwargs)
