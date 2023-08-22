# openai_utils Library Documentation

## Version 2.1

### Importing the Library
To utilize the `openai_utils` library, you must first import the required modules:
```python
import openai
import numpy as np
from openai.embeddings_utils import cosine_similarity
```

### Functions

---

### **`AskGPT(model: str, Context, temperature: float = 1) -> str`**

##### Description
This function takes a model name, context, and temperature to generate a response using OpenAI's GPT models. The context can be either a list of messages or a single string.

##### Parameters
- `model` (str): The name of the model to use for the completion (e.g., "text-davinci-003").
- `Context`: A list of messages or a single string to use as context.
- `temperature` (float, optional): Controls the randomness of the output. Default value is 1.

##### Returns
- str: The content of the generated response.

---

### **`CreateEmbedding(String: str) -> list`**

##### Description
This function takes a string and returns its embedding using the specified OpenAI model.

##### Parameters
- `String` (str): The input text for which the embedding is to be created.

##### Returns
- list: The embedding of the input string.

---

### **`GetEmbeddingDistance(Embedding1: list, Embedding2: list) -> float`**

##### Description
This function calculates the cosine similarity between two embeddings.

##### Parameters
- `Embedding1` (list): The first embedding vector.
- `Embedding2` (list): The second embedding vector.

##### Returns
- float: The cosine similarity between the two embeddings. Note that the return value is missing in the given code snippet, so you may need to update the function to return the computed value.

---

### Examples and Use Cases

Please refer to the respective library's documentation for examples on how to use the `openai` module, including specific models and methods.