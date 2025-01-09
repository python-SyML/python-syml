from transformers import pipeline

from .utils import get_device


class Linguist:
    def __init__(
        self,
    ):
        self.device = get_device()

    def setup_true_label_model(self, model="Qwen/Qwen2.5-0.5B-Instruct"):
        task = "text-generation"
        self.qa_model = pipeline(task=task, model=model, device=self.device)

    def true_label_correction(self, list_of_labels, field=None, max_new_tokens=50):
        input = f"Is the word {list_of_labels} correctly spelled? Answer ONLY with 'yes' OR 'no'."
        return self.qa_model(input, max_new_tokens=max_new_tokens)
