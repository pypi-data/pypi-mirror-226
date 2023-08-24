import torch
from .encryptedtensor import EncryptedTensor


class EncryptedSigmoid(torch.nn.Sigmoid):
    def __init__(self, poly_approx_degree=1):
        super().__init__()
        self.poly_approx_degree = poly_approx_degree
        if poly_approx_degree < 1 or poly_approx_degree > 3:
            raise Exception("Polynomial Approximation degree only supports 1, 2, 3")

    def forward(self, input):
        if isinstance(input, EncryptedTensor):
            # We use the polynomial approximation of degree 3
            # sigmoid(x) = 0.5 + 0.197 * x - 0.004 * x^3
            # from https://eprint.iacr.org/2018/462.pdf
            # which fits the function pretty well in the range [-5,5]
            data = EncryptedTensor.__parse_data__(input)
            if self.poly_approx_degree == 1 or self.poly_approx_degree == 2:
                return EncryptedTensor(0.5 + 0.197 * data)
            else:
                return EncryptedTensor(0.5 + (0.197 - ((0.004 * data) * data)) * data)

        return super().forward(input)
