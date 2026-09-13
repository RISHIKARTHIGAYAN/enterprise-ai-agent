\# Enterprise AI Agent



A local-first enterprise AI agent that intelligently routes user requests to the right AI capability — RAG, SQL, or Calculator — using LangGraph and a locally hosted LLM.



\## Overview



Enterprise AI Agent is an AI-powered system designed to help employees interact with company knowledge and structured business data using natural language.



Instead of sending every question directly to an LLM, the system first understands the request and routes it to the appropriate tool.



\### Main capabilities



\- Agentic AI routing

\- Retrieval-Augmented Generation (RAG)

\- Local LLM using Ollama

\- ChromaDB vector search

\- Employee database querying

\- Safe mathematical calculator

\- Prompt-injection guardrails

\- FastAPI REST API

\- Document upload

\- Request-level logging

\- Automated testing

\- Agent evaluation



\## Architecture



```text

&#x20;                        User

&#x20;                          |

&#x20;                          v

&#x20;                   Security Guardrails

&#x20;                          |

&#x20;                          v

&#x20;                    Agent Router

&#x20;                          |

&#x20;            +-------------+-------------+

&#x20;            |             |             |

&#x20;            v             v             v

&#x20;           RAG           SQL       Calculator

&#x20;            |             |             |

&#x20;            v             v             v

&#x20;        ChromaDB       SQLite       Safe AST

&#x20;            |             |             |

&#x20;            +-------------+-------------+

&#x20;                          |

&#x20;                          v

&#x20;                     Local LLM

&#x20;                       Ollama

&#x20;                          |

&#x20;                          v

&#x20;                   Final Response

