from tqdm import tqdm
import concurrent.futures
import itertools


def parallel_lookup(items, func):
    values = iter(i for i in items)
    progress = tqdm(total=len(items), desc="Searching...")

    rv = []

    with concurrent.futures.ProcessPoolExecutor(32) as executor:
        futures = {executor.submit(func, val) for val in itertools.islice(values, 512)}

        while futures:
            done, futures = concurrent.futures.wait(
                futures, return_when=concurrent.futures.FIRST_COMPLETED
            )

            for fut in done:
                try:
                    if returned_value := fut.result():
                        rv.append(returned_value)
                except UnicodeDecodeError as e:
                    pass
                progress.update()

            for task in itertools.islice(values, len(done)):
                futures.add(executor.submit(func, task))

    return rv