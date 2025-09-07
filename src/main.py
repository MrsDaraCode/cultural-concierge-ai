import openai
import os
from dotenv import load_dotenv
from inputimeout import inputimeout, TimeoutOccurred
import typer
from rich.console import Console
from rich.panel import Panel
from rich import box

console = Console()

def bubble(text: str, title: str, color: str):
    """Muestra texto dentro de un panel estilo bocadillo."""
    console.print(
        Panel(
            text,
            title=title,
            border_style=color,
            box=box.ROUNDED,
            padding=(1, 2)
        )
    )

def main():
    # Cargar variables desde .env
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-5-nano")
    use_mock = os.getenv("USE_MOCK", "true").lower() == "true"

    bubble("Adan ChatGPT is your Ireland assistant", "System", "dark_green")

    # Mensaje system
    messages = [{
        "role": "system",
        "content": (
            "You are a cultured assistant with a timeless, discreet tone. "
            "Always respond to the user in three languages — English, French, and Spanish — "
            "each as a separate paragraph. Ensure elegance, accuracy, and conciseness. "
            "Use a refined style appropriate for high culture and professional contexts. Be charming. "
            "If I do not mention the city, assume that I am referring to Dublin. "
            "Provide specific details: renowned shops, places, and landmarks. "
            "Choose among those most highly regarded and with the richest history. "
            "If I ask where to go or about a particular location, give me cultural and touristic information about it — "
            "interesting facts and a touch of its history. "
            "If I speak to you in only one language, reply in that language."
        )
    }]

    bubble(
        "Good day, I am Adan. How may I be of assistance to you today?\n"
        "Bonjour, je suis Adan. En quoi puis-je vous être utile aujourd’hui ?\n"
        "Buenos días, soy Adan. ¿En qué puedo serle de ayuda hoy?\n"
        "(type 'exit' / 'quit' / 'salir' to end)\n",
        "Adan",
        "gold3"
    )

    while True:
        try:
            content = inputimeout(prompt="→ ", timeout=60).strip()
        except TimeoutOccurred:
            bubble("⏳ Conversation ended: no response within 1 minute.", "System", "grey70")
            break
        except KeyboardInterrupt:
            bubble("👋 Conversation ended by user (Ctrl+C).", "System", "grey70")
            break

        if not content:
            continue

        if content.lower() in {"exit", "quit", "salir"}:
            bubble("👋 Conversation ended by user.", "System", "grey70")
            break

        bubble(content, "You", "dark_green")

        if use_mock:
            reply = "This is a mock response. (Enable API in .env to get real answers.)"
        else:
            response = openai.chat.completions.create(
                model=model,
                messages=messages + [{"role": "user", "content": content}],
                temperature=0.6,
            )
            reply = response.choices[0].message.content.strip()

        bubble(reply, "Adan", "gold3")
        messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    typer.run(main)
