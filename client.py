from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

API_KEY=os.getenv("API_KEY")

curr_dir=os.path.dirname(os.path.abspath(__file__))
server_dir=os.path.join(curr_dir,"servers.py")
print(curr_dir)
print(server_dir)
client=MultiServerMCPClient({
    "access_files":{
        "command":"python",
        "args":[server_dir],
        "transport":"stdio"
    }
})





async def main():
    tools= await client.get_tools()
    print("Available Tools : ")
    for tool in tools:
        print(tool.name," -> ",tool.description)

    llm = ChatNVIDIA(
        model="meta/muse-glimmer-30b",
        api_key=API_KEY, 
        temperature=0.5,
        top_p=0.95,
        max_tokens=8192,
    )
    checkpointer=InMemorySaver()
    config={
        "configurable":{
            "thread_id":"user-1"
        }
    }
    SYSTEM_PROMPT="""You are the professional software engineer your job is to help the user based on their query.
    you have access to the two tools get files names and get the content of the files. You must behave like a careful senior software engineer.
    Do NOT blindly generate code based only on the user's description.
    When solving a problem, follow this general process:

    1. Understand the user's request.
    2. Identify the files relevant to the request.
    3. Read the relevant files.
    4. Identify the actual root cause.
    5. give the fixed code
    6. for writing in the file always take user permission. if user accepts it then you can write to the file otherwise just say user has denied the write
    7. while writing code into the file make sure to only write the code do not write the explanation into it
    8. if user asks to write into the new file just check all the names of the available files in the dir and create a new file with the name that is not present to prevent the conflict
    9. if it is a code file make sure you give the right extension to the file name if python code .py, if js code .js like that.

    """
    agent=create_agent(model=llm,tools=tools,system_prompt=SYSTEM_PROMPT,checkpointer=checkpointer)

    while True:
        user_prompt=input("Ask Something... ")
        if user_prompt in ["bye","stop"]:
            break
        result=await agent.ainvoke({
            "messages":[
                {
                    "role":"user",
                    "content":user_prompt
                }
            ]
        },
        config=config
        )
        print(result["messages"][-1].content)

asyncio.run(main())

