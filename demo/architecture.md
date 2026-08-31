# Architecture

Incoming request (support ticket or vendor query)
        |
        v
Decision agent — classifies: simple or complex
        |
        v
Tool execution — KB search or vendor negotiation
        |
        v
Evaluate outcome — is the resolution acceptable?
        |
   +----+----+
   |         |
   v         v
Auto-resolved   Escalate to human (with reasoning)
```

Same loop for both domains: **Observe → Decide → Act → Evaluate → Adapt.**
Only the tool called in the "Act" step differs based on `request_type`.

(Paste the rendered diagram image here for the final submission.)
