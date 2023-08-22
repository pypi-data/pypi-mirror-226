# Copyright (c) 2023 promptulate
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright Owner: Zeeland
# GitHub Link: https://github.com/Undertone0809/
# Project Link: https://github.com/Undertone0809/promptulate
# Contact Email: zeeland@foxmail.com

from typing import Optional, Union

from pydantic import Field

from promptulate import utils
from promptulate.config import Config
from promptulate.llms.base import BaseLLM
from promptulate.memory import BufferChatMemory
from promptulate.llms import OpenAI, ChatOpenAI
from promptulate.memory.base import BaseChatMemory
from promptulate.frameworks.schema import BasePromptFramework
from promptulate.preset_roles.roles import CustomPresetRole, get_preset_role_prompt
from promptulate.provider.mixins import (
    SummarizerMixin,
    TranslatorMixin,
    DeriveHistoryMessageMixin,
)
from promptulate.schema import (
    AssistantMessage,
    init_chat_message_history,
)
from promptulate.tips import EmptyMessageSetError
from promptulate.utils.core_utils import record_time

CFG = Config()
logger = utils.get_logger()


# todo finish here
# todo 完成agent
class Chain(BasePromptFramework):
    conversation_id: Optional[str] = None
    llm: BaseLLM = Field(default_factory=ChatOpenAI)
    enable_stream: bool = False  # streaming transmission
    role: Union[str, CustomPresetRole] = "default-role"
    memory: BaseChatMemory = Field(default_factory=BufferChatMemory)
