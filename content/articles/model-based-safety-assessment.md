---
title: Deriving Safety Assessments From the Model Instead of Maintaining Them Beside It — Matthew Collaro
h1: Deriving safety assessments from the model instead of maintaining them beside it
description: Hazard analyses go stale because they are maintained in parallel with the architecture. Generating them from the model changes which errors are possible.
type: article
date: 2026-04-16
---

A functional hazard assessment is a document that describes a system. The system changes. The document does not change at the same rate. Everything downstream of that gap is a category of defect that engineering organizations spend enormous effort catching late.

At Boeing I built model-based safety and hazard assessment tooling integrated into engineering workflows for certification-oriented analysis. The motivation was not efficiency, though it helped. It was that a parallel-maintained safety artifact is wrong by default and correct only by coincidence, and no amount of process rigor fixes a structural problem.

## The staleness mechanism

Safety analysis is performed against an architecture. Failure modes are enumerated for components that exist, propagation paths are traced through connections that exist, mitigations are credited to redundancy that exists.

Then the architecture changes, because architectures change. A component is decomposed. A connection is rerouted. A redundant path is consolidated for weight or cost.

Nothing in the safety artifact knows this happened. The FHA still lists the old failure modes. The fault tree still credits the mitigation that was removed. The analysis is now describing a system that does not exist, and it will continue to look like a complete, professionally-produced analysis, because it is one — of a different aircraft.

Programs handle this with process: change boards, impact assessments, periodic re-review. This works to the extent that people correctly identify which architecture changes have safety significance, which is a judgment call made under schedule pressure by people who are not always the safety engineers. The failures are not random. They cluster exactly where you would expect — changes that seemed obviously benign.

## What derivation changes

If the safety artifact is generated from the model, the failure mode changes from silent staleness to loud regeneration.

Change the architecture, regenerate the analysis, and the diff tells you what moved. A removed redundant path shows up as a mitigation that no longer has support. A new component shows up as failure modes with no assessment. You are no longer relying on someone noticing.

To make this work the model has to carry information that architecture models often do not:

- **Failure modes as model elements**, attached to components, with their own identity — not free text in a description field.
- **Propagation semantics on connections**: what a connection carries and how a failure at one end manifests at the other.
- **Mitigations as explicit relationships**, so that crediting redundancy is a modeled claim rather than an assertion in prose.
- **Severity classification and its rationale**, attached to failure conditions.

This is real modeling work and it is the actual cost of the approach. The generation tooling is straightforward once the model carries the semantics. Most of the effort is in the semantics.

## What it does not do

It does not perform the safety analysis. This distinction matters and it is where these efforts most often get oversold.

Deciding that a failure condition is catastrophic rather than hazardous is engineering judgment informed by operational context, certification precedent, and experience that is not in the model. Identifying a failure mode nobody thought of is creative work. Recognizing that a common-cause failure defeats a redundancy that looks independent on paper requires knowing things about physical installation that a logical architecture model does not represent.

What derivation does is remove the clerical layer — enumeration, propagation tracing, cross-referencing, consistency checking — so the engineers doing the judgment work spend their time on judgment rather than on maintaining tables. It also makes the judgment auditable, because every classification is attached to the element it classifies rather than living in a document that references it by name.

## Reproducibility is the requirement that shapes the design

For certification, the generated artifact must be reproducible. Same model state, same tool version, same output. This constrains implementation more than anything else.

It means generation cannot depend on iteration order over unordered collections, cannot embed timestamps in content, cannot sample the model at an unspecified state, and cannot depend on any nondeterministic component. If you are tempted to use a language model anywhere in the generation path, this is the constraint that tells you where: it can propose, a human disposes, and the disposition is what enters the artifact deterministically.

It also means model states have to be identifiable and retrievable. Regenerating the analysis from the version submitted eighteen months ago has to be possible, which is a versioning requirement on the model repository that programs frequently discover late.

## Where I would start

If you are considering this on an existing program, the entry point I would pick is not the full FHA. It is the consistency check.

Before generating anything, write validation that compares the existing safety artifact against the current model: does every component referenced in the FHA still exist, does every credited redundancy still have two paths, does every failure condition reference a function that is still allocated. Run it once.

The result of that first run is usually persuasive enough that you do not have to argue for the rest of the approach. It is also cheap, it does not require the full failure-mode semantics, and it delivers value on day one rather than after a modeling campaign.

Then build the semantics incrementally, starting with the subsystem where that first run found the most.

---

Related: [Model governance for SysML programs that have to certify](sysml-model-governance.html) and [Interface control documents should be models](interface-control-documents-as-models.html).
