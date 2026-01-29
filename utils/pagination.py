def paginate_all(fetch_page_func, start_page=1, **kwargs):
    """
    Generic helper to fetch all pages from an ATS API.
    
    :param fetch_page_func: Function that takes (page, **kwargs) and returns a list of items.
    :param start_page: The first page index.
    :param kwargs: Additional arguments for fetch_page_func.
    :return: A combined list of all items.
    """
    all_items = []
    current_page = start_page
    
    while True:
        items = fetch_page_func(page=current_page, **kwargs)
        if not items:
            break
        
        all_items.extend(items)
        current_page += 1
        
        # Safety break for mock/infinite loops
        if current_page > 100:
            break
            
    return all_items

def paginate_with_cursor(fetch_func, **kwargs):
    """
    Generic helper to fetch all records using cursor-based pagination.
    
    :param fetch_func: Function that returns (items, next_cursor).
    :param kwargs: Initial arguments.
    :return: Combined list of all items.
    """
    all_items = []
    next_cursor = None
    
    while True:
        items, cursor = fetch_func(cursor=next_cursor, **kwargs)
        all_items.extend(items)
        
        if not cursor:
            break
        
        next_cursor = cursor
        
    return all_items
