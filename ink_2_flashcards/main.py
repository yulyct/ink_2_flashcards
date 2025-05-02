<<<<<<< HEAD
=======

from agents.agents import FlashcardBuilder


config_file = "config_list.json"
flashcard_builder = FlashcardBuilder(config_file)
file_path = "./data/sample_note.pdf" 
try : 
    response= flashcard_builder.process_file(file_path)
    print("response:", response, flush= True)
except Exception as e:
    print("Error:", e, flush= True)
>>>>>>> a35761d (Temp commit)
