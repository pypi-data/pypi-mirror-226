# aioqueueext

A package that provides asyncio Queues with additional functionality.

## Work-in-Progress

The repository contains modules extracted from my other project and was refactored as a separate package.

In the current version, I have not verified all of the functions.

Additional functions I plan to implement are:
- `return_when_*()` - async functions to ease synchronization tasks
- `set_on_get_callback()`
- `set_on_put_callback()`
- `peek_nowait()` - returns the "up-next" item without removing it from the queue
- `peek_and_get()` - async peek and conditionally get (pop) an item from the queue

## Examples

### Sync Peeking

```
async def sync_peeking_example() -> None:
    queue1 = QueueExt()

    await queue1.put("apple")

    item = queue1.peek_nowait()
    print(f"first peek: {item}")  # "apple"

    await queue1.put("banana")

    item = queue1.peek_nowait()
    print(f"second peek: {item}")  # "apple"

    item = await queue1.get()  # popped "apple"

    item = queue1.peek_nowait()
    print(f"third peek: {item}")  # "banana"

    item = await queue1.get()  # popped "banana"

    # the next peek raises the QueueEmpty exception
    try:
        print(f"fourth peek: {queue1.peek_nowait()}")
    except asyncio.QueueEmpty:
        print("fourth peek failed: QueueEmpty")

```