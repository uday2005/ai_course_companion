# 🤖 AI Course Companion

A comprehensive AI-powered learning assistant that provides intelligent Q&A capabilities for course materials. This project combines textbook content, lecture transcripts, and Jupyter notebooks[right now not using it as i am unable to find a good reader for it.] to create an interactive learning experience powered by RAG (Retrieval-Augmented Generation) technology.

## ✨ Features

- **Multi-Source Knowledge Base**: Integrates textbooks (PDFs), lecture transcripts, and Jupyter notebooks
- **Intelligent Query Engine**: Uses LlamaIndex with specialized tools for different content types
- **Web Interface**: Clean Gradio-based UI for easy interaction
- **Local AI Support**: Powered by Ollama for privacy-focused, offline AI capabilities
- **Vector Storage**: Persistent ChromaDB storage for efficient retrieval
- **Automated Content Processing**: Tools for extracting and processing course materials

## 🏗️ Architecture

The system uses a multi-agent architecture with specialized tools:

- **📚 Textbook Tool**: Answers theoretical questions and concept definitions from the fast.ai textbook
- **🎥 Transcript Tool**: Provides practical advice and examples from Jeremy Howard's video lectures
- **🔍 RAG Pipeline**: Combines retrieval and generation for contextually relevant answers

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running locally
- Course materials (PDFs, transcripts, notebooks) in the `data/` directory

### Installation
All these only if you are putting other courses ,for fast ai course we already have indices so you don't need to build again the indices , if you want you can.
1. **Clone the repository**:
   ```bash
   git clone https://github.com/uday2005/ai_course_companion.git
   cd ai_course_companion
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Ollama models**:
   ```bash
   ollama pull llama3
   ollama pull mistral
   ```

4. **Prepare your course materials**:
   - Place PDF files in `data/book/`
   - Place transcript files in `data/transcripts/`
   - Place Jupyter notebooks in `data/notebooks/`

### Usage

1. **Build the knowledge indices** (first time setup):
   ```bash
   python build_indices.py
   ```

2. **Launch the web interface**:
   ```bash
   python ui.py
   ```

3. **Or use the CLI interface**:
   ```bash
   python app.py
   ```

## 📁 Project Structure

```
ai_course_companion/
├── app.py                      # Main application with agent workflow
├── ui.py                       # Gradio web interface
├── build_indices.py            # Script to build vector indices
├── transcript_extractor.py     # YouTube transcript extraction utility
├── pdf_extractor_to_small.py   # PDF chapter splitting utility
├── requirements.txt            # Python dependencies
├── data/                       # Course materials
│   ├── book/                   # PDF textbook chapters
│   ├── notebooks/              # Jupyter notebooks
│   └── transcripts/            # Lecture transcripts
├── storage_book/               # ChromaDB storage for textbook
├── storage_notebooks/          # ChromaDB storage for notebooks
└── storage_transcripts/        # ChromaDB storage for transcripts
```

## 🛠️ Utilities

### PDF Chapter Extractor
Use `pdf_extractor_to_small.py` to split a large textbook PDF into individual chapters:

```python
# Configure the CHAPTERS list with your book's structure
CHAPTERS = [
    ("01_Introduction", 27, 80),
    ("02_From_Model_to_Production", 81, 116),
    # ... add more chapters
]
```

### YouTube Transcript Extractor
Extract transcripts from YouTube videos using `transcript_extractor.py`:

```python
video_id = "your_video_id_here"
# Script will save transcript to data/transcripts/
```

## 🔧 Configuration

### Using Different LLM Providers

The system supports both Ollama (default) and Google Gemini:

**Ollama (Local, Privacy-focused)**:
```python
Settings.embed_model = OllamaEmbedding(model_name="llama3")
Settings.llm = Ollama(model="mistral")
```

**Google Gemini** (requires API key):
```python
Settings.embed_model = GeminiEmbedding(api_key=GOOGLE_API_KEY)
Settings.llm = Gemini(api_key=GOOGLE_API_KEY, model="gemini-2.5-pro")
```

## 💡 Example Queries

- **Theoretical Questions**: "What is a loss function according to the textbook?"
- **Practical Advice**: "What does Jeremy Howard say about transfer learning in the lectures?"
- **Multi-source**: "Define neural networks using the textbook, then find examples from the transcripts"

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built using [LlamaIndex](https://www.llamaindex.ai/) for RAG capabilities
- Powered by [Ollama](https://ollama.ai/) for local AI inference
- UI created with [Gradio](https://gradio.app/)
- Vector storage with [ChromaDB](https://www.trychroma.com/)

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub or contact [24b2729@iitb.ac.in].

---

**Note**: This project is designed specifically for the fast.ai course materials, but can be adapted for other educational content by modifying the data processing scripts and tool descriptions.


## ⚠️ Important Notes

### Model Recommendations
1. **Rate Limits**: Currently using Ollama (local models) instead of Gemini due to API rate limit issues. Local models have no rate limits and ensure privacy.

2. **LLM Selection**: 
   - ✅ **Recommended**: Use `mistral` as the main LLM (supports tool calling)
   - ❌ **Avoid**: `llama3` as LLM doesn't support tool calling properly
   - 💡 **Tip**: You can use lightweight models for embeddings to reduce processing time

### Current Limitations
- **Jupyter Notebooks**: Currently limited support due to lack of a robust reader in LlamaIndex
- **Web Deployment**: No public web app available due to rate limit considerations with cloud APIs

## 🚀 Future Roadmap

### Planned Improvements
1. **Enhanced Jupyter Support**: Develop or integrate a better Jupyter notebook reader
2. **Public Web Interface**: Deploy a public web application when rate limiting issues are resolved
3. **Automated Setup**: Create a fully automated system where users only need to provide:
   - PDF files
   - YouTube video links
   - Other source materials
   
   The system will handle all processing automatically without code modifications.
