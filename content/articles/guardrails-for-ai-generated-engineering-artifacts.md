---
title: Guardrails for AI-Generated Engineering Artifacts — Matthew Collaro
h1: Guardrails for AI-generated engineering artifacts
description: Reviewing generated requirements and models by reading them does not scale and does not work. The check has to be structural, and the generator must not be able to route around it.
type: article
date: 2026-05-22
---

The pitch for language models in systems engineering is that they will write your requirements. The problem with the pitch is that writing requirements was never the expensive part. Being wrong about them is the expensive part, and generation makes being wrong cheaper to produce and no cheaper to detect.

I have spent most of my career in places where an artifact does not ship because it looks right. Aircraft networks, missile subsystems, vehicle platforms. The posture that environment teaches transfers directly to generated output, and it is not the posture the industry has adopted by default.

## Review does not scale, and it does not work

The default control on generated artifacts is human review. An engineer reads the generated requirement and approves it. This fails in two ways.

It does not scale, obviously: generation is fast and reading is not, so review becomes the bottleneck and then becomes perfunctory. A reviewer facing 400 generated requirements does not review 400 requirements. They spot-check twelve and approve the batch, and everyone involved knows this.

Less obviously, **review is bad at catching the specific errors generation produces.** Human reviewers are tuned to catch things that read wrong. Generated text reads well by construction — that is the one thing the technology is unambiguously good at. A requirement that is fluent, correctly formatted, uses the right vocabulary, and is subtly inconsistent with the interface it constrains will pass review by a tired engineer essentially every time.

The errors are not stylistic. They are referential: plausible statements about a system that do not correspond to the system. Reading is the wrong instrument for detecting that.

## The check has to be structural

The alternative is to check generated artifacts against the model rather than against a reader's judgment.

A generated requirement that references a signal must reference a signal that exists, with the type it claims. A generated requirement allocated to a component must be allocated to a component that exists and is in the right decomposition branch. A generated verification method must be one of the permitted methods for that requirement class. A generated hazard must reference failure modes present in the model.

None of this is judgment. All of it is checkable, mechanically, in milliseconds. And each of these is a real failure mode I have seen from generated content — confident references to signals that do not exist, allocations to components in the wrong subsystem, invented failure modes.

The rule I keep coming back to: **the generator must not be able to route around the check.** If the same system that produced the artifact also decides whether it is valid, you have no control. The validator must operate on the model with rules the generator does not author and cannot modify. This is the whole ballgame, and it is where most implementations go wrong — they ask the model to critique its own output and call that verification.

## Grounding beats prompting

The other structural move is to stop asking a model to produce statements about a system it only knows through a prompt.

This is the reasoning behind exposing engineering context through the Model Context Protocol rather than pasting exported documents into a context window. When a model can query the actual requirement, traverse the actual traceability relationships, and read the actual interface definition, its output is anchored to retrievable objects. Anchored claims can be checked against their anchors. Unanchored claims can only be believed or not.

It also changes the failure mode in a useful direction. An ungrounded model that does not know something produces something plausible. A grounded model that queries and finds nothing can report that it found nothing. The second is a much better failure to have, and it is available only if you build the retrieval path.

## What generation is genuinely good for

I am not arguing against using these tools. I am building a platform that uses them. But the value is in specific places.

**Normalization.** Taking requirements written by forty people over eight years in inconsistent phrasing and rendering them in a consistent pattern. The semantic content is already there and human-authored; the model is reformatting. Errors are visible and low-stakes.

**First-pass extraction.** Reading a 200-page supplier specification and proposing which paragraphs contain requirements. It will miss some and over-flag others, but it turns a week of reading into a day of triage, and a human decides every inclusion.

**Coverage interrogation.** Asking what is not covered — which functions have no requirements, which requirements have no verification, which interfaces are referenced but undefined. This plays to the technology's strength, which is breadth, and the output is a list of questions rather than a set of assertions.

**Draft rationale.** Proposing why a trace link might exist for an engineer to confirm or reject. Cheap to produce, cheap to check, and it attacks the real problem that rationale never gets written down.

Notice what these have in common. In each, the output is either checkable against something concrete, or it is a proposal a human accepts. None of them place a generated assertion into an authoritative artifact without a structural check.

## The uncomfortable part

If you cannot check it, do not generate it.

This is a stronger constraint than it sounds, and it rules out several things people want to do. If your model is not formal enough to validate a generated requirement against, the answer is not to generate anyway and review harder. The answer is that your model is not ready to be a generation target.

That is a less exciting conclusion than the demos suggest. It is also the difference between tooling that survives contact with a certification program and tooling that produces an impressive pilot and quietly disappears.

---

Related: [Model Context Protocol for engineering toolchains](model-context-protocol-engineering-toolchains.html) and [Model governance for SysML programs](sysml-model-governance.html).
