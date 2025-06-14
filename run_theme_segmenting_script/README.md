**PIPELINE:**

- script 1 manages input / output (iterates through folder, PDF by PDF, puts each article into OpenAI querier, & adds result to CSV)

- script 2 extracts all articles from a given PDF and outputs them as a JSON file of {title, text} 

- script 3 intakes 1 article and outputs the same article, segmented by theme using OpenAI prompting. (Format: JSON of theme, text)

** prompting notes: **
Our prompt gives the themes, without providing examples (originally lengthy); this makes the prompt more succinct & thus more cost-effective and easier for ChatGPT to parse without getting lost in the weeds. We fine-tune our model by giving it examples of human-coded articles.

** design notes: ** 
- Our final output is a CSV, but we use JSON as an intermediate object so I don't have to wrangle with commas within the article text. 
- Having a pipeline of inputs / outputs like such makes it easy to modularize troubleshooting.