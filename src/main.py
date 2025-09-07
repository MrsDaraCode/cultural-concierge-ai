import openai
import confi
from inputimeout import inputimeout, TimeoutOccurred
import typer
from rich import print
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

    # Configura tu API key
    openai.api_key = confi.API_KEY

    print("[bold dark_green]Adan ChatGPT is your Ireland assistant[/bold dark_green]")

    # Mensaje system para marcar estilo y formato trilingüe
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

    # Mensaje de bienvenida
    bubble(
        "Good day, I am Adan. How may I be of assistance to you today?\n"
        "Bonjour, je suis Adan. En quoi puis-je vous être utile aujourd’hui ?\n"
        "Buenos días, soy Adan. ¿En qué puedo serle de ayuda hoy?\n"
        "(type 'exit' / 'quit' / 'salir' to end)\n",
        title="Adan",
        color="gold3"
    )

    while True:
        try:
            # Espera máximo 60 segundos para la respuesta del usuario
            content = inputimeout(prompt="→ ", timeout=60).strip()
        except TimeoutOccurred:
            bubble("⏳ Conversation ended: no response within 1 minute.", title="System", color="grey70")
            break
        except KeyboardInterrupt:
            bubble("👋 Conversation ended by user (Ctrl+C).", title="System", color="grey70")
            break

        if not content:
            continue

        if content.lower() in {"exit", "quit", "salir"}:
            bubble("👋 Conversation ended by user.", title="System", color="grey70")
            break

        # Muestra lo que escribió el usuario
        bubble(content, title="You", color="dark_green")

        # Añadimos el mensaje del usuario a la conversación
        messages.append({"role": "user", "content": content})

        # Llamada al modelo con el historial completo
        response = openai.chat.completions.create(
            model=confi.MODEL,
            messages=messages,
            temperature=0.6,
        )

        reply = response.choices[0].message.content.strip()

        # Muestra la respuesta en un bocadillo dorado
        bubble(reply, title="Adan", color="gold3")

        # Añadimos la respuesta al historial
        messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    typer.run(main)
