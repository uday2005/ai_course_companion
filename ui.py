import gradio as gr
from app import agent

async def ask_agent(query):
    result = await agent.run(query)
    # If result is a dict or list, extract the answer text
    if isinstance(result, dict) and "output" in result:
        return result["output"]
    elif isinstance(result, list) and len(result) > 0:
        # Try to extract from first element if it's a dict
        if isinstance(result[0], dict) and "output" in result[0]:
            return result[0]["output"]
        return str(result)
    return str(result)

gr.Interface(
    fn=ask_agent,
    inputs=gr.Textbox(lines=10, label="query"),
    outputs=gr.Textbox(lines=50, label="output"),  # Bigger output box
    title="🤖 AI Course Companion"
).launch(share=True)