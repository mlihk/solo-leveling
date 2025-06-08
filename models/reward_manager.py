from config.database import get_db_connection
import sqlite3

class RewardManager:
    def __init__(self):
        # Initialize the database table for redeem codes
        self._init_database()
        
        # Predefined redeem codes
        self.redeem_codes = {
            'sololeveling': {
                'gold': 10000,
                'description': 'A special reward for starting your journey!'
            }
        }
    
    def _init_database(self):
        """Initialize the database table for tracking used redeem codes."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Create table for tracking used codes per user
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS used_redeem_codes (
                    account_id INTEGER,
                    code TEXT,
                    used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (account_id, code)
                )
            ''')
            
            conn.commit()
        except Exception as e:
            print(f"Database initialization error: {e}")
        finally:
            if conn:
                conn.close()
    
    def is_code_used(self, account_id, code):
        """Check if a code has been used by the specific account."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT 1 FROM used_redeem_codes WHERE account_id = ? AND code = ?",
                (account_id, code)
            )
            
            result = cursor.fetchone()
            return result is not None
        except Exception as e:
            print(f"Error checking code usage: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def mark_code_used(self, account_id, code):
        """Mark a code as used by the specific account."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO used_redeem_codes (account_id, code) VALUES (?, ?)",
                (account_id, code)
            )
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error marking code as used: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def redeem_code(self, player, code):
        """Redeem a code and give rewards to the player."""
        try:
            # Check if code exists
            if code not in self.redeem_codes:
                return False, "Invalid redeem code!"
            
            # Check if code has been used by this account
            if self.is_code_used(player.account_id, code):
                return False, "You have already used this code!"
            
            # Get rewards
            rewards = self.redeem_codes[code]
            
            # Apply rewards
            if 'gold' in rewards:
                player.gold += rewards['gold']
            
            # Mark code as used for this account
            if self.mark_code_used(player.account_id, code):
                return True, f"Successfully redeemed code! Received {rewards['gold']} gold!"
            else:
                return False, "Error processing your reward. Please try again."
                
        except Exception as e:
            print(f"Error redeeming code: {e}")
            return False, "An error occurred while processing your reward."
    
    def get_dialogue(self):
        """Get the reward manager's dialogue."""
        return {
            'greeting': "Welcome to the Reward Center! I can help you redeem special codes for rewards.",
            'help': "To redeem a code, just type 'redeem' followed by your code.",
            'invalid_code': "I'm sorry, but that code is not valid.",
            'used_code': "I'm sorry, but you have already used this code.",
            'success': "Excellent! Your rewards have been added to your account.",
            'farewell': "Come back anytime you have a code to redeem!"
        } 