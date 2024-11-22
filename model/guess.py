class Guess:
    def __init__(self, message, category_prompt, categories):
        self.message = message
        self.category_prompt = category_prompt
        self.categories = categories

    def display(self):
        print(f"Message: {self.message}")
        print(f"Category Prompt: {self.category_prompt}")
        print(f"Categories: {', '.join(self.categories)}")

    def to_dict(self):
        return {
            "message": self.message,
            "category_prompt": self.category_prompt,
            "categories": self.categories
        }