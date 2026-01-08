import globals

async def trigger_memory_generation(sId, user_id):
    """
    Refreshes the session object and adds the session to the vertex ai memory bank service.

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
            user_id=user_id,
            session_id=sId
        )
        await globals.memory_service.add_session_to_memory(session)
        print(f"Added session to memory: {session}")
        print(f"Added session to vertex ai memory bank for sId : {session.id}")

    except Exception as e:
        print(f"Memory Manager Error in trigger_memory_generation: {e}")

async def trigger_search_memory(user_id, query):
    """
    Searches the memory bank for relevant information.

    Args:
        query (str): The search query.

    Returns:
        list: A list of relevant memory entries.
    """
    try:
        results = await globals.memory_service.search_memory(
            app_name=globals.app_name,
            user_id=user_id,
            query=query
        )
        print(f"Memory search results for query '{query}': {results}")
        return results
    except Exception as e:
        print(f"Memory Manager Error in search_memory: {e}")
        return []