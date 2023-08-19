from typing import List, Union
from llama import LLMEngine
import jsonlines
import pandas as pd

from llama.prompts.llama_v2_prompt import LlamaV2Prompt, LlamaV2Input, LlamaV2Output

DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""


class LlamaV2Runner:
    """A class for running and training a Llama V2 model, using system and user prompts"""

    def __init__(
        self,
        model_name: str = "meta-llama/Llama-2-7b-chat-hf",
        system_prompt: str = None,
        enable_peft: bool = False,
        config: dict = {},
    ):
        self.model_name = model_name
        self.prompt = LlamaV2Prompt()
        self.llm = LLMEngine(
            "llama_v2_runner_data",
            model_name=model_name,
            config=config,
            prompt=self.prompt,
        )
        self.job_id = None
        self.data = []
        self.evaluation = None
        self.enable_peft = enable_peft
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT

    def __call__(self, inputs: Union[str, List[str]], system_prompt: str = None) -> str:
        """Call the model runner on prompt"""
        system_prompt = system_prompt or self.system_prompt
        if isinstance(inputs, list):
            print("Running batch job on %d number of inputs" % len(inputs))
            input_objects = [LlamaV2Input(user=i, system=system_prompt) for i in inputs]
        else:
            # Singleton
            input_objects = LlamaV2Input(user=inputs, system=system_prompt)
        output_objects = self.llm(
            input=input_objects,
            output_type=LlamaV2Output,
            model_name=self.model_name,
            enable_peft=self.enable_peft,
        )
        if isinstance(output_objects, list):
            outputs = [o.output for o in output_objects]
            return [{"input": i, "output": o} for i, o in zip(inputs, outputs)]
        else:
            return output_objects.output

    def get_keys(self, data_keys):
        if "question" in data_keys and "answer" in data_keys:
            keys = ["question", "answer"]
        elif "instruction" in data_keys and "response" in data_keys:
            keys = ["instruction", "response"]
        elif "input" in data_keys and "output" in data_keys:
            keys = ["input", "output"]
        else:
            keys = ["text", None]
        return keys

    def load_data(self, data, verbose: bool = False):
        """
        Load a list of dictionary objects with input-output keys into the LLM
        Each object must have 'user' and 'output' as keys.
        """
        # Get keys
        if not isinstance(data, list) and not isinstance(data[0], dict):
            raise ValueError(
                "Data must be a list of dicts with keys 'user' and 'output'"
            )
        try:
            input_output_objects = [
                [
                    LlamaV2Input(
                        user=d["user"],
                        system=self.system_prompt,
                    ),
                    LlamaV2Output(output=d["output"])
                    if "output" in d
                    else LlamaV2Output(output=""),
                ]
                for d in data
            ]
        except KeyError:
            raise ValueError("Each object must have 'user' and 'output' as keys")
        self.data.extend(input_output_objects)
        if verbose:
            print("Sample added data: %s" % str(input_output_objects[0]))
            print("Loaded %d data pairs" % len(input_output_objects))
            print("Total data pairs: %d" % len(self.data))

    def load_data_from_jsonlines(self, file_path: str, verbose: bool = False):
        """
        Load a jsonlines file with input output keys into the LLM.
        Each line must be a json object with 'user' and 'output' as keys.
        """
        data = []
        with open(file_path) as dataset_file:
            reader = jsonlines.Reader(dataset_file)
            data = list(reader)
        self.load_data(data, verbose=verbose)

    def load_data_from_dataframe(
        self, df: pd.DataFrame, verbose: bool = False
    ):
        """
        Load a pandas dataframe with input output keys into the LLM.
        Each row must have 'user' and 'output' as keys.
        """
        data_keys = df.columns
        keys = self.get_keys(data_keys)
        input_output_objects = []
        try:
            for _, row in df.iterrows():
                input_output_objects.append(
                    [
                        LlamaV2Input(user=row[keys[0]], system=self.system_prompt),
                        LlamaV2Output(output=row[keys[1]])
                        if keys[1]
                        else LlamaV2Output(output=""),
                    ]
                )
        except KeyError:
            raise ValueError("Each object must have 'user' and 'output' as keys")
        self.data.extend(input_output_objects)

        if verbose:
            print("Sample added data: %s" % str(input_output_objects[0]))
            print("Loaded %d data pairs" % len(input_output_objects))
            print("Total data pairs: %d" % len(self.data))

    def load_data_from_csv(self, file_path: str, verbose: bool = False):
        """
        Load a csv file with input output keys into the LLM.
        Each row must have 'user' and 'output' as keys.
        The 'system' key is optional and will default to system prompt 
        if passed during model initiation else to DEFAULT_SYSTEM_PROMPT.
        """
        df = pd.read_csv(file_path)
        self.load_data_from_dataframe(df, verbose=verbose)

    def clear_data(self):
        """Clear the data from the LLM"""
        self.data = []

    def train(
        self, verbose: bool = False, finetune_args={}, limit=500, is_public=False
    ):
        """
        Train the LLM on added data. This function blocks until training is complete.
        """
        if len(self.data) < 10:
            raise Exception("Submit at least 10 data pairs to train")
        if len(self.data) > limit:
            data = self.data[:limit]
        else:
            data = self.data

        final_status = self.llm.train(
            data, verbose=verbose, finetune_args=finetune_args, is_public=is_public
        )
        try:
            self.model_name = final_status["model_name"]
            self.job_id = final_status["job_id"]
            self.llm.clear_data()
        except KeyError:
            raise Exception("Training failed")

    def evaluate(self) -> List:
        """Get evaluation results"""
        self.evaluation = self.llm.evaluate()
        return self.evaluation

    def get_eval_results(self) -> List:
        if self.job_id is None:
            raise Exception("Must train before getting results (no job id))")
        self.evaluation = self.llm.eval(self.job_id)
        return self.evaluation
