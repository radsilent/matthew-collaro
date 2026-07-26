---
title: Interface Control Documents Should Be Models — Matthew Collaro
h1: Interface control documents should be models
description: The ICD is where integration problems are born. Treating it as a document instead of a model is why interfaces that pass review still fail on the bench.
type: article
date: 2026-06-09
---

An interface control document is a contract between two teams who will not talk to each other again for six months. It should be treated with the seriousness of a contract. Usually it is treated with the seriousness of a Word file.

I have spent a lot of my career on interfaces — modeling embedded system interfaces at a missile defense prime, building model-based Interface Control Diagrams at Boeing, and more recently untangling signal ownership within vehicle infotainment controllers. The pattern is consistent enough that I think it is structural.

## What goes wrong with the document form

**Prose admits ambiguity that implementation cannot.** "The controller shall report status periodically." Two teams read this. One implements a 100 ms periodic message. The other implements on-change reporting with a 1 s heartbeat and considers it periodic. Both are defensible readings. Both pass document review, because the reviewer also read it as whichever one they had in mind.

You find out on the bench. If you are lucky, you find out on the bench.

**Documents cannot be checked.** There is no operation you can run on a Word file that tells you whether the signal list in section 4.2 is consistent with the state machine in section 6.1. So nobody checks, and by revision C they are not consistent, and the inconsistency is discovered by an integration engineer at 11 pm.

**Both sides get their own copy.** The moment an ICD is a file, it is a file that gets emailed, forked, and locally annotated. Two teams end up working from documents with the same title and different content. This is so common that on some programs it is the default assumption, and integration begins with a diff.

**Revision granularity is wrong.** A document revises as a whole. So a change to one signal produces a new revision of the entire ICD, and every consumer must re-review a hundred pages to find the one thing that moved. In practice they do not re-review. They skim, miss it, and integrate against a stale understanding.

## What the model form gives you

When the interface is a model element rather than a section of prose, several things become possible that were not.

**Types are checked.** A signal has a type, a range, units, and an encoding. If one side declares a value in meters per second and the other consumes it as kilometers per hour, that is not a discussion at integration. It is a validation failure at commit. Unit mismatches are among the most expensive and most preventable integration defects in the industry, and they are trivially catchable if units are modeled rather than mentioned.

**Completeness is computable.** Every port either connects to something or is explicitly marked as unconnected with rationale. Every signal has a producer and at least one consumer. A model can enforce this. A document can only assert it.

**Change impact is derivable.** Change a signal definition and the model tells you which components consume it, which requirements reference it, and which test cases exercise it. This is the single most valuable property, and it is the one documents fundamentally cannot provide. Not because document tooling is immature — because the relationships are not represented anywhere a tool can read.

**There is one instance.** Both sides reference the same element. There is no your-copy and my-copy. Disagreements about what the interface is become impossible to sustain, which sounds trivial and eliminates an entire genre of integration meeting.

**Views can be generated per consumer.** The software team wants message formats. The safety team wants failure propagation paths. The test team wants observability points. From one model you generate three views that cannot contradict each other, because they are projections of the same underlying thing. From one document you get one document that serves nobody especially well.

## Interfaces as a security surface

At the missile defense prime I modeled embedded system interfaces partly for integration and partly for cybersecurity. At Boeing, model-based ICDs fed directly into networked system vulnerability identification during threat analysis.

The connection is not obvious until you have done it, and then it is hard to unsee: **an interface you cannot specify precisely is an interface nobody fully owns, and interfaces nobody fully owns are where the exposure is.** Formal modeling does not find vulnerabilities by being clever. It finds them by refusing to accept vagueness, and vagueness is where the exposure hides.

Ask what data crosses a boundary, in what direction, under what authority, and with what validation on receipt. Model that honestly and the gaps announce themselves. Write it as prose and the gaps read as reasonable-sounding paragraphs.

## Objections worth taking seriously

**"Our suppliers need a document."** Fine — generate one. A PDF produced from the model, with a version and a hash tying it to the model state it came from, is a document. The distinction that matters is whether the document is the source or a rendering. Rendered documents are fine. Authored documents drift.

**"The tooling is heavy."** Sometimes. But the comparison is not against zero cost; it is against the cost of the integration defects the document form produces, which is real and simply appears in a different budget line, usually later and attributed to someone else.

**"We do not have modeling skills across all the teams."** This is the honest objection and the one I would address first. It also does not require every engineer to be a modeler. It requires the interface owner to be one, and everyone else to consume generated views. That is a much smaller training problem than it initially appears, and it is the shape most successful adoptions actually take.

---

Related: [Why requirements traceability breaks](requirements-traceability-breaks.html) and [Modeling automotive HMI and infotainment integration](automotive-hmi-infotainment-modeling.html).
