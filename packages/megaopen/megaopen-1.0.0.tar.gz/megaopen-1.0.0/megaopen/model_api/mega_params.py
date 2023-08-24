from dataclasses import dataclass

from megaopen.model_api.params import ModelParams


@dataclass
class LegalAidParams(ModelParams):
    model: str = "legalaid"

