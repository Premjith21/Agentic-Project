import PyPDF2
import docx
import os
from groq import Groq

class DocumentProcessor:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.available_models = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "gemma2-9b-it",
            "qwen/qwen3-32b",
        ]
        self.user_documents = {}
    
    def call_llm(self, prompt: str, system_message: str = None) -> str:
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        # Try each model until one works
        for model in self.available_models:
            try:
                print(f"📄 Trying model for document processing: {model}")
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.1,
                    max_tokens=500
                )
                print(f"✅ Model {model} succeeded for document processing!")
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"❌ Model {model} failed for document processing: {str(e)}")
                continue
        
        return "Error: All available models failed for document processing."
    
    def process_document(self, user_id: str, file):
        """Process uploaded document and store text content"""
        try:
            # Create upload directory
            upload_dir = f"uploads/{user_id}"
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save file
            file_path = os.path.join(upload_dir, file.filename)
            file.save(file_path)
            
            # Extract text
            text = self.extract_text(file_path)
            
            # Store document data
            if user_id not in self.user_documents:
                self.user_documents[user_id] = {}
            
            self.user_documents[user_id][file.filename] = {
                "file_path": file_path,
                "text": text,
                "processed": True
            }
            
            return {
                "success": True, 
                "message": f"Document '{file.filename}' processed successfully",
                "char_count": len(text)
            }
            
        except Exception as e:
            return {
                "success": False, 
                "message": f"Error processing document: {str(e)}"
            }
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from PDF or Word documents"""
        try:
            if file_path.endswith('.pdf'):
                return self.extract_pdf_text(file_path)
            elif file_path.endswith('.docx'):
                return self.extract_docx_text(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
        except Exception as e:
            raise Exception(f"Error extracting text from {file_path}: {str(e)}")
    
    def extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"PDF extraction error: {str(e)}")
    
    def extract_docx_text(self, file_path: str) -> str:
        """Extract text from Word document"""
        text = ""
        try:
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"DOCX extraction error: {str(e)}")
    
    def query_document(self, user_id: str, question: str) -> str:
        """Answer questions based on processed document"""
        try:
            # Check if user has processed documents
            if user_id not in self.user_documents or not self.user_documents[user_id]:
                return "No documents processed for this user. Please upload a document first."
            
            # Get the first document (for simplicity)
            doc_name = list(self.user_documents[user_id].keys())[0]
            doc_data = self.user_documents[user_id][doc_name]
            document_text = doc_data['text']
            
            # Limit text length to avoid token limits
            if len(document_text) > 8000:
                document_text = document_text[:8000] + "... [document truncated]"
            
            # Create prompt for LLM
            prompt = f"""Based EXCLUSIVELY on the following document content, answer the user's question.

DOCUMENT CONTENT:
{document_text}

USER QUESTION: {question}

IMPORTANT INSTRUCTIONS:
1. Answer ONLY using information from the document content above
2. If the answer cannot be found in the document, say "I cannot find this information in the document"
3. Be concise and accurate
4. Do not make up information or use external knowledge

ANSWER:"""
            
            # Get response from Groq
            return self.call_llm(prompt, "You are a document analysis assistant. Answer questions based ONLY on the provided document content.")
            
        except Exception as e:
            return f"Error generating answer: {str(e)}"