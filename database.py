import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor
import json

class Database:
    def __init__(self):
        """
        Initialize the database connection using local PostgreSQL settings
        """
        self.conn = psycopg2.connect(
            dbname='your_database_name',
            user='your_username',
            password='your_password',
            host='localhost',
            port='5432'
        )
        self._create_tables()

    def _create_tables(self):
        """
        Create necessary tables if they don't exist
        """
        with self.conn.cursor() as cur:
            # Create ethics_cases table
            cur.execute('''
                CREATE TABLE IF NOT EXISTS ethics_cases (
                    id SERIAL PRIMARY KEY,
                    case_title VARCHAR(255) NOT NULL,
                    dilemma_text TEXT NOT NULL,
                    dilemma_context TEXT,
                    dilemma_stakeholders TEXT,
                    classification VARCHAR(50) NOT NULL,
                    ethics_score INTEGER NOT NULL,
                    explanation TEXT NOT NULL,
                    implications JSONB,
                    recommendations JSONB,
                    factors JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.commit()

    def save_case(self, case_data):
        """
        Save an ethics case to the database
        
        Args:
            case_data: Dictionary containing case information
            
        Returns:
            id: The ID of the newly created case
        """
        with self.conn.cursor() as cur:
            query = '''
                INSERT INTO ethics_cases (
                    case_title, dilemma_text, dilemma_context, dilemma_stakeholders,
                    classification, ethics_score, explanation, implications,
                    recommendations, factors
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            '''
            
            # Convert list and dict to JSON strings for JSONB fields
            implications_json = json.dumps(case_data.get('implications', []))
            recommendations_json = json.dumps(case_data.get('recommendations', []))
            factors_json = json.dumps(case_data.get('factors', {}))
            
            cur.execute(query, (
                case_data.get('case_title'),
                case_data.get('dilemma_text'),
                case_data.get('dilemma_context'),
                case_data.get('dilemma_stakeholders'),
                case_data.get('classification'),
                case_data.get('ethics_score'),
                case_data.get('explanation'),
                implications_json,
                recommendations_json,
                factors_json
            ))
            
            case_id = cur.fetchone()[0]
            self.conn.commit()
            
            return case_id

    def get_case(self, case_id):
        """
        Retrieve a case by its ID
        
        Args:
            case_id: The ID of the case to retrieve
            
        Returns:
            dict: The case data or None if not found
        """
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            query = "SELECT * FROM ethics_cases WHERE id = %s"
            cur.execute(query, (case_id,))
            
            result = cur.fetchone()
            if result is None:
                return None
                
            # Convert row to dict and parse JSON fields
            case = dict(result)
            # Parse JSON fields if they're not None
            if case['implications']:
                case['implications'] = json.loads(case['implications'])
            if case['recommendations']:
                case['recommendations'] = json.loads(case['recommendations'])
            if case['factors']:
                case['factors'] = json.loads(case['factors'])
            
            return case

    def get_all_cases(self, limit=100):
        """
        Retrieve all cases with optional limit
        
        Args:
            limit: Maximum number of cases to retrieve
            
        Returns:
            list: List of case dictionaries
        """
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            query = "SELECT * FROM ethics_cases ORDER BY created_at DESC LIMIT %s"
            cur.execute(query, (limit,))
            
            results = cur.fetchall()
            cases = []
            
            for row in results:
                case = dict(row)
                # Parse JSON fields if they're not None
                if case['implications']:
                    case['implications'] = json.loads(case['implications'])
                if case['recommendations']:
                    case['recommendations'] = json.loads(case['recommendations'])
                if case['factors']:
                    case['factors'] = json.loads(case['factors'])
                cases.append(case)
                
            return cases

    def search_cases(self, search_term):
        """
        Search for cases based on title or dilemma text
        
        Args:
            search_term: Text to search for
            
        Returns:
            list: Matching cases
        """
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            query = '''
                SELECT * FROM ethics_cases 
                WHERE case_title ILIKE %s 
                OR dilemma_text ILIKE %s
                ORDER BY created_at DESC
            '''
            search_pattern = f'%{search_term}%'
            cur.execute(query, (search_pattern, search_pattern))
            
            results = cur.fetchall()
            cases = []
            
            for row in results:
                case = dict(row)
                # Parse JSON fields if they're not None
                if case['implications']:
                    case['implications'] = json.loads(case['implications'])
                if case['recommendations']:
                    case['recommendations'] = json.loads(case['recommendations'])
                if case['factors']:
                    case['factors'] = json.loads(case['factors'])
                cases.append(case)
                
            return cases

    def get_cases_by_classification(self, classification):
        """
        Get cases filtered by classification
        
        Args:
            classification: The ethical classification to filter by
            
        Returns:
            list: Matching cases
        """
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            query = '''
                SELECT * FROM ethics_cases 
                WHERE classification = %s
                ORDER BY created_at DESC
            '''
            cur.execute(query, (classification,))
            
            results = cur.fetchall()
            cases = []
            
            for row in results:
                case = dict(row)
                # Parse JSON fields if they're not None
                if case['implications']:
                    case['implications'] = json.loads(case['implications'])
                if case['recommendations']:
                    case['recommendations'] = json.loads(case['recommendations'])
                if case['factors']:
                    case['factors'] = json.loads(case['factors'])
                cases.append(case)
                
            return cases

    def delete_case(self, case_id):
        """
        Delete a case by its ID
        
        Args:
            case_id: The ID of the case to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with self.conn.cursor() as cur:
                query = "DELETE FROM ethics_cases WHERE id = %s"
                cur.execute(query, (case_id,))
                self.conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Error deleting case: {e}")
            return False

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()