from test.utils import TestEndpointExecutor

URL_ENDPOINT = "classification/v1"
client = TestEndpointExecutor(URL_ENDPOINT)


# User input
def test_text_invalid_input_empty():
    message = ""
    client.do_post_endpoint(body={"text": message})(400)


def text_text_invalid_input_only_control_chars():
    message = "\t\n\r\r\r\r"
    client.do_post_endpoint(body={"text": message})(400)


def text_text_invalid_input_only_spaces():
    message = "     "
    client.do_post_endpoint(body={"text": message})(400)


def test_text_invalid_to_long():
    message = """
    Certainly! Here's a short text about life:

    Life, with its myriad twists and turns, is a journey we all embark upon from the moment of our birth. It's a tapestry woven with moments of joy and sorrow, triumphs and setbacks, love and loss. Each day presents us with opportunities to learn, grow, and evolve as individuals.

    At its core, life is about connection. It's about the bonds we form with family, friends, and even strangers we meet along the way. These connections shape our experiences, influencing the paths we choose to take and the person we ultimately become.

    Yet, life is also unpredictable. Despite our best-laid plans, we encounter obstacles that challenge us in unexpected ways. It's during these moments of adversity that our resilience is tested, and we discover the depths of our inner strength.

    But amidst the chaos and uncertainty, there is beauty to be found. In the laughter of loved ones, the warmth of a hug, or the simple pleasure of watching a sunrise, we find moments of pure, unadulterated joy. It's these moments that remind us of the preciousness of life and the importance of cherishing every fleeting second.

    Ultimately, life is what we make of it. It's about embracing each experience, whether good or bad, and finding meaning in the journey. It's about living authentically, pursuing our passions, and leaving a positive impact on the world around us.

    In the end, life is a gift—a precious gift that should be treasured, savored, and lived to the fullest.
    """
    client.do_post_endpoint(body={"text": message})(400)


# English Tests
def test_text_class_ok_default():
    message = "I am so happy today"
    client.do_post_endpoint(body={"text": message})(
        200, text_class="ok", intensity="low", language="English"
    )


def test_text_class_hate_speech_default():
    message = "I hate Gay people"
    client.do_post_endpoint(body={"text": message})(
        200,
        text_class="hate_speech",
        intensity="strong",
        language="English",
    )


def test_text_class_spam_default():
    message = "Limited time offer! Get 50% off on all our products. Shop now!"
    client.do_post_endpoint(body={"text": message})(
        200,
        text_class="spam",
        intensity="moderate",
        language="English",
    )


def test_text_class_spam_2_default():
    message = "Congratulations! You've been selected for a free trip to Paris. Click to claim."
    client.do_post_endpoint(body={"text": message})(
        200,
        text_class="spam",
        intensity="moderate",
        language="English",
    )


def test_text_class_spam_3_default():
    message = "Important message! Your Amazon account has been compromised. Click to secure it."
    client.do_post_endpoint(body={"text": message})(
        200,
        text_class="spam",
        intensity="strong",
        language="English",
    )


def test_text_class_sexual_violence():
    message = "I wanna rape you"
    client.do_post_endpoint(body={"text": message})(
        200,
        text_class="sexual_harassment",
        intensity="strong",
        language="English",
    )


# Germany test
def test_text_class_hate_speech_de():
    message = "Alle Moslime stinken"
    client.do_post_endpoint(body={"text": message})(
        200,
        text_class="hate_speech",
        intensity="strong",
        language="German",
    )


def test_text_class_sexual_violence_de():
    message = "Ich will dich ficken du schlampe"
    client.do_post_endpoint(body={"text": message})(
        200,
        text_class="sexual_harassment",
        intensity="strong",
        language="German",
    )
