import asyncio
from nicegui import ui
from RAG.query import generate_response

def main():
    # Header or Title
    ui.label('Chat with My RAG Prototype').classes('text-2xl font-bold m-4')

    with ui.column().classes('w-full max-w-xl mx-auto'):
        chat_history = ui.column().classes('gap-2 border rounded p-4 mb-4')
        
        user_input = ui.input('Type your message...').classes('w-full')

        # A function to handle sending the user's message
        async def send_message():
            query = user_input.value
            if not query.strip():
                return
            # Display user message in chat
            with chat_history:
                ui.markdown(f"**User**: {query}").classes('text-left p-2 bg-gray-100 rounded')

            # Call the generate_response function asynchronously
            context, response = await asyncio.to_thread(generate_response, query)

            # Display the response in chat
            with chat_history:
                ui.markdown(f"**Bot**: {response}").classes('text-left p-2 bg-blue-100 rounded')

            user_input.value = ''  # clear input

        # Button to send message
        ui.button('Send', on_click=send_message).classes('w-full')

    # Run the NiceGUI app
    ui.run()

if __name__ in {"__main__", "__mp_main__"}:
    main()