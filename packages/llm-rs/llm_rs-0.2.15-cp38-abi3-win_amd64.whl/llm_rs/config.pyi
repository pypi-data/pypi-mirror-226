from typing import Optional,List
from enum import Enum, auto

class ContainerType(Enum):
    GGML=auto(),
    GGJT=auto(),

class QuantizationType(Enum):
    Q4_0=auto(),
    Q4_1=auto(),
    Q5_0=auto(),
    Q5_1=auto(),
    Q8_0=auto(),
    F16=auto(),

class Precision(Enum):
    FP32=auto(),
    FP16=auto(),
    
class GenerationConfig():
    """
    Configuration parameters for the generation process.
    """
    top_k:int
    top_p:float
    temperature:float
    repetition_penalty:float
    repetition_penalty_last_n:int
    seed:int
    max_new_tokens:Optional[int]
    stop_words:Optional[List[str]]
    
    def  __init__(self,top_k:int=40,top_p:float=0.95,temperature:float=0.8,repetition_penalty:float=1.3,repetition_penalty_last_n:int=512,seed:int=42,max_new_tokens:Optional[int]=None,stop_words:Optional[List[str]]=None) -> None: ...
    
class SessionConfig():
    """
    Configure the generation session that will be used for all generations.
    """
    threads:int
    batch_size:int
    keys_memory_type:Precision
    values_memory_type:Precision
    rope_frequency_scale:Optional[float]
    rope_frequency_base:Optional[int]
    
    
    @property
    def context_length(self)->int: ...
    
    @property
    def prefer_mmap(self)->bool:...

    @property
    def use_gpu(self)->bool:...

    @property
    def gpu_layers(self)->Optional[int]:...
    
    def  __init__(self,
                  threads:int=8,
                  batch_size:int=8,
                  context_length:int=2048,
                  keys_memory_type:Precision=Precision.FP16,
                  values_memory_type:Precision=values_memory_type.FP16,
                  prefer_mmap:bool=True,
                  use_gpu:bool=False,
                  gpu_layers:Optional[int]=None,
                  rope_frequency_scale:Optional[float]=None,
                  rope_frequency_base:Optional[int]=None
                  ) -> None: ...