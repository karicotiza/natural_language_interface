import requests


class NeuralAPI:
    __url = "https://api-inference.huggingface.co/models/csebuetnlp/mT5_multilingual_XLSum"
    __token = {
        "Authorization": "Bearer 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",
    }

    @staticmethod
    def summarize(text: str) -> str:
        try:
            return requests.post(
                url=NeuralAPI.__url,
                headers=NeuralAPI.__token,
                json={
                    "inputs": text,
                },
            ).json()[0].get("summary_text")

        except KeyError:
            return "Model is loading"
