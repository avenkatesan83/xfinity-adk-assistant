from fastapi import HTTPException

async def llm_response_to_text(llm_response: dict) -> str:
    try:
        #Iterate to collect the chunks into a single string
        full_response_text = ""
        
        async for chunk in llm_response:
            print(f"DEBUG: Processing chunk from: {getattr(chunk, 'author', 'Unknown')}")
            
            # Check for 'answer' attribute (Primary)
            if hasattr(chunk, 'answer') and chunk.answer:
                full_response_text += chunk.answer
                print("Found 'answer' attribute")
                continue # Move to next chunk to avoid double-processing this one

            # Check for Vertex AI Search Summary (High Priority)
            if hasattr(chunk, 'summary') and hasattr(chunk.summary, 'summary_text'):
                if chunk.summary.summary_text:
                    full_response_text += chunk.summary.summary_text
                    print("Found 'summary_text'")
                    continue # Found the best text, skip other parts of this chunk

            # Check Content Parts (Standard Model Text or Function Responses)
            if hasattr(chunk, 'content') and chunk.content.parts:
                for part in chunk.content.parts:
                    # Standard LLM Text
                    if hasattr(part, 'text') and part.text:
                        # Only add if it's not a duplicate of what we just added
                        if part.text.strip() not in full_response_text:
                            full_response_text += part.text
                            print("Found 'text' in part")

                    # Tool/Function Response Text (Fallback)
                    elif hasattr(part, 'function_response') and part.function_response:
                        resp_data = part.function_response.response
                        if isinstance(resp_data, dict) and 'responseText' in resp_data:
                            text_content = resp_data['responseText']
                            # ONLY append if we haven't already captured this text via 'summary'
                            if text_content.strip() not in full_response_text.strip():
                                full_response_text += text_content + "\n"
                                print("Found FunctionResponse text")

        return full_response_text

    except Exception as e:
        print(f"Agent Execution Error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error handling prompt with agent: {e}"
        )