import torch

from cca_zoo.linear._gradient._base import BaseLoop
from cca_zoo.linear._gradient._ey import PLSEY
from cca_zoo.linear._pls import PLSMixin


class PLSStochasticPower(PLSEY, PLSMixin):
    def _get_pl_module(self, weights=None, k=None):
        return StochasticPowerLoop(
            weights=weights,
            k=k,
            learning_rate=self.learning_rate,
            optimizer_kwargs=self.optimizer_kwargs,
        )

    def _more_tags(self):
        return {"multiview": True, "stochastic": True}


class StochasticPowerLoop(BaseLoop):
    def __init__(
        self,
        weights=None,
        k=None,
        learning_rate=1e-3,
        optimizer_kwargs=None,
        tracking=False,
        convergence_checking=False,
    ):
        super().__init__(
            weights=weights,
            k=k,
            learning_rate=learning_rate,
            optimizer_kwargs=optimizer_kwargs,
            tracking=tracking,
            convergence_checking=convergence_checking,
        )

    def training_step(self, batch, batch_idx):
        for weight in self.weights:
            weight.data = self._orth(weight)
        scores = self(batch["views"])
        # find the pairwise covariance between the scores
        cov = torch.cov(torch.hstack(scores).T)
        loss = torch.trace(cov[: scores[0].shape[1], scores[0].shape[1] :])
        self.log("train_loss", loss)
        return loss

    def on_train_end(self) -> None:
        for weight in self.weights:
            weight.data = self._orth(weight)

    @staticmethod
    def _orth(U):
        Qu, Ru = torch.linalg.qr(U)
        Su = torch.sign(torch.sign(torch.diag(Ru)) + 0.5)
        return Qu @ torch.diag(Su)
