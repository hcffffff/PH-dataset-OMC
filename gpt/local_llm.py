from transformers import AutoTokenizer, AutoModel


class ChatGLM():
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("../chatglm/chatglm-6b-int4", trust_remote_code=True)
        self.model = AutoModel.from_pretrained("../chatglm/chatglm-6b-int4", trust_remote_code=True).half().cuda()
        self.model = self.model.eval()

    
    def get_response(self, text):
        response, history = self.model.chat(self.tokenizer, text, history=[])
        return response