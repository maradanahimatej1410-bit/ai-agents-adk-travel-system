import asyncio
from google.adk import Agent
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session
from google.genai import types

import os
from dotenv import load_dotenv

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from callback_logging import log_query_to_model, log_model_response
import google.cloud.logging

from pydantic import BaseModel  #  Added

#  Define schema
class CountryCapital(BaseModel):
    capital: str

# Load environment variables
load_dotenv()
google_cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT")
google_cloud_location = os.getenv("GOOGLE_CLOUD_LOCATION")
google_genai_use_vertexai = os.getenv("GOOGLE_GENAI_USE_VERTEXAI")
model_name = os.getenv("MODEL")

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()


# Create an async main function
async def main():

    app_name = 'geo_validator_app'
    user_id_1 = 'user1'

    #  Agent with schema + transfer disabled
    root_agent = Agent(
        model=model_name,
        name="geo_validator",
        instruction="Return ONLY the capital city in JSON format.",
        before_model_callback=log_query_to_model,
        after_model_callback=log_model_response,

        output_schema=CountryCapital,              # ✅ Enforce JSON
        disallow_transfer_to_parent=True,          # ✅ Disable parent transfer
        disallow_transfer_to_peers=True,           # ✅ Disable peer transfer
    )

    # Runner
    runner = InMemoryRunner(
        agent=root_agent,
        app_name=app_name,
    )

    # Session
    my_session = await runner.session_service.create_session(
        app_name=app_name, user_id=user_id_1
    )

    # Function to run prompt
    async def run_prompt(session: Session, new_message: str):
        content = types.Content(
            role='user',
            parts=[types.Part.from_text(text=new_message)]
        )
        print('** User says:', content.model_dump(exclude_none=True))

        async for event in runner.run_async(
            user_id=user_id_1,
            session_id=session.id,
            new_message=content,
        ):
            if event.content.parts and event.content.parts[0].text:
                print(f'** {event.author}: {event.content.parts[0].text}')

        cloud_logging_client.close()

    # Test query
    query = "What is the capital of France?"
    await run_prompt(my_session, query)


if __name__ == "__main__":
    asyncio.run(main())