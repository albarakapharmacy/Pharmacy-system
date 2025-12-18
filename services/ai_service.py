from db.database import Database

class AIService:
    @staticmethod
    def suggest_reorder(limit=10):
        db = Database()
        query = '''
        SELECT p.name, SUM(si.qty) as sold
        FROM sale_items si
        JOIN products p ON p.id = si.product_id
        GROUP BY p.id
        ORDER BY sold DESC
        LIMIT ?
        '''
        return db.fetch_all(query, (limit,))