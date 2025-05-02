
# 📝 ink_2_flashcards

**ink_2_flashcards** is a minimal multi-agent AI system that extracts handwritten notes from images or PDFs and generates study flashcards using `ollama-ocr` and `AutoGen`.

---

## 🚀 Features

- OCR text extraction using vision models via `ollama-ocr`
- Flashcard generation in Q&A format
- Runs locally with open-source models

---

## 📁 Project Structure

```plaintext
ink_2_flashcards/
├── agents/
│   ├── __init__.py
│   └── agents.py
├── data/
│   └── sample_note.pdf
├── config_list.json
├── main.py
├── README.md
└── requirements.txt
