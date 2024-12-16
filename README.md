# QuizBot Setup

## Prerequisites
- Python 3.x
- pip
- OpenAI API key

## Installation Steps

1. **Clone the Repository**
   ```
   git clone <repository-url>
   cd quizbot
   ```

2. **Create Virtual Environment**
   - macOS/Linux:
     ```
     python3 -m venv myenv
     source myenv/bin/activate
     ```
   - Windows:
     ```
     python -m venv myenv
     myenv\Scripts\activate
     ```

3. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Configure API Key**
   Create a `.env` file and add your OpenAI API key:
   ```
   echo "OPENAI_API_KEY='your-api-key-here'" > .env
   ```

5. **Run the Program**
   ```
   python chris.py
   ```

6. **Deactivate Virtual Environment (when done)**
   ```
   deactivate
   ```

## Notes
- Ensure you have a valid OpenAI API key
- Keep your `.env` file private and do not commit it to version control
