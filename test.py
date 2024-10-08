import textgrad as tg

tg.set_backward_engine("hf://google/gemma-2b-it", override=True,)

# Step 1: Get an initial response from an LLM.
model = tg.BlackboxLLM("hf://google/gemma-2b-it")
question_string = ("If it takes 1 hour to dry 25 shirts under the sun, "
                   "how long will it take to dry 30 shirts under the sun? "
                   "Reason step by step")

question = tg.Variable(question_string, 
                       role_description="question to the LLM", 
                       requires_grad=False)

answer = model(question)