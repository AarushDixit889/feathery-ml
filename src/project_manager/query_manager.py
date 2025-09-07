"""
Blueprint: Project Manager - Query Manager

This module handles the processing of user queries, manages the QnA history,
and orchestrates the analysis workflow.

Components:
1. Query Processing
2. History Management
3. Analysis Workflow
4. Result Management
5. Context Management
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
import json
from dataclasses import dataclass
from datetime import datetime
from ..ai_engine.code_generator import CodeGenerator
from ..data_handlers.data_processor import DataProcessor
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

@dataclass
class QueryResult:
    """Structure for query results"""
    query: str
    code: str
    result: Any
    timestamp: str
    context: Optional[Dict[str, Any]] = None

class QueryManager:
    """Handles query processing and history management"""
    
    def __init__(self):
        self.code_generator = CodeGenerator()
        self.data_processor = DataProcessor()
        self.context: Dict[str, Any] = {}
        
    def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> QueryResult:
        """
        Process a natural language query
        
        Args:
            query: User's natural language query
            context: Optional context from previous queries
            
        Returns:
            QueryResult: Results of the analysis
        """
        try:
            # Update context
            if context:
                self.context.update(context)
            
            # Generate and execute code
            code = self.code_generator.generate(query, self.context)
            result = self._execute_analysis(code)
            
            # Create result object
            query_result = self._create_result(query, code, result)
            
            # Update history
            self._update_history(query_result)
            
            return query_result
            
        except Exception as e:
            logger.error(f"Query processing failed: {str(e)}")
            raise
            
    def _execute_analysis(self, code: str) -> Any:
        """Execute generated code safely"""
        # TODO: Implement safe code execution
        return "Analysis results placeholder"
        
    def _create_result(self, query: str, code: str, result: Any) -> QueryResult:
        """Create structured result object"""
        return QueryResult(
            query=query,
            code=code,
            result=result,
            timestamp=datetime.now().isoformat(),
            context=self.context.copy()
        )
        
    def _update_history(self, result: QueryResult):
        """Update QnA history file"""
        try:
            qna_file = Path.cwd() / "qna.json"
            
            # Load existing history
            if qna_file.exists():
                history = json.loads(qna_file.read_text())
            else:
                history = []
                
            # Add new result
            history.append({
                "query": result.query,
                "code": result.code,
                "timestamp": result.timestamp,
                "context": result.context
            })
            
            # Save updated history
            qna_file.write_text(json.dumps(history, indent=2))
            
        except Exception as e:
            logger.error(f"History update failed: {str(e)}")
            raise
            
    def bulk_update_history(self, entries: List[Dict[str, Any]]):
        """
        Update history with multiple entries
        
        Args:
            entries: List of history entries
        """
        try:
            qna_file = Path.cwd() / "qna.json"
            
            # Load existing history
            if qna_file.exists():
                history = json.loads(qna_file.read_text())
            else:
                history = []
                
            # Add new entries
            history.extend(entries)
            
            # Save updated history
            qna_file.write_text(json.dumps(history, indent=2))
            
        except Exception as e:
            logger.error(f"Bulk history update failed: {str(e)}")
            raise
