from dataclasses import dataclass

from megatechai.model_api.params import ModelParams


@dataclass
class LegalAidParams(ModelParams):
    model: str = "legalaid"

