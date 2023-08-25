from number_transcription.enums import ScaleTypeEnum
from .enums import EnglishUnit


def number_to_words(number: int, unit: EnglishUnit | None,
                    scale_type: ScaleTypeEnum = ScaleTypeEnum.LONG) -> str:
    return ""


def words_to_number(text: str, scale_type: ScaleTypeEnum = ScaleTypeEnum.LONG) -> int:
    return 0
