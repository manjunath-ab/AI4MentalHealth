from concurrent.futures import ThreadPoolExecutor

def get_max_workers():
    with ThreadPoolExecutor() as executor:
        max_workers = executor._max_workers
    return max_workers

max_workers = get_max_workers()
print(f"Maximum number of workers: {max_workers}")
