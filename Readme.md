# Language Detection and Text Classification Endpoint

## About
This API offers language detection, content classification, intensity level assessment, and suggested action generation for text inputs. It is designed to analyze text content and provide insights into its nature, ranging from benign to potentially harmful categories.

## Language Detection
Automatically detects the language of the input text. Focus is primarily on English, German, French, Spanish, and Italian. Texts not in these languages are rejected.

## Content Classification
Classifies the text into one of the following categories: 'sexual harassment', 'hate speech', 'spam', or 'ok'.

## Intensity Level Assessment
Evaluates the intensity level of the text based on nuances and context. Intensity levels are categorized as 'strong', 'moderate', or 'low'.

**Input a text for analysis:** Receive detailed insights including language detection, content classification, intensity level assessment, and suggested action.
Customize user settings for strictness and precision to tailor the suggested action according to preferences.
Implement the suggested action programmatically based on the API response.

## Example Request
`POST {baseUrl}/classification/v1`

**Request Body:**

```
{
    "text": "I am a good person. and I love the world"
}
```

**Response Body:**

```
{
    "language": "English",
    "text_class": "ok",
    "intensity": "low",
    "explanation": "The text was classified as 'ok' with a low intensity level.  No action is suggested as the content does not contain any concerning elements."
}
```

## Use Cases
Social media platforms can use this API to automatically identify and take action on harmful content, such as hate speech or sexual harassment.
E-commerce platforms can utilize this API to filter out spam messages and fraudulent activities, protecting users from scams and phishing attempts.
Online forums and communities can implement this API to maintain a safe and respectful environment by monitoring and addressing inappropriate content.
**Integration:** Available as a RESTful API for seamless integration into existing systems and applications. Supports JSON format for easy data exchange.

**Scalability:** workload/text is limited to 2000 character.

## Get Started
You can try this API on [rapidapi.com](https://rapidapi.com/agilebyte-agilebyte-default/api/text-classifier1/details)
Choose a plan to get access and start analyzing text content to enhance safety and moderation in digital platforms.

## Application can be deployed as docker image on AWS Lambda.

### Precondctions

- You have an [OpenAI](https://platform.openai.com/docs/introduction) account.
- You have credits on your account [OpenAI](https://platform.openai.com/settings/organization/billing/overview)
- Precondiction you have a [OpenAI Api Key](https://platform.openai.com/api-keys)
- You have an [AWS Account](https://aws.amazon.com/).
- Docker command is configured on your maschine

**Build Docker**
Set your OpenAI API-KEY as environment variable and build docker

```
export OPENAI_API_KEY=<you key here>

docker build -t txt_classify_api --build-arg OPENAI_API_KEY .
```

**Build lambda from container image**
Build Lambda on [AWS](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)
