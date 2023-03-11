class Config:
    def __init__(self, file, model_prefix, vocab_size, model_type, max_sentence_length):
        self.file = file
        self.model_prefix = model_prefix
        self.vocab_size = vocab_size
        self.model_type = model_type
        self.max_sentence_length = max_sentence_length