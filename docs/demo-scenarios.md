# Demo Scenarios and Test Prompts

## Scenario 1: Refund Request (Standard)
Prompt:
"I was charged yesterday and need a refund because I canceled the service."

Expected behavior:
- Intent: refund
- Sentiment: neutral/negative
- Retrieval: refund policy snippet
- Escalation: optional (not mandatory)

## Scenario 2: Password Reset (Self-Service)
Prompt:
"I cannot login. How do I reset my password?"

Expected behavior:
- Intent: account
- Sentiment: neutral
- Retrieval: password reset steps
- Escalation: no

## Scenario 3: Angry Customer, Manager Request (Escalation)
Prompt:
"This is the worst support ever. I want a manager immediately."

Expected behavior:
- Sentiment: very_negative
- Escalation: yes
- Ticket creation: yes with high priority

## Scenario 4: Billing Dispute with Urgency
Prompt:
"You charged me twice and I need this fixed now."

Expected behavior:
- Intent: billing
- Urgency: high
- Retrieval: billing errors policy
- Escalation: likely yes

## Scenario 5: Delivery Delay
Prompt:
"My order still has not arrived after 12 days."

Expected behavior:
- Intent: delivery
- Retrieval: delivery delay policy
- Escalation: optional
