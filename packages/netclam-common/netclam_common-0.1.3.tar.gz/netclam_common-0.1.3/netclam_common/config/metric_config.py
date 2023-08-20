from dataclasses import dataclass

@dataclass
class metric_config:

    namespace: str
    subsystem: str
    enabled: bool