import re
from enum import Enum

from app.llm.llm_adapter import LLMAdapter
from app.utils.error import BusinessException

# Max length of user message string
USER_MESSAGE_MAX_LENGTH = 1000

# client adapter
CLIENT = LLMAdapter()

PROMPT_TEMPLATE = """
Classify the text given by the user and decide on an appropriate intensity category and suggested action:

Instructions:
1. Detect the language of the text. Focus on English, German, French, Spanish, and Italian. Reject texts not in these languages.
2. Classify the content into one of the categories: 'sexual harassment', 'hate speech', 'spam', 'ok'.h
3. Assign an intensity level ('strong', 'moderate', 'low') based on nuances in the text:
   - Categorize as 'strong' if the text offers sex services, weapons, drugs or can be identified as scam or fraud.
   - Consider the influence of specified user setting Strictness for the level of intensity.
4. For the category 'spam' assign the intensity level:
    - 'strong' if message is attempted fraud or scam 
    - 'moderate' for every other not as strong classified spam
    - 'low' there is no low intensity level for spam
5. Based on the Strictness setting:
    - High Strictness
        - if intensity level is between 'strong' and 'moderate' use 'strong'
        - if intensity level is between 'moderate' and 'low' use 'moderate'
    - Low Strictness
        - if intensity level is between 'strong' and 'moderate' use 'moderate'
        - if intensity level is between 'moderate' and 'low' use 'low'
6. Suggested action should be included ('report', 'notify', 'none') based on the intensity level.
    - Consider the influence of specified user setting Precision for the suggested action.
7. Based on the Precision setting:
   - High Precision: 
       - 'strong' and 'moderate' lead to action 'report'
       - 'low' leads to action 'notify'
       - category 'ok' leads to action none 'none'
   - Medium Precision:
       - 'strong' leads to action 'report'
       - 'moderate' leads to action 'notify'
       - 'low' leads to action 'none'
       - category 'ok' always leads to action 'none'
   - Low Precision:
       - 'strong' leads to 'notify'
       - ambiguous'moderate' and 'low' lead to 'none'
       - category 'ok' leads to 'none'
8. Provide a brief explanation for the classification decision in the same language as the user text.
9. Include the detected language in the response.

User configurations:
- Precision: {precision_level}
- Strictness: {strictness_level}

Return the category, intensity, detected_language, suggested_action, and brief_explanation of the classification in your response as json.
"""


#
class LLMResultKeyEnum(Enum):
    CATEGORY = "category"
    INTENSITY = "intensity"
    LANGUAGE = "detected_language"
    ACTION = "suggested_action"
    EXPLANATION = "brief_explanation"

    @classmethod
    def from_value(cls, value: str):
        return cls(value)

    @classmethod
    def all_values(cls) -> list:
        return [cls.CATEGORY, cls.INTENSITY, cls.LANGUAGE, cls.ACTION, cls.EXPLANATION]


class StrictnessEnum(Enum):
    HIGH = "High"
    LOW = "Low"


class PrecisionEnum(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class TextClassEnum(Enum):
    SEXUAL_HARASSMENT = "sexual_harassment"
    HATE_SPEECH = "hate_speech"
    SPAM = "spam"
    OK = "ok"


class IntensityEnum(Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    LOW = "low"


class ActionEnum(Enum):
    REPORT = "report"
    NOTIFY = "notify"
    NONE = "none"


class TextClassificationResult:
    def __init__(
        self,
        language: str,
        text_class: TextClassEnum,
        intensity: IntensityEnum,
        # action: ActionEnum,
        explanation: str,
    ):
        self.language = language
        self.text_class = text_class
        self.intensity = intensity
        # self.action = action
        self.explanation = explanation


# Remove control chars
def replace_control_char(message: str | None) -> str | None:
    if message == None:
        return message
    """
    Because of security remove all control character  
    """
    return re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F\t\n\r]", " ", message)


def has_alphanumeric(text):
    return any(char.isalnum() for char in text)


def verify_message(message: str | None) -> None:
    """
    Validate user message to avoid unnecessary LLM calls.
    """
    if message == None or len(message) == 0 or len(message.replace(" ", "")) == 0:
        raise BusinessException(
            400, "Message is empty msg: '{message}'".format(message=message), None
        )

    if not has_alphanumeric(message):
        raise BusinessException(
            400, "Nothing to check: '{message}'".format(message=message), None
        )

    if len(message) > USER_MESSAGE_MAX_LENGTH:
        raise BusinessException(
            400,
            "Message length {msgLen} > {maxLen}".format(
                msgLen=len(message), maxLen=USER_MESSAGE_MAX_LENGTH
            ),
            None,
        )


def normalizeValue(value) -> str:
    """
    Normalize value to Enum value.
    """
    if value is None:
        return ""
    return str(value).replace(" ", "_").upper()


def check_and_convert(content: dict) -> TextClassificationResult:
    """
    Check and convert LLM result
    """
    for item in LLMResultKeyEnum.all_values():
        if item.value not in content:
            raise BusinessException(
                500,
                "Invalid response from LLMProvider: {content}".format(content),
                None,
            )
    try:
        return TextClassificationResult(
            content[LLMResultKeyEnum.LANGUAGE.value],
            TextClassEnum[normalizeValue(content[LLMResultKeyEnum.CATEGORY.value])],
            IntensityEnum[normalizeValue(content[LLMResultKeyEnum.INTENSITY.value])],
            # ActionEnum[normalizeValue(content[LLMResultKeyEnum.ACTION.value])],
            content[LLMResultKeyEnum.EXPLANATION.value],
        )
    except Exception as err:
        raise BusinessException(
            500, "Building text classification response failed", err
        )


async def classify(
    user_message: str, precision="medium", strictness="high"
) -> TextClassificationResult:
    """
    Classify text
    user_message: the text that has to be classified
    precision: "high" | "medium" | "low"
    strictness: "high" | "low"
    """

    clean_user_message = replace_control_char(user_message)
    verify_message(clean_user_message)

    system_prompt = ""
    try:
        precision_level = PrecisionEnum[normalizeValue(precision)]
        strictness_level = StrictnessEnum[normalizeValue(strictness)]

        system_prompt = PROMPT_TEMPLATE.format(
            precision_level=precision_level.value,
            strictness_level=strictness_level.value,
        )
    except Exception as err:
        raise BusinessException(
            400,
            """ Wrong value for: precision_level={precision_level} []
                                or strictness_level={strictness_level}""",
            err,
        )

    content = await CLIENT.do_text_classification(
        system_prompt, str(clean_user_message)
    )

    return check_and_convert(dict(content))
