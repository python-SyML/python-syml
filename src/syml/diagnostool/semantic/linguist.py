from transformers import pipeline

from .utils import get_device


class Linguist:
    def __init__(
        self,
    ):
        self.device = get_device()

    def setup_true_label_model(self, model="openai-community/gpt2"):
        task = "text-generation"
        self.qa_model = pipeline(task=task, model=model, device=self.device)

    def true_label_correction(self, list_of_labels, field=None, max_new_tokens=50):
        role = "system"
        content = """
        You are an expert in linguistics and word spelling. You are very cautious about typos and spelling mistakes.

        You are given lists of labels that belong to a certain field. Some labels may contain typos and spelling mistakes.
        BASED ON YOUR KNOWLEDGE, FIND IN THE LIST the labels that are correctly spelled and returns them as a list.

        The ONLY VALID RESPONSE format is :

        ['label_1', 'label_2', ..., 'label_n']

        where 'label_1', ... 'label_n' are the labels without typos that you found.

        ----------------------------------------------------------------

        Correct Example 1 :

        Input :

        Field name : 'work class'
        Labels : ['self-emp-inc', 'self-emp-not-inc', 'self-emp-noti-nc', 'self-emp-noit-inc', 'never-worked', 'nevre-worked', 'never-woorked', 'never-worked']

        Output :

        ['self-emp-inc', 'self-emp-not-inc', 'never-worked']

        Correct Example 2 :

        Field name : 'occupation'
        Labels : 'Protective-erv', 'Protective-sev', 'xProtective-serv', 'Protective-serv', 'Otehr-service', 'Other-service', 'Craf-repair', 'Craft-epair', 'Prof-specailty', 'rPof-specialty', 'Prof-specailty', 'Craft-repair', 'Adm-clerical, 'Other-zervice', 'Other-serviceg', 'Profs-specialty',   'Craft-rwpair', 'Adm-clericl']

        Output :
        ['Protective-serv', 'Other-service', 'Prof-specailty', 'Craft-repair', 'Adm-clerical']

        INCORRECT Example 1 :

        Field name : 'occupation'
        Labels : 'Protective-erv', 'Protective-sev', 'xProtective-serv', 'Otehr-service', 'Other-zervice', 'Other-serviceg', 'Profs-specialty', 'Prof-specailty', 'rPof-specialty', 'Craf-repair', 'Craft-epair', 'Craft-rwpair', 'Adm-clericl']

        Output :
        ['Protective-serv', 'Other-service', 'Prof-specailty', 'Craft-repair']

        INCORRECT Example 2 :

        Field name : 'work class'
        Labels : ['self-emp-inc', 'self-emp-not-inc', 'self-emp-noti-nc', 'self-emp-noit-inc', 'never-worked', 'nevre-worked', 'never-woorked']

        Output :

        ['self-emp-inc', 'self-emp-not-inc', 'self-emp-not-inc', 'self-emp-not-inc', 'never-worked']
        """
        init_message = {"role": role, "content": content}

        role_user = "user"
        content_user = f"""
        Input :

        Field name : {field}
        Labels : {list_of_labels}

        Output :
        """

        user_message = {"role": role_user, "content": content_user}

        message = [init_message, user_message]

        return self.qa_model(message, max_new_tokens=max_new_tokens)
