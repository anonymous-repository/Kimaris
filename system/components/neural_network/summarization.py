
# External Libraries
from simpletransformers.seq2seq import Seq2SeqModel, Seq2SeqArgs
import language_check

tool = language_check.LanguageTool('en-US')
def create_network():
    # Configure the model
    model_args = Seq2SeqArgs()
    model_args.padding = "longest"
    model_args.length_penalty = 1
    model_args.truncation = True
    model_args.max_length = 512
    

    model = Seq2SeqModel(
        encoder_decoder_type="bart",
        encoder_decoder_name="facebook/bart-large-cnn",
        args=model_args,
    )
    return model


def summarize(model, data):
    n = 512
    length = len(data)
    
    snnipets = []
        
    index = 0
    last_i = 0
    while index < length:
        i = data.rfind(". ", index, index + n)
        if i == -1 or i == index:
            i = index + n
        text = data[index : i + 2]
        index = i + 2
        snnipets.append(text)
        
    result = model.predict(
            snnipets
    )
    
    result = " ".join(result)
    
    matches = tool.check(result)
    
    result = language_check.correct(result, matches)
    
    return result
