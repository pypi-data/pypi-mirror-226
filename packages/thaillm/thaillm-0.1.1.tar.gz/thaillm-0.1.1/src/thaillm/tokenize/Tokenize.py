import os
import sentencepiece as spm
THISDIR, THISFILENAME = os.path.split(__file__)
class Tokenize(object):
    def __init__(self):
        self.sp_model = spm.SentencePieceProcessor()
        self.st_model = False
        self.vocab_size = 0
    def initModel(self,inputModel=os.path.join(THISDIR, "input/th_tokenizer_32000.model")):
        self.st_model = self.sp_model.Load(inputModel)
        self.vocab_size = self.sp_model.get_piece_size()
    def status_cls(self):
        return self.st_model
    def get_vocabSize(self):
        return self.vocab_size
    def get_vocabList(self):
        return [self.sp_model.id_to_piece(i) for i in range(self.vocab_size)]
    def vocab2file(self,vocab_path):
        with open(vocab_path, "w", encoding="utf-8") as f:
            for i in range(self.vocab_size):
                f.write(self.sp_model.id_to_piece(i) + "\n")
    def vocab2file_withWeight(self,vocab_path):
        with open(vocab_path, "w", encoding="utf-8") as f:
            for i in range(self.sp_model.get_piece_size()):
                token = self.sp_model.id_to_piece(i)
                weight = self.sp_model.get_score(i)
                f.write(f"{token} {weight}\n")
    def encode(self,text):
        return self.sp_model.encode(text)
    def decode(self,text):
        return self.sp_model.decode(text)
    def token_str(self,text):
        return self.sp_model.Tokenize(text, out_type=str)
    def token(self,text):
        resList = []
        for resEnc in self.encode(text):
            resList.append(self.decode(resEnc))
        return resList    
