---
title: Model Governance for SysML Programs That Have to Certify — Matthew Collaro
h1: Model governance for SysML programs that have to certify
description: When the model is the certification artifact rather than a picture of one, governance stops being bureaucracy and becomes the thing that makes the model trustworthy.
type: article
date: 2026-06-28
---

There is a moment on every MBSE program where someone asks whether the model is authoritative. The answer determines everything that follows, and most programs answer it by accident.

If the model is authoritative, it is a controlled artifact and changes to it are engineering changes. If it is not, it is documentation, and documentation drifts. There is no stable middle position, though many programs try to occupy one — the model is authoritative in the sense that everyone agrees it should be, and non-authoritative in the sense that nobody gates anything on it.

## What governance actually means here

Model governance gets a bad reputation because it is usually introduced as process: naming conventions, review checklists, a style guide nobody reads. That is not governance. That is formatting.

Governance is the set of answers to four questions:

1. **Who is allowed to change what?** Not "who has write access," which is usually everybody. Which engineer owns which part of the model such that a change without their involvement is a defect.
2. **What must be true before a change lands?** The conditions a model change has to satisfy to be accepted — well-formedness, traceability preservation, constraint satisfaction, whatever the program requires.
3. **How is a change recorded?** Enough that in three years someone can reconstruct why a block was decomposed the way it was.
4. **What happens when a rule is violated?** If the answer is "nothing," the rule does not exist.

Every program I have worked on could answer the first question informally and the fourth not at all.

## Ownership boundaries have to match the architecture

The most common governance failure is drawing ownership boundaries around organizations instead of around interfaces.

If the model is partitioned by team — cabin systems owns this package, network systems owns that one — then every interface between them sits on a boundary with two owners or none. In practice it is none. Interfaces are where integration problems live, and putting them in ownership no-man's-land is how you get a model that looks complete and integrates badly.

Partitioning by interface is harder to set up and much better. Every interface gets a single owning engineer, who is responsible for its definition being precise enough that both sides can implement against it independently. Whether that engineer sits in the cabin org or the network org matters less than whether they exist.

At Boeing, doing this across large integrated product teams was the difference between revisions that converged and revisions that ping-ponged.

## Validation has to be automated or it does not happen

Manual model review does not scale, and more importantly it does not catch the things automation catches. A reviewer looking at a decomposition will notice that it seems wrong. They will not notice that a port on a nested block has no matching connector three levels up, because nobody holds a model that large in their head.

The rules worth automating are the boring ones:

- Every requirement has at least one satisfying element, and that element exists.
- Every interface has both ends defined and typed compatibly.
- Every port is connected, or explicitly marked as intentionally unconnected with a rationale.
- No element references a deleted element.
- Naming and identifier rules hold, so that downstream tooling can rely on them.
- Verification methods are assigned for every requirement in scope.

None of these require judgment. All of them are violated regularly on large models. Running them on every change turns a class of defect that used to be found at review into a class of defect that cannot be committed.

The rules requiring judgment — is this the right decomposition, is this requirement well-formed as a requirement — still need humans. Automating the mechanical checks is what frees reviewers to spend attention on the judgment ones instead of hunting for dangling ports.

## Certification changes the stakes, not the method

When the model feeds certification artifacts, two additional properties matter.

**Reproducibility.** You must be able to regenerate the artifact from a specified model state and get the same result. This means model versions have to be identifiable and retrievable, and generation has to be deterministic. If your hazard analysis is produced by a tool that samples the model at whatever state it happened to be in, you cannot defend it.

**Provenance.** For any statement in a certification artifact, you need to identify the model elements it was derived from. Not approximately — specifically. When a regulator asks why a particular failure condition was classified the way it was, "the tool generated it" is not an answer.

Both are engineering properties of the pipeline, not process documents. If you build model-based safety and hazard assessment tooling — which I did at Boeing — these are the requirements that constrain the design most, and they are much cheaper to build in than to retrofit.

## The part that decides whether it works

Governance succeeds when violating it is harder than complying with it, and fails otherwise.

If the traceability check runs in CI and blocks the merge, engineers maintain traceability. If it runs as a monthly report that goes to a manager, they do not, and no amount of emphasis in the kickoff deck changes that. This is not a statement about engineers. It is a statement about where friction sits relative to incentive.

The corollary is that every governance rule you cannot enforce automatically is a rule you should think hard about keeping. An unenforced rule is worse than no rule, because it creates the impression of control while providing none, and it trains people to treat the rule set as advisory.

Write down fewer rules. Enforce the ones you write.

---

Related: [Why requirements traceability breaks](requirements-traceability-breaks.html) and [Guardrails for AI-generated engineering artifacts](guardrails-for-ai-generated-engineering-artifacts.html).
