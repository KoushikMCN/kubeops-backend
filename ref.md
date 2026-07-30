backend/
│
├── app/
│   ├── agent/
│   │   ├── graph.py          # LangGraph definition
│   │   ├── state.py          # Graph state
│   │   ├── nodes.py          # LangGraph nodes
│   │   ├── prompts.py
│   │   └── router.py
│   │
│   ├── tools/
│   │   ├── kubernetes.py
│   │   ├── logs.py
│   │   ├── events.py
│   │   ├── deployment.py
│   │   └── health.py
│   │
│   ├── services/
│   │   ├── llm.py
│   │   ├── kubernetes.py
│   │   └── incident.py
│   │
│   ├── api/
│   │   ├── routes.py
│   │   └── websocket.py
│   │
│   ├── models/
│   │   ├── request.py
│   │   └── response.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   └── logging.py
│   │
│   ├── utils/
│   │
│   └── main.py
│
├── tests/
│
├── requirements.txt
│
└── Dockerfile