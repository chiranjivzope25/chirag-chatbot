from transformers import AutoTokenizer,AutoModelForCausalLM
import torch 
model_using = "microsoft/DialoGPT-medium"

tokenizer=AutoTokenizer.from_pretrained(model_using)
tokenizer.pad_token=tokenizer.eos_token
model=AutoModelForCausalLM.from_pretrained(model_using)

def chatbot(user_input,cht_hist_ids=None):
  new_ids=tokenizer.encode(user_input+tokenizer.eos_token,return_tensors="pt",truncation=True,padding=True)
  if cht_hist_ids is not None:
    bot_ids=torch.cat([cht_hist_ids,new_ids],dim=-1)
  else:
    bot_ids=new_ids
  model_ids=model.generate(bot_ids,pad_token_id=tokenizer.eos_token_id,temperature=1.0 ,top_k=50,top_p=0.96)
  response=tokenizer.decode(model_ids[:,bot_ids.shape[-1]:][0],skip_special_token=True)
  response=response.replace("<|endoftext|>"," ")
  return response
  
