import asyncio
from nicegui import ui
from RAG.query import generate_response

def main():
    # Header with centered title
    ui.label('Chat with My RAG Prototype').classes('text-2xl font-bold m-4 text-center')

    with ui.column().classes('w-full max-w-xl mx-auto'):
        # Chat history container with fixed height and auto scroll enabled
        chat_history = ui.column().classes(
            'gap-2 border rounded p-4 mb-4 overflow-y-auto'
        ).style('height: 400px;')

        # Input with a clearable property for convenience
        user_input = ui.input('Type your message...').classes('w-full').props('clearable')

        # Function to handle sending messages
        async def send_message():
            query = user_input.value
            if not query.strip():
                return

            # Display the user message in chat
            with chat_history:
                ui.markdown(f"**User**: {query}").classes('text-left p-2 bg-gray-100 rounded shadow-sm')

            # Clear the input field
            user_input.value = ''

            # Auto-scroll to the bottom after user message
            ui.run_javascript('''
                const chat = document.getElementById("chat-history");
                chat.scrollTop = chat.scrollHeight;
            ''')

            # Generate bot response asynchronously
            context, response = await asyncio.to_thread(generate_response, query)

            # Display the bot response
            with chat_history:
                ui.markdown(f"**Bot**: {response}").classes('text-left p-2 bg-blue-100 rounded shadow-sm')

            # Auto-scroll to the bottom after bot response
            ui.run_javascript('''
                const chat = document.getElementById("chat-history");
                chat.scrollTop = chat.scrollHeight;
            ''')

        # Send button with improved styling
        ui.button('Send', on_click=send_message).classes('w-full mt-2 bg-blue-500 text-white font-bold hover:bg-blue-600')

    # Run the NiceGUI app
    ui.run()

if __name__ in {"__main__", "__mp_main__"}:
    main()