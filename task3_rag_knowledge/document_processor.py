"""
Document processing module for RAG Knowledge Base
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

# Document processing libraries
try:
    import PyPDF2
    from docx import Document
    import pandas as pd
except ImportError:
    PyPDF2 = None
    Document = None
    pd = None

from config import Config

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Process various document types for RAG system"""
    
    def __init__(self):
        self.config = Config()
        self.supported_extensions = {
            '.txt': self._process_text,
            '.pdf': self._process_pdf,
            '.docx': self._process_docx,
            '.csv': self._process_csv,
            '.json': self._process_json,
            '.md': self._process_markdown
        }
    
    def process_directory(self, directory_path: str) -> List[Dict]:
        """
        Process all documents in a directory
        
        Args:
            directory_path: Path to directory containing documents
            
        Returns:
            List of processed documents
        """
        try:
            directory = Path(directory_path)
            if not directory.exists():
                logger.error(f"Directory {directory_path} does not exist")
                return []
            
            documents = []
            
            for file_path in directory.rglob("*"):
                if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                    try:
                        doc = self.process_file(str(file_path))
                        if doc:
                            documents.append(doc)
                            logger.info(f"Processed: {file_path.name}")
                    except Exception as e:
                        logger.error(f"Error processing {file_path}: {e}")
                        continue
            
            logger.info(f"Processed {len(documents)} documents from {directory_path}")
            return documents
            
        except Exception as e:
            logger.error(f"Error processing directory {directory_path}: {e}")
            return []
    
    def process_file(self, file_path: str) -> Optional[Dict]:
        """
        Process a single file
        
        Args:
            file_path: Path to file to process
            
        Returns:
            Processed document dictionary or None
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.error(f"File {file_path} does not exist")
                return None
            
            if file_path.suffix.lower() not in self.supported_extensions:
                logger.warning(f"Unsupported file type: {file_path.suffix}")
                return None
            
            # Check file size
            if file_path.stat().st_size > self.config.max_document_size:
                logger.warning(f"File {file_path} too large, skipping")
                return None
            
            # Process file
            processor = self.supported_extensions[file_path.suffix.lower()]
            content = processor(str(file_path))
            
            if not content:
                logger.warning(f"No content extracted from {file_path}")
                return None
            
            # Create document metadata
            document = {
                "content": content,
                "metadata": {
                    "filename": file_path.name,
                    "filepath": str(file_path),
                    "file_size": file_path.stat().st_size,
                    "file_type": file_path.suffix.lower(),
                    "processed_at": datetime.now().isoformat(),
                    "language": self._detect_language(content)
                }
            }
            
            return document
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return None
    
    def _process_text(self, file_path: str) -> str:
        """Process text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
    
    def _process_pdf(self, file_path: str) -> str:
        """Process PDF file"""
        if not PyPDF2:
            logger.error("PyPDF2 not available for PDF processing")
            return ""
        
        try:
            content = ""
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    content += page.extract_text() + "\n"
            return content.strip()
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {e}")
            return ""
    
    def _process_docx(self, file_path: str) -> str:
        """Process DOCX file"""
        if not Document:
            logger.error("python-docx not available for DOCX processing")
            return ""
        
        try:
            doc = Document(file_path)
            content = ""
            for paragraph in doc.paragraphs:
                content += paragraph.text + "\n"
            return content.strip()
        except Exception as e:
            logger.error(f"Error processing DOCX {file_path}: {e}")
            return ""
    
    def _process_csv(self, file_path: str) -> str:
        """Process CSV file"""
        if not pd:
            logger.error("pandas not available for CSV processing")
            return ""
        
        try:
            df = pd.read_csv(file_path)
            # Convert to text representation
            content = df.to_string(index=False)
            return content
        except Exception as e:
            logger.error(f"Error processing CSV {file_path}: {e}")
            return ""
    
    def _process_json(self, file_path: str) -> str:
        """Process JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert to readable text
                content = json.dumps(data, indent=2, ensure_ascii=False)
                return content
        except Exception as e:
            logger.error(f"Error processing JSON {file_path}: {e}")
            return ""
    
    def _process_markdown(self, file_path: str) -> str:
        """Process Markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error processing Markdown {file_path}: {e}")
            return ""
    
    def _detect_language(self, text: str) -> str:
        """Detect language of text"""
        try:
            # Simple language detection based on character sets
            arabic_chars = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
            total_chars = len([char for char in text if char.isalpha()])
            
            if total_chars > 0 and arabic_chars / total_chars > 0.3:
                return 'ar'
            return 'en'
        except Exception:
            return 'en'
    
    def chunk_document(self, document: Dict) -> List[Dict]:
        """
        Chunk document into smaller pieces
        
        Args:
            document: Document dictionary
            
        Returns:
            List of document chunks
        """
        try:
            content = document["content"]
            metadata = document["metadata"]
            
            # Split content into chunks
            chunks = self._split_text(content)
            
            # Create chunk documents
            chunk_documents = []
            for i, chunk in enumerate(chunks):
                chunk_doc = {
                    "content": chunk,
                    "metadata": {
                        **metadata,
                        "chunk_id": f"{metadata['filename']}_chunk_{i}",
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    }
                }
                chunk_documents.append(chunk_doc)
            
            logger.info(f"Split document into {len(chunks)} chunks")
            return chunk_documents
            
        except Exception as e:
            logger.error(f"Error chunking document: {e}")
            return [document]  # Return original document if chunking fails
    
    def _split_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        try:
            # Simple text splitting by sentences and paragraphs
            sentences = text.split('. ')
            chunks = []
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk) + len(sentence) < self.config.chunk_size:
                    current_chunk += sentence + ". "
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence + ". "
            
            # Add the last chunk
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            # Ensure minimum chunk size
            final_chunks = []
            for chunk in chunks:
                if len(chunk) >= self.config.chunk_size // 2:  # Minimum chunk size
                    final_chunks.append(chunk)
                elif final_chunks:
                    # Merge with previous chunk
                    final_chunks[-1] += " " + chunk
                else:
                    final_chunks.append(chunk)
            
            return final_chunks
            
        except Exception as e:
            logger.error(f"Error splitting text: {e}")
            return [text]  # Return original text if splitting fails
