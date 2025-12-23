import globals

async def trigger_memory_generation(sId):
    """
    Refreshes the session object and adds the session to the memory service.

    Args:
        app_name (str): The name of the app.
        session (Session): The session object to be added to memory.

    Returns:
        None
    """
    try:
        # Refresh your `session` object so that all of the session events locally available.
        session = await globals.session_service.get_session(
            app_name=globals.app_name,
            user_id=globals.user_id,
            session_id=sId
        )
        await globals.memory_service.add_session_to_memory(session)
        print(f"Added session to memory: {session}")

    except Exception as e:
        print(f"Memory Manager Error in trigger_memory_generation: {e}")