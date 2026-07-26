---
title: Model Context Protocol for Engineering Toolchains, Matthew Collaro
h1: Model Context Protocol for engineering toolchains
description: Why exposing MBSE context through typed, governed operations beats dumping exported documents into a context window, and what the interface design has to get right.
type: article
date: 2026-05-03
---

The naive way to connect an AI assistant to an engineering program is to export everything and paste it in. Requirements to CSV, model to XMI, specifications to text, into the context window. This works well enough in a demo to be misleading.

It fails on real programs for reasons that have nothing to do with context length.

## Why the export approach fails

**Exports are stale the moment they are made.** An engineering model changes daily. An export is a photograph. Any answer derived from it is an answer about the system as of Tuesday, delivered with no indication that it is not about the system as of today. On a program where the whole point is keeping artifacts synchronized, introducing a new source of drift is a strange thing to do deliberately.

**Exports lose structure.** XMI flattened into text preserves the words and destroys the graph. The relationship between a requirement and the component satisfying it becomes textual adjacency rather than a traversable edge. So the model reconstructs relationships by inference, which is exactly the operation you wanted to avoid, since the relationships were already recorded precisely.

**Access control disappears.** Engineering models contain export-controlled content, supplier-proprietary content, and program-sensitive content. A flat export has no notion of who is asking. Anyone who has worked under ITAR or on a classified program will recognize why this is not a minor implementation detail.

**Provenance disappears.** When the assistant asserts something, you want to know which model elements it came from. Text in a context window has no addresses. You get an assertion and a vibe.

## What a protocol interface changes

Model Context Protocol gives you a way to expose capabilities as typed operations rather than as a blob. For engineering context, the useful shape is a small set of well-defined queries against the live model:

- Retrieve a requirement by identifier, with its current text, status, and attributes.
- Traverse traceability relationships from an element in a given direction, to a given depth.
- Query the interface definition for a port or signal, with types and units.
- Check constraint satisfaction for a scoped subset of the model.
- Search semantically over the graph and return element references, not prose.
- Report verification coverage for a set of requirements.

Each has a schema. Each returns element references. Each executes against current state.

The difference this makes is not incremental. When an assistant answers "which requirements are affected by changing this interface" by traversing the actual graph, the answer is derived rather than guessed, and every item in it can be clicked. When it answers from a flattened export, the answer is a plausible list.

## Design decisions that matter

**Return references, not just content.** Every result should carry the identifier of the element it came from. This is what makes downstream validation possible: given an assertion and its claimed sources, you can check whether the sources say that. Without references you are trusting a summary.

**Make operations narrow.** A tool called `query_model` that accepts arbitrary graph queries is convenient and hard to govern. Narrow operations, `get_requirement`, `trace_downstream`, `get_interface`, are easier to reason about, easier to authorize, easier to audit, and easier for a model to use correctly. Breadth in the interface pushes complexity onto the caller, which is the wrong direction when the caller is a language model.

**Enforce scope at the interface.** Authorization belongs in the operation, not in a prompt instruction. "Do not reveal export-controlled content" as a system prompt is not a control. A retrieval path that cannot return content the requester is not cleared for is a control. Treat the assistant as an untrusted caller, because it is one.

**Separate reads from writes, and gate writes hard.** Reading model context is low-risk. Writing to an authoritative engineering model is a configuration change. If you expose write operations at all, they should produce proposals that enter the normal change process, not direct mutations. The temptation to let the agent just fix it is strong and should be resisted until the review path exists.

**Version everything.** Every response should indicate the model version it reflects. This lets you detect when an analysis was performed against a state that has since changed, and it makes the whole interaction reproducible, which matters enormously if any of this feeds a certification artifact.

## Where this sits relative to the tools

A frequent misunderstanding is that this replaces Cameo, or DOORS, or JAMA. It does not, and a platform that tries to will lose. Those tools hold the authoritative content and the workflows engineers already know.

What the protocol layer adds is a governed read path over the top of them: one that speaks a consistent vocabulary across tools that otherwise share nothing, so that a question about a requirement in DOORS, a block in Cameo, and a test case in a third system can be answered as one question. The integration burden lives in the adapters, which is the right place for it.

The tool ecosystem stays intact. The intelligence layer sits above it and is not authoritative for anything.

## The honest limitation

None of this makes the assistant correct. It makes the assistant's claims checkable, which is a different and more achievable goal.

A grounded assistant with a well-designed protocol interface will still produce wrong answers. It will traverse correctly and characterize incorrectly. The value is that when it does, you can see which elements it read, and the assertion can be validated against them mechanically rather than by a reviewer's impression.

That is the property worth engineering for. Not correctness, auditability. Correctness is what you get from auditability plus iteration.

---

Related: [Guardrails for AI-generated engineering artifacts](guardrails-for-ai-generated-engineering-artifacts.html).
