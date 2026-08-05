import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_summary(incident):
    prompt = f"""
    Summarize this power outage.

    Incident ID: {incident.incident_id}
    Start Pole: {incident.start_pole.pole_id}
    End Pole: {incident.end_pole.pole_id}
    Confidence: {incident.confidence}
    Status: {incident.status}

    Give a short summary in 3-4 lines.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content