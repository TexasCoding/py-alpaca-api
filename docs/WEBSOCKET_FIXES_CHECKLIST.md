# WebSocket Streaming - Immediate Fixes Checklist

## 🚀 Quick Fixes for v3.1.0-alpha.2

This checklist tracks the immediate fixes needed before merging PR #77 or as a fast-follow update.

### 🔴 Critical Fixes (Must Do)

#### Thread Safety
- [ ] Add `threading.RLock` for connection state
  ```python
  self._state_lock = threading.RLock()
  self._is_connected = False
  ```
- [ ] Protect subscription modifications with locks
- [ ] Add locks for handler list access
- [ ] Test with concurrent operations

#### Exception Handling
- [ ] Replace `logger.error` with `logger.exception` in:
  - [ ] Line 119: `_run_forever`
  - [ ] Line 189: `_on_message` (JSONDecodeError)
  - [ ] Line 191: `_on_message` (General Exception)
  - [ ] Line 229: `_handle_reconnect`
  - [ ] Line 269: `_dispatch_message`

#### Message Handling
- [ ] Add validation for empty/null messages
- [ ] Handle partial JSON messages
- [ ] Add try-catch for corrupted data
- [ ] Log and continue on bad messages (don't crash)

### 🟡 Important Fixes (Should Do)

#### Connection Management
- [ ] Make connection state checks atomic
- [ ] Add connection state enum
- [ ] Prevent multiple simultaneous connections
- [ ] Clean up resources on disconnect

#### Method Signatures
- [ ] Fix unused `ws` parameter warnings:
  ```python
  def _on_message(self, _ws: websocket.WebSocketApp, message: str) -> None:
      # Use underscore prefix for unused params
  ```
  Or add `# noqa: ARG002` comments

#### Memory Management
- [ ] Add method to remove individual handlers
- [ ] Clear handlers on disconnect
- [ ] Add maximum handler limit
- [ ] Consider weak references for handlers

### 🟢 Nice to Have (Can Do Later)

#### Monitoring
- [ ] Add connection metrics
- [ ] Add message counters
- [ ] Add performance logging
- [ ] Create health check method

#### Testing
- [ ] Add test for partial messages
- [ ] Add test for concurrent subscriptions
- [ ] Add test for memory leaks
- [ ] Add test for reconnection during auth

## 📝 Implementation Examples

### Fix 1: Thread Safety
```python
class StreamClient:
    def __init__(self, ...):
        # Add locks
        self._state_lock = threading.RLock()
        self._handler_lock = threading.RLock()

    @property
    def is_connected(self) -> bool:
        with self._state_lock:
            return self._is_connected

    @is_connected.setter
    def is_connected(self, value: bool) -> None:
        with self._state_lock:
            self._is_connected = value
```

### Fix 2: Exception Handling
```python
# Change all exception handlers
try:
    # code
except json.JSONDecodeError as e:
    logger.exception("Failed to parse message")  # Not logger.error
    # Handle gracefully, don't crash
except Exception as e:
    logger.exception("Unexpected error")  # Preserves stack trace
```

### Fix 3: Message Validation
```python
def _on_message(self, _ws, message: str) -> None:
    """Handle incoming WebSocket messages."""
    if not message:
        logger.debug("Received empty message")
        return

    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        logger.exception(f"Invalid JSON received: {message[:100]}...")
        return  # Don't crash, just skip

    # Ensure it's a list
    if not isinstance(data, list):
        data = [data]

    # Process each message...
```

### Fix 4: Handler Removal
```python
def remove_handler(self, stream_type: StreamType, handler: Callable) -> bool:
    """Remove a specific handler.

    Returns:
        True if handler was removed, False if not found
    """
    with self._handler_lock:
        if handler in self.handlers[stream_type]:
            self.handlers[stream_type].remove(handler)
            return True
    return False

def clear_all_handlers(self) -> None:
    """Remove all handlers."""
    with self._handler_lock:
        for stream_type in StreamType:
            self.handlers[stream_type].clear()
```

## 🧪 Test Cases to Add

### Thread Safety Tests
```python
def test_concurrent_subscriptions():
    """Test multiple threads subscribing simultaneously."""
    client = StreamClient(...)
    threads = []

    def subscribe_worker(symbol):
        client.subscribe_quotes(symbol, lambda x: None)

    # Create 50 threads
    for i in range(50):
        t = threading.Thread(target=subscribe_worker, args=[f"TEST{i}"])
        threads.append(t)
        t.start()

    # Wait for all
    for t in threads:
        t.join()

    # Should have 50 subscriptions, no errors
    assert len(client.subscriptions[StreamType.QUOTES]) == 50
```

### Error Handling Tests
```python
def test_corrupted_message_handling():
    """Test that corrupted messages don't crash the client."""
    client = StreamClient(...)

    # Send various bad messages
    bad_messages = [
        "",  # Empty
        "not json",  # Invalid JSON
        '{"partial": ',  # Incomplete JSON
        '[]',  # Empty array
        'null',  # Null
    ]

    for msg in bad_messages:
        # Should not raise exception
        client._on_message(None, msg)

    # Client should still be functional
    assert client is not None
```

## 📅 Timeline

### Immediate (Before Merge)
- Thread safety for state management
- Fix exception handling (logger.exception)
- Basic message validation

### Fast Follow (v3.1.0-alpha.2)
- Complete thread safety
- Handler removal methods
- Connection state machine

### Future (v3.1.0-stable)
- Full metrics implementation
- Advanced error recovery
- Performance optimizations

## ✅ Verification

### Before Marking Complete
1. Run existing tests: `pytest tests/test_streaming/`
2. Check for race conditions: Run concurrent test
3. Verify logging: Check stack traces are preserved
4. Memory check: Monitor for leaks
5. Code review: Get second opinion

## 📊 Progress Tracking

| Category | Total | Fixed | Remaining |
|----------|-------|-------|-----------|
| Critical | 12 | 0 | 12 |
| Important | 9 | 0 | 9 |
| Nice to Have | 8 | 0 | 8 |
| **Total** | **29** | **0** | **29** |

---

**Last Updated**: 2024-01-17
**Target Completion**: v3.1.0-alpha.2
**Owner**: Development Team
