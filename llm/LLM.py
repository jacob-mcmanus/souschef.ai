import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

class Mistral_LLM:
    def __init__(self):
        self.model_id = "mistralai/Mistral-7B-v0.1"
        self.bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            device_map="auto",
            torch_dtype=torch.float16,
            quantization_config=self.bnb_config
        )

    def run(self,prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True).to("cuda")
        outputs = self.model.generate(**inputs, max_new_tokens=512)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    
class Gemma_2B_LLM:
        def __init__(self):
            self.model_id = "google/gemma-2-2b-it"
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            quantization_config = BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_compute_dtype=torch.float16,bnb_4bit_use_double_quant=True, bnb_4bit_quant_type="nf4")
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                device_map="auto",
                quantization_config=quantization_config,
                torch_dtype=torch.float16
            )
            
        def run(self,prompt):
            inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
            outputs = self.model.generate(**inputs, max_new_tokens=512, do_sample=False, pad_token_id=self.tokenizer.eos_token_id)
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response

class Llama_3_2_1B_LLM:
        def __init__(self):
            self.model_id = "meta-llama/Llama-3.2-1B-Instruct"
            self.bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4"
            )
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                device_map="auto",
                torch_dtype=torch.float16,
                quantization_config=self.bnb_config
            )

        def run(self,prompt):
            inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
            outputs = self.model.generate(**inputs, max_new_tokens=512, do_sample=True, pad_token_id=self.tokenizer.eos_token_id)
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response

 
class Llama_3_2_3B_LLM:
        def __init__(self):
            self.model_id = "meta-llama/Llama-3.2-3B-Instruct"
            self.bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4"
            )
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                device_map="auto",
                torch_dtype=torch.float16,
                quantization_config=self.bnb_config
            )

        def run(self,prompt):
            inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
            outputs = self.model.generate(**inputs, max_new_tokens=512, do_sample=True, pad_token_id=self.tokenizer.eos_token_id)
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response
