from dataclasses import dataclass


@dataclass
class ImageAnalysis:
    description: str
    objects: list[str]
    insights: list[str]
    recommendations: list[str]