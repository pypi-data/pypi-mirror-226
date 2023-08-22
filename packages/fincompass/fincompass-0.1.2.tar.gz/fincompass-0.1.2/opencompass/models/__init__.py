from .base import BaseModel, LMTemplateParser  # noqa
from .base_api import APITemplateParser, BaseAPIModel  # noqa
from .glm import GLM130B  # noqa: F401, F403
from .huggingface import HuggingFace  # noqa: F401, F403
from .huggingface import HuggingFaceCausalLM  # noqa: F401, F403
from .openai_api import OpenAI  # noqa: F401
from .cpmbee_api import CPMBEE10B  # noqa: F401
from .cpmbee_api_v2 import CPMBEE10B_V2  # noqa: F401
from .azure_api import Azure  # noqa: F401
from .eb_instant_api import EBInstant  # noqa: F401
from .eb_turbo_api import EBTurbo  # noqa: F401
from .cpmbee_ori_api import CPMBEEOri # noqa: F401
from .minimax_api import MiniMax # noqa: F401
from .qwen_api import Qwen # noqa: F401
from .model_base import ModelBaseAPI # noqa: F401
