'''
suggestions
we cant rely just on the JD. Need more data to do matching (maybe create a dataset and store data corresponding to every position (generic for every company))
the above thing will improve similarity score and also help in giving suggestions, like we can suggest keywords from our dataset.


Resume generator 
Parallel computaion dekhle (do paraphrasing on gpu than cpu's)  Ray, Hugg Do Face ||ism

'''
def paraphrase_sentence(model, tokenizer, text, max_length=128):

  input_ids = tokenizer.encode(text, return_tensors="pt", add_special_tokens=True)
  generated_ids = model.generate(input_ids=input_ids, num_return_sequences=3, num_beams=5, max_length=max_length, no_repeat_ngram_size=2, repetition_penalty=6.0, length_penalty=1.0, early_stopping=True)
  
  preds = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in generated_ids]

  return preds

def paraphrase_fn(model, tokenizer, p_text):

    phrases = p_text.split('.')
    ans = []
    for phrase in phrases:
        temp = paraphrase_sentence(model=model, tokenizer=tokenizer, text=phrase)
        ans.append(temp)
    return ans


if __name__ == '__main__':
    paraphrase_fn()