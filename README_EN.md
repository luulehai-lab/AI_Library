<!--
File: README_EN.md
Description: Introductory document, installation, and operation guide for the AI Book Library Assistant
CHANGELOG:
- 10:52:00 08/07/2026: [NEW] Initialize English README.md with detailed project background and installation guide. (Antigravity)
-->

# 📚 AI Library Assistant

🌐 *[Bản Tiếng Việt](README.md)*

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg) ![UI PyQt6](https://img.shields.io/badge/UI-PyQt6-orange.svg) ![AI Engine Gemini](https://img.shields.io/badge/AI%20Engine-Gemini%20Flash-brightgreen.svg) ![Vector DB ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-blueviolet.svg) ![Database SQLite3](https://img.shields.io/badge/Database-SQLite3-003b57.svg) ![License MIT](https://img.shields.io/badge/license-MIT-blue.svg)

A premium desktop application built with **PyQt6** and integrated with **Generative AI (Gemini Flash)** to automate the digitization, management, and semantic interaction of personal book collections.

<p align="center">
  <img src="assets/logo.png" alt="AI Library Logo" width="200"/>
</p>

---

## 📖 Background & Origin Story

The project originated from the real-world management needs of Mr. Luu, an avid reader who owns a massive physical collection of over **2,000 books**. Organizing, cataloging, and storing such a large number of physical books manually is an extremely complex and time-consuming task.

Initially, he managed the book catalog via an Excel file. However, this process required him to manually search for each book's metadata on the Internet (such as the exact book title, author, publisher, publication year, page count, genres, target age group, summaries/reviews, and prices on e-commerce platforms like Tiki) and manually type them into individual cells.

Recognizing the inefficiency of this manual process, the **AI Library Assistant** was born as a smart digitization solution: **With just a single photo of a book's cover**, the AI system automatically handles all the rest, from analysis and metadata extraction to database storage, data normalization, and RAG-powered chatbot conversations.

---

## ✨ Key Features

*   📷 **AI-Powered Cover Scanning**: Upload a book cover image, and Gemini AI will automatically analyze and extract 100% of the metadata (Title, Author, Publisher, Genre, Publication Year, Goodreads Score, Tiki Price, and summary Review).
*   🔄 **Intelligent Auto-Rotation**: AI automatically detects the orientation of the book cover and rotates the image to the correct vertical aspect ratio.
*   📊 **Interactive Dashboard**: Integrated Matplotlib graphs displaying detailed library statistics by Genre, Reading Status, Top Authors, Publication Year, and Country of Origin.
*   💬 **Semantic AI Chatbot (RAG)**: Integrated ChromaDB (Vector Database) semantic search allowing you to chat directly and ask questions about the contents/knowledge of books stored in your library.
*   📥 **Batch Import Tool**: Script to import hundreds of books simultaneously from a local folder of cover images, automating the entire pipeline.
*   📑 **Excel Reports**: Export book library data to professionally formatted Excel files with color formatting using openpyxl.

---

## 🛠️ Tech Stack

*   **GUI Framework**: PyQt6
*   **AI Engine**: Google Gemini API (`google.generativeai` with model `gemini-flash-latest`)
*   **Vector DB (RAG)**: ChromaDB (using model `gemini-embedding-001`)
*   **Database**: SQLite 3 (configured with WAL mode for performance)
*   **Data Export**: openpyxl
*   **Visualizations**: Matplotlib
*   **Image Processing**: Pillow (PIL)

---

## 🚀 Installation Guide

### 1. System Requirements
*   Python 3.10 or higher.
*   Git installed on your system.

### 2. Install Dependencies
Navigate to the project root directory and install requirements:
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory of the project and set your Google Gemini API key:
```env
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE
```

---

## 📂 Usage

### 1. Launching the Main Application
Run `main.py` to open the graphical user interface (GUI):
```bash
python main.py
```
*A startup Splash Screen will prepare the SQLite database, run cleanups, and synchronize ChromaDB vector collections before opening the main interface.*

### 2. Using the Batch Import Tool
If you have a local folder containing multiple book cover photos that you want to import in bulk:
1.  Place all cover images in the `images_input/` directory.
2.  Run the batch import script:
    ```bash
    python batch_import.py
    ```
3.  The script will automatically scan all images, analyze them using Gemini AI, save details in SQLite, save vector embeddings in ChromaDB, and move the processed covers to `images_processed/`.

---

## 🏗️ System Architecture

The application is structured into distinct layers:
*   `frontend/`: Contains the GUI layout and independent widgets (Book Table, Chatbot Widget, Statistics Dashboard, Dialogs).
*   `backend/`:
    *   `ai_service.py`: Handles connection with Gemini API for cover image analysis.
    *   `rag_service.py`: Interacts with ChromaDB for embedding storage and semantic RAG querying.
    *   `database.py`: DAO (Data Access Object) managing SQLite operations.
    *   `data_model.py`: Definitions of book schema.
*   `scripts/`: Automation scripts for linting and code quality (`check_modularity.py`, `audit_code_quality.py`, `git_guard.py`).

A detailed Mermaid diagram showing class call relationships is updated automatically at [docs/architecture/MAP_GRAPH.md](file:///d:/CloudStation/CODE/PYTHON_APP/22_THU_VIEN_AI_LOCAL_1212/docs/architecture/MAP_GRAPH.md).

---

## 📝 Changelog & Audit Reports
*   **Latest Codebase Quality Audit Report**: See [docs/CODE_AUDIT_REPORT_2026_07_08.md](file:///d:/CloudStation/CODE/PYTHON_APP/22_THU_VIEN_AI_LOCAL_1212/docs/CODE_AUDIT_REPORT_2026_07_08.md)
*   **Work Logs**: Available inside `docs/work_logs/`

---
*Developed and maintained by luulehai-lab & Antigravity (Senior Software Architect).*
