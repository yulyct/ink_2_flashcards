

from autogen import AssistantAgent, UserProxyAgent, GroupChatManager, GroupChat
from autogen import register_function
from ollama_ocr import OCRProcessor
import autogen
import json


class FlashcardBuilder:
    def __init__(self, config_file):
        config_file =  config_file 
        config_list = autogen.config_list_from_json(
            config_file,
            filter_dict={"model": ["llama3.2:3b"]},
        )

        self.llm_config = {
            "config_list": config_list,
            "cache_seed": None,
            "temperature": 0.5,
        }

        self.user_proxy = UserProxyAgent(
            name="UserProxyAgent",
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            human_input_mode="NEVER",
            max_consecutive_auto_reply=2,
            code_execution_config=False,
        )

        self.ocr_agent = AssistantAgent(
            name="OCR_agent",
            llm_config=self.llm_config,
            system_message="""You are an OCR assistant. 
                Your main responsibility is to extract text from documents by invoking the 'run_ocr' tool. 
                Make sure to call it with the provided file path."""
        )

        self.flashcard_agent = AssistantAgent(
            name="FlashcardAgent",
            llm_config=self.llm_config,
            system_message=(
                """You are an expert study assistant. Your task is to generate flashcards from course notes.
                   You must follow the formatting and content instructions provided.
                   Instructions:
                - Read the provided text carefully.
                - Identify important concepts, definitions, or facts.
                - For each key point, create a flashcard in the format:
                Q: [Question]
                A: [Answer]
                Requirements:
                - Keep questions clear and concise.
                - Limit answers to 1 or 2 sentences.
                - Do not include questions that are too vague or overly broad.
                - Focus only on relevant and factual content from the notes."""
            )
        )

        register_function(
            run_ocr,
            caller=self.ocr_agent,
            executor=self.user_proxy,
            name="run_ocr",
            description="Extract text from image or pdf using ollama-ocr."
        )

        self.manager = GroupChatManager(
            groupchat=GroupChat(
                agents=[self.user_proxy, self.ocr_agent, self.flashcard_agent],
                messages=[],
                max_round=4,
                speaker_selection_method="round_robin",
            ),
            llm_config=self.llm_config,
            system_message=(
                """You are the group manager responsible for coordinating a two-step process to convert handwritten notes into study flashcards.
                Step 1: Ask the OCR_Agent to extract the text from the handwritten image or PDF file.
                Step 2: Once the OCR_Agent provides the extracted text, send that content to the FlashcardAgent to generate flashcards in Q&A format.
                Make sure the process follows this order strictly:
                1. OCR_Agent → extract raw text.
                2. FlashcardAgent → create flashcards from the extracted text.
               """
            )
        )


    def process_file(self, file_path: str):
        message = f"extracts notes from file '{file_path}', and provide flashcards in Q&A format."
        response = self.user_proxy.initiate_chat(self.manager, message=message)
        return response.chat_history[-1]['content']


def run_ocr(file_path: str) -> str:
        ocr = OCRProcessor(model_name='granite3.2-vision')
        result = ocr.process_image(
            image_path=file_path,
            format_type="text",
            language="eng"
        )
        return result

