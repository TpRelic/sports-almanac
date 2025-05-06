import sys
import os
import pandas as pd
import io
from openai import OpenAI
from io import StringIO
from bs4 import BeautifulSoup

OpenAI.api_key = os.getenv("OPENAI_API_KEY") 
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

html = sys.stdin.read()

soup = BeautifulSoup(html, 'html.parser')
dfs = pd.read_html(StringIO(str(soup.prettify())))

summaries = []
for i, df in enumerate(dfs):
    summary = f"Table {i+1}:\n{df.to_markdown(index=False)}"
    summaries.append(summary)

tables_text = "\n\n".join(summaries)
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    instructions="Your are a NBA analyst. You will be provided a series of markdown tables and your job is to return a short paragraph giving general trends and insight into them.",
    input=tables_text,
)

print(response.output_text)

