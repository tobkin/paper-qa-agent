from openai import OpenAI
client = OpenAI()

class Gpt35Generator:
  def __init__(self):
    self.system_prompt = f"""
      You are an assistant for question-answering tasks. 
      Use the following pieces of retrieved context to answer the question. 
      If you don't know the answer, just say that you don't know. 
      Use three sentences maximum and keep the answer concise.
      """

  def _generation_prompt(self, question, context): 
    return f"""
      Question: {question}
      Context: {context}
      Answer:
      """

  def generate(self, question, context):
    completion_obj = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": f"{self.system_prompt}"
        },
        {
          "role": "user",
          "content": f"{self._generation_prompt(question, context)}"
        }
      ],
      temperature=0,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return completion_obj.choices[0].message.content