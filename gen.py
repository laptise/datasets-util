import json
from os import getenv
from lib.load_json import load_json
from openai import OpenAI

bot_policy = '''
1. You are example generator, user gives you some examples in json format, you should generate another examples for it, as much as a lot you can answer.
2. You must keep the format of the examples that user provided.
3. Never include dupplicated examples that user provided.
4. Double check that the user provided examples are not duplicated before you generate new examples.
5. Create examples with as new a topic as possible that hasn't appeared in user-provided examples.
6. Your answer is must be correct json format.
'''

def dump_records():
    records = load_json("dumps")
    client = OpenAI(api_key=getenv("OPEN_AI_API_KEY"))
    
    for record in records:
        count = 0
        while count < 10:
            c = open(record, "r")
            content = c.read()
            c.close()
            try:
                arr = json.loads(content)
                res = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": bot_policy}, 
                        {"role": "user", "content": content} ]
                )
                generated = json.loads(res.choices[0].message.content or "[]")
                open(record, "w").write(json.dumps(arr + generated, indent=2))
                count += 1
                print(f"Dumped {record} {count} times")
            except Exception as e:
                print(e)
                count += 1
                print(f"Failed to dump {record} {count} times")

dump_records()
