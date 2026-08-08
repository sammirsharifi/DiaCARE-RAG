# DiaCARE-RAG

### Diabetes Causality-Aware Retrieval-Augmented Generation

**DiaCARE-RAG** is a research project focused on improving the capabilities, reliability, and explainability of Language Models in the medical domain through the use of **external structured knowledge**.

The core idea behind the project is that a Language Model should not have to rely exclusively on the knowledge stored within its parameters when answering sensitive medical questions. Instead, external sources of knowledge—particularly **medical knowledge graphs and ontologies**—can be used to provide the model with relevant, structured, and verifiable evidence at the time of answering.

This approach aims to make medical question answering more **knowledge-grounded, reliable, and explainable**, while allowing the model to support its responses using evidence retrieved from an external medical knowledge source.

DiaCARE-RAG initially focuses on the **diabetes domain**, where medical knowledge contains complex relationships between diseases, symptoms, risk factors, complications, treatments, and other clinical concepts.

---

## External Knowledge and Evidence

A central concept of DiaCARE-RAG is the use of a medical knowledge source as an external source of evidence.

Instead of asking a Language Model to answer a medical question solely from what it has learned during training, relevant knowledge can be retrieved from a medical knowledge graph or ontology and used during response generation.

This allows the system to associate an answer with the underlying evidence that supports it.

For example, rather than simply generating an answer about a relationship between two medical concepts, the system can retrieve the corresponding relationship from the knowledge graph and use it as evidence for the generated response.

This creates a more transparent relationship between:

**Question → External Knowledge → Evidence → Answer**

---

## Causality-Aware Medical Question Answering

Medical questions are not always simple fact-retrieval questions.

Many questions are inherently causal, such as:

- What causes a particular condition?
- What can diabetes lead to?
- Why does a complication occur?
- Which factors increase the risk of a disease?
- What is the causal relationship between two medical concepts?

DiaCARE-RAG therefore aims to incorporate **causal knowledge** into the retrieval and question-answering process.

By representing and retrieving causal relationships from the external knowledge source, later versions of the project will investigate how explicit causal knowledge can help Language Models better answer **causal medical questions**.

The objective is not only to retrieve concepts that are related to a question, but also to preserve the meaningful relationships between those concepts.

---

# Project Versions

DiaCARE-RAG is being developed incrementally through multiple versions.

Each version represents a step toward a more capable **knowledge-grounded and causality-aware medical RAG system**.

### Version 1 — Initial GraphRAG

The first version provides the initial implementation of the GraphRAG approach using a **manually developed graph-retrieval implementation**.

The purpose of this version is to establish the fundamental concept of using a medical knowledge graph as an external knowledge source for Language Models and to provide the foundation for subsequent versions.

---

### Version 2 — Improved GraphRAG

The second version will build upon the first implementation.

In this version, the project will adopt and integrate components from **Microsoft's GraphRAG** approach while adapting them to the requirements of a structured medical knowledge graph / ontology.

This version will also include improvements to the implementation developed in Version 1.

The goal is to obtain a more mature and robust GraphRAG implementation while preserving the project's core objective of grounding medical Language Model responses in external structured knowledge.

---

### Version 3 — Causality-Aware GraphRAG

The third version will introduce **causal reasoning and causality-aware retrieval** as a core component of DiaCARE-RAG.

The knowledge graph will be used not only to retrieve medically relevant concepts and relationships, but also to identify and preserve **causal relationships and causal paths** relevant to a question.

This version will specifically investigate whether incorporating causal knowledge can improve the ability of Language Models to answer questions involving:

- Causes and effects
- Risk factors
- Disease progression
- Medical complications
- Causal relationships between conditions
- Multi-step causal chains

The long-term objective is to move from a conventional knowledge-grounded GraphRAG system toward a **Causality-Aware Medical GraphRAG** framework.

---
