# AI Prompt Ledger

## Bug 1 – Buffer Leak (Mutable Default Argument)

### Prompt
Can you explain what's wrong with this constructor? I know using `[]` as a default argument is not recommendable, but I don't understand why for this application.

### AI Suggestion
The AI explained that using a mutable object such as a list as a default argument causes every `TelemetryBuffer` object to share the same list. It recommended replacing the default value with `None` and creating a new list inside the constructor.

### Engineering Justification
I changed the default argument from `[]` to `None` and initialized a new list inside the constructor. This ensures that each `TelemetryBuffer` object has its own frame buffer instead of sharing one list with other objects.

---

## Bug 2 – Polymorphic Trap (LSP Violation)

### Prompt
I modified the `IMUPeripheral.poll_raw_voltage()` method so that it always returns a float instead of sometimes returning a dictionary. Can you review my implementation and determine whether it now satisfies the Liskov Substitution Principle? If there are any remaining design issues, explain them and justify your recommendations.

### AI Suggestion
The AI confirmed that always returning a float resolves the Liskov Substitution Principle violation. It also suggested storing fault information separately instead of returning it as a dictionary.

### Engineering Justification
Although storing fault information separately is a better design for larger systems, the exam only required the method to always return a float. I chose the simpler solution because it satisfies the class contract while keeping the changes minimal.

---

## Bug 3 – Race Condition (Concurrency Flaw)

### Prompt
I modified the `AvionicsBusMaster` class by adding a `threading.Lock` to protect updates to the shared bus register and `total_cycles_executed`. Can you review my implementation and determine whether it correctly resolves the race condition while preserving concurrency? If there are any remaining synchronization or design issues, explain them and justify your recommendations.

### AI Suggestion
The AI confirmed that the race condition was resolved and concurrency was preserved. It recommended keeping the lock only around the shared register updates and removing unnecessary shared-state access outside the critical section.

### Engineering Justification
I followed the AI's recommendation by limiting the lock to the shared register and counter updates. This protects the shared data from race conditions while still allowing the sensor polling and signal processing to run concurrently.