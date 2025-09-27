"""
Query engine for RAG Knowledge Base
"""

import json
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime

try:
    import openai
except ImportError:
    openai = None

from config import Config

logger = logging.getLogger(__name__)

class QueryEngine:
    """Query engine for generating answers from retrieved context"""
    
    def __init__(self):
        self.config = Config()
        self.client = None
        
        if not self.config.use_mock_services and not self.config.mock_openai and self.config.openai_api_key:
            try:
                self.client = openai.OpenAI(api_key=self.config.openai_api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")
                self.client = None
    
    def generate_answer(self, question: str, search_results: List[Dict], language: str = "en") -> Dict:
        """
        Generate answer from question and search results
        
        Args:
            question: User question
            search_results: Retrieved context from vector search
            language: Language preference (en/ar)
            
        Returns:
            Dictionary with answer and sources
        """
        try:
            logger.info(f"Generating answer for question: {question[:50]}...")
            
            if self.client and not self.config.use_mock_services:
                return self._generate_with_openai(question, search_results, language)
            else:
                return self._generate_template_answer(question, search_results, language)
                
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return self._generate_fallback_answer(question, search_results, language)
    
    def _generate_with_openai(self, question: str, search_results: List[Dict], language: str) -> Dict:
        """Generate answer using OpenAI"""
        try:
            # Prepare context from search results
            context = self._prepare_context(search_results)
            
            # Create prompt based on language
            if language == "ar":
                prompt = self._create_arabic_prompt(question, context)
            else:
                prompt = self._create_english_prompt(question, context)
            
            # Generate answer
            response = self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt(language)},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            answer = response.choices[0].message.content
            
            # Calculate confidence based on source quality
            confidence = self._calculate_confidence(search_results)
            
            # Format sources
            sources = self._format_sources(search_results)
            
            return {
                "answer": answer,
                "sources": sources,
                "confidence": confidence,
                "language": language
            }
            
        except Exception as e:
            logger.error(f"OpenAI answer generation failed: {e}")
            return self._generate_template_answer(question, search_results, language)
    
    def _generate_template_answer(self, question: str, search_results: List[Dict], language: str) -> Dict:
        """Generate answer using template"""
        try:
            if not search_results:
                return self._generate_no_results_answer(question, language)
            
            # Prepare context
            context = self._prepare_context(search_results)
            
            # Generate template answer
            if language == "ar":
                answer = self._generate_arabic_template_answer(question, context)
            else:
                answer = self._generate_english_template_answer(question, context)
            
            # Format sources
            sources = self._format_sources(search_results)
            
            # Calculate confidence
            confidence = self._calculate_confidence(search_results)
            
            return {
                "answer": answer,
                "sources": sources,
                "confidence": confidence,
                "language": language
            }
            
        except Exception as e:
            logger.error(f"Error generating template answer: {e}")
            return self._generate_fallback_answer(question, search_results, language)
    
    def _generate_arabic_template_answer(self, question: str, context: str) -> str:
        """Generate Arabic template answer with proper RTL formatting"""
        # Format Arabic text properly for RTL display
        formatted_context = context[:500] + "..." if len(context) > 500 else context
        
        return f"""بناءً على المعلومات المتاحة في قاعدة المعرفة، إليك الإجابة على سؤالك:

السؤال: {question}

الإجابة:
{formatted_context}

ملاحظة: هذه إجابة مبنية على المعلومات المتاحة في قاعدة المعرفة. يرجى التأكد من صحة المعلومات قبل اتخاذ أي قرارات مهمة.

إذا كنت بحاجة إلى معلومات أكثر تفصيلاً، يرجى التواصل مع فريق المبيعات على sales@alrouf.com"""
    
    def _generate_english_template_answer(self, question: str, context: str) -> str:
        """Generate English template answer"""
        return f"""
Based on the information available in our knowledge base, here's the answer to your question:

Question: {question}

Answer:
{context[:500]}...

Note: This answer is based on the information available in our knowledge base. Please verify the information before making any important decisions.

If you need more detailed information, please contact our sales team at sales@alrouf.com
        """.strip()
    
    def _generate_no_results_answer(self, question: str, language: str) -> Dict:
        """Generate answer when no results found"""
        if language == "ar":
            answer = f"""
عذراً، لم أتمكن من العثور على معلومات كافية للإجابة على سؤالك: "{question}"

يرجى المحاولة مرة أخرى بصياغة مختلفة أو التواصل مع فريق المبيعات للحصول على المساعدة.

للتواصل: sales@alrouf.com أو +966 11 123 4567
            """.strip()
        else:
            answer = f"""
Sorry, I couldn't find sufficient information to answer your question: "{question}"

Please try rephrasing your question or contact our sales team for assistance.

Contact: sales@alrouf.com or +966 11 123 4567
            """.strip()
        
        return {
            "answer": answer,
            "sources": [],
            "confidence": 0.0,
            "language": language
        }
    
    def _generate_fallback_answer(self, question: str, search_results: List[Dict], language: str) -> Dict:
        """Generate fallback answer when all else fails"""
        if language == "ar":
            answer = "عذراً، حدث خطأ في معالجة سؤالك. يرجى المحاولة مرة أخرى أو التواصل مع فريق الدعم."
        else:
            answer = "Sorry, there was an error processing your question. Please try again or contact our support team."
        
        return {
            "answer": answer,
            "sources": self._format_sources(search_results),
            "confidence": 0.0,
            "language": language
        }
    
    def _prepare_context(self, search_results: List[Dict]) -> str:
        """Prepare context from search results"""
        try:
            context_parts = []
            
            for i, result in enumerate(search_results, 1):
                metadata = result.get("metadata", {})
                content = result.get("content", "")
                
                if content:
                    # Truncate content if too long
                    if len(content) > 500:
                        content = content[:500] + "..."
                    
                    context_parts.append(f"Source {i}: {content}")
                elif metadata.get("filename"):
                    context_parts.append(f"Source {i}: Information from {metadata['filename']}")
            
            return "\n\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Error preparing context: {e}")
            return "Context preparation failed"
    
    def _format_sources(self, search_results: List[Dict]) -> List[Dict]:
        """Format sources for response"""
        try:
            sources = []
            
            for result in search_results:
                metadata = result.get("metadata", {})
                source = {
                    "title": metadata.get("filename", "Unknown Document"),
                    "score": result.get("score", 0.0),
                    "file_type": metadata.get("file_type", "unknown"),
                    "language": metadata.get("language", "en")
                }
                sources.append(source)
            
            return sources
            
        except Exception as e:
            logger.error(f"Error formatting sources: {e}")
            return []
    
    def _calculate_confidence(self, search_results: List[Dict]) -> float:
        """Calculate confidence score based on search results"""
        try:
            if not search_results:
                return 0.0
            
            # Calculate average score
            scores = [result.get("score", 0.0) for result in search_results]
            avg_score = sum(scores) / len(scores)
            
            # Adjust based on number of results
            num_results = len(search_results)
            if num_results >= 3:
                confidence = min(avg_score * 1.2, 1.0)
            elif num_results >= 2:
                confidence = min(avg_score * 1.1, 1.0)
            else:
                confidence = avg_score
            
            return round(confidence, 2)
            
        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            return 0.0
    
    def _create_arabic_prompt(self, question: str, context: str) -> str:
        """Create Arabic prompt for OpenAI"""
        return f"""
أنت مساعد ذكي لشركة الأروف للتكنولوجيا والإضاءة. أجب على السؤال التالي بناءً على المعلومات المتاحة.

السؤال: {question}

المعلومات المتاحة:
{context}

يرجى تقديم إجابة مفيدة ومفصلة باللغة العربية. إذا لم تكن المعلومات كافية، اذكر ذلك بوضوح.
        """.strip()
    
    def _create_english_prompt(self, question: str, context: str) -> str:
        """Create English prompt for OpenAI"""
        return f"""
You are an intelligent assistant for Alrouf Lighting Technology. Answer the following question based on the available information.

Question: {question}

Available Information:
{context}

Please provide a helpful and detailed answer in English. If the information is insufficient, please state that clearly.
        """.strip()
    
    def _get_system_prompt(self, language: str) -> str:
        """Get system prompt based on language"""
        if language == "ar":
            return """
أنت مساعد ذكي متخصص في منتجات شركة الأروف للتكنولوجيا والإضاءة. 
تتمثل مهمتك في مساعدة العملاء بالإجابة على أسئلتهم حول منتجاتنا وخدماتنا.
أجب دائماً باللغة العربية وكن مفيداً ودقيقاً.
            """.strip()
        else:
            return """
You are an intelligent assistant specialized in Alrouf Lighting Technology products.
Your task is to help customers by answering their questions about our products and services.
Always respond in English and be helpful and accurate.
            """.strip()
    
    def get_query_stats(self) -> Dict:
        """Get query engine statistics"""
        try:
            stats = {
                "engine_type": "OpenAI" if self.client else "Template",
                "model": self.config.openai_model if self.client else "Template",
                "supported_languages": self.config.supported_languages,
                "status": "healthy"
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting query stats: {e}")
            return {"status": "error", "message": str(e)}
