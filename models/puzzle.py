import random
import math

class Puzzle:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.puzzle_type = random.choice(['math', 'sequence', 'riddle'])
        self.solved = False
        self.attempts = 0
        self.max_attempts = 3
        
        # Generate puzzle based on type
        if self.puzzle_type == 'math':
            self.generate_math_puzzle()
        elif self.puzzle_type == 'sequence':
            self.generate_sequence_puzzle()
        else:  # riddle
            self.generate_riddle_puzzle()
    
    def generate_math_puzzle(self):
        """Generate a math puzzle based on difficulty."""
        operations = ['+', '-', '*']
        if self.difficulty > 20:
            operations.append('/')
        
        op = random.choice(operations)
        if op == '+':
            num1 = random.randint(1, 10 * self.difficulty)
            num2 = random.randint(1, 10 * self.difficulty)
            self.answer = num1 + num2
            self.question = f"What is {num1} + {num2}?"
        elif op == '-':
            num1 = random.randint(1, 10 * self.difficulty)
            num2 = random.randint(1, num1)  # Ensure positive result
            self.answer = num1 - num2
            self.question = f"What is {num1} - {num2}?"
        elif op == '*':
            num1 = random.randint(1, 5 * self.difficulty)
            num2 = random.randint(1, 5 * self.difficulty)
            self.answer = num1 * num2
            self.question = f"What is {num1} × {num2}?"
        else:  # division
            num2 = random.randint(1, 5 * self.difficulty)
            self.answer = random.randint(1, 5 * self.difficulty)
            num1 = num2 * self.answer
            self.question = f"What is {num1} ÷ {num2}?"
    
    def generate_sequence_puzzle(self):
        """Generate a sequence puzzle based on difficulty."""
        sequence_types = ['arithmetic', 'geometric', 'fibonacci']
        if self.difficulty > 30:
            sequence_types.append('alternating')
        
        seq_type = random.choice(sequence_types)
        if seq_type == 'arithmetic':
            start = random.randint(1, 10)
            diff = random.randint(1, 5)
            self.sequence = [start + (i * diff) for i in range(4)]
            self.answer = start + (4 * diff)
            self.question = f"Complete the sequence: {', '.join(map(str, self.sequence))}, ?"
        elif seq_type == 'geometric':
            start = random.randint(1, 5)
            ratio = random.randint(2, 4)
            self.sequence = [start * (ratio ** i) for i in range(4)]
            self.answer = start * (ratio ** 4)
            self.question = f"Complete the sequence: {', '.join(map(str, self.sequence))}, ?"
        elif seq_type == 'fibonacci':
            start1 = random.randint(1, 5)
            start2 = random.randint(1, 5)
            self.sequence = [start1, start2]
            for _ in range(2):
                self.sequence.append(self.sequence[-1] + self.sequence[-2])
            self.answer = self.sequence[-1] + self.sequence[-2]
            self.question = f"Complete the sequence: {', '.join(map(str, self.sequence))}, ?"
        else:  # alternating
            start = random.randint(1, 10)
            self.sequence = [start]
            for i in range(3):
                if i % 2 == 0:
                    self.sequence.append(self.sequence[-1] * 2)
                else:
                    self.sequence.append(self.sequence[-1] + 3)
            self.answer = self.sequence[-1] * 2
            self.question = f"Complete the sequence: {', '.join(map(str, self.sequence))}, ?"
    
    def generate_riddle_puzzle(self):
        """Generate a riddle puzzle based on difficulty."""
        riddles = [
            {
                "question": "I am not alive, but I grow; I don't have lungs, but I need air; I don't have a mouth, but I can be killed. What am I?",
                "answer": "fire"
            },
            {
                "question": "What has keys, but no locks; space, but no room; and you can enter, but not go in?",
                "answer": "keyboard"
            },
            {
                "question": "What gets wetter and wetter the more it dries?",
                "answer": "towel"
            },
            {
                "question": "What has a head and a tail that will never meet?",
                "answer": "coin"
            },
            {
                "question": "What can you catch but not throw?",
                "answer": "cold"
            }
        ]
        riddle = random.choice(riddles)
        self.question = riddle["question"]
        self.answer = riddle["answer"]
    
    def check_answer(self, user_answer):
        """Check if the user's answer is correct."""
        self.attempts += 1
        
        if self.puzzle_type in ['math', 'sequence']:
            try:
                user_answer = int(user_answer)
                return user_answer == self.answer
            except ValueError:
                return False
        else:  # riddle
            return user_answer.lower().strip() == self.answer.lower()
    
    def get_hint(self):
        """Get a hint for the puzzle."""
        if self.puzzle_type == 'math':
            return "Remember to follow the order of operations!"
        elif self.puzzle_type == 'sequence':
            return "Look for a pattern in how the numbers change."
        else:  # riddle
            return "Think about the literal meaning of the words."
    
    def is_solved(self):
        """Check if the puzzle is solved."""
        return self.solved
    
    def get_remaining_attempts(self):
        """Get the number of remaining attempts."""
        return self.max_attempts - self.attempts 