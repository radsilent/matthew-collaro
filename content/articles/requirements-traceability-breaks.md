---
title: Why Requirements Traceability Breaks, and What Actually Fixes It — Matthew Collaro
h1: Why requirements traceability breaks, and what actually fixes it
description: Traceability decays on real programs for structural reasons, not because engineers are lazy. A look at the actual failure modes and what a fix has to do.
type: article
date: 2026-07-14
---

Every program I have worked on had a traceability matrix. Most of them had one that was wrong.

This is not a story about undisciplined engineers. The people maintaining those matrices were conscientious, and on several programs they were the most conscientious people in the building. Traceability decays for structural reasons, and if you do not address the structure, you get the same outcome with better people and more meetings.

## The failure modes

**Traceability is maintained as a separate artifact.** The requirements live in DOORS. The architecture lives in Cameo. The test cases live somewhere else, frequently a spreadsheet with a name like `Verification_Matrix_v14_FINAL_rev2.xlsx`. The trace links live in a fourth place that references the other three by identifier.

The moment those identifiers can change independently, the links are guesses. Someone renames a requirement, someone refactors a block in the model, and the link still resolves to a string that no longer means what it meant. Nothing errors. The matrix still looks complete. It is now lying to you, and it will keep lying quietly until an audit or a test failure surfaces it.

**Links are created at the wrong time.** Trace links get created during a push before a milestone, by whoever has capacity, working from documents rather than from the design conversation. That person is reconstructing intent they were not present for. They will produce links that are defensible in review and disconnected from why the requirement exists.

The link that matters is the one made by the engineer who decided that this component satisfies that requirement, at the moment they decided it. Any later reconstruction is archaeology.

**There is no cost to a missing link.** In most toolchains you can commit a model change that orphans six requirements and nothing happens. No build fails. No reviewer is notified. The cost arrives months later, distributed across people who did not cause it. Systems where the cost of breakage is deferred and diffuse reliably accumulate breakage.

**Coverage is measured, correctness is not.** Programs report traceability coverage — the percentage of requirements with at least one downstream link. This is the metric that is easy to compute, so it is the metric that gets reported, so it is the metric that gets gamed. You can reach 100% coverage with links that are individually meaningless. I have seen requirements traced to a component whose only relationship to the requirement was that both mentioned the word "power."

Coverage tells you a link exists. It tells you nothing about whether the link is true.

## What a fix has to do

**Make the link a first-class object, not a reference.** If a trace link is a row in a spreadsheet pointing at two identifiers, it will rot. If it is an edge in a graph where both endpoints are the actual objects, then renaming a requirement moves the edge with it, and deleting a component either fails or explicitly orphans what depended on it. This is the same reason you use foreign keys instead of storing a name and hoping.

This is not a tooling preference. It is the difference between a relationship the system knows about and a relationship the system merely records.

**Make breakage immediate and local.** The engineer who orphans a requirement should find out during their change, not during a review board six weeks later. This means validation has to run where the work happens — in the model, on commit, in CI — and it has to name the person who caused it while they still have the context to fix it in ten minutes.

Programs resist this because it feels like friction. It is friction. It is a small amount of friction now instead of a large amount of archaeology later, and the exchange rate is extremely favorable.

**Capture rationale with the link.** A trace link with no rationale is a claim with no argument. Ten minutes of typing when the decision is made saves an afternoon of reconstruction when someone asks why in eighteen months. The engineers who resist this most are usually the ones who will be asked.

**Measure change impact, not coverage.** The question worth answering is not "what fraction of requirements have links." It is "if I change this interface, what needs review." A traceability structure that can answer the second question accurately is useful even at partial coverage. One that reports 100% coverage but cannot answer it is theater.

I would rather have 60% coverage I trust than 100% I do not, and I have worked with both.

## The part nobody wants to hear

Most traceability problems are ownership problems dressed as tooling problems.

When an interface has no clear owner, its requirements do not get traced properly, because tracing forces you to state precisely who is responsible for satisfying what. Ambiguity is comfortable. Formal traceability removes the comfort, which is exactly why it gets deprioritized, and why the deprioritization is always justified on schedule grounds.

If you introduce rigorous traceability to a program with unresolved ownership boundaries, the first thing that happens is not better traceability. It is a series of uncomfortable conversations about who owns what. Those conversations are the actual deliverable. The links are a byproduct.

I have come to think of a traceability initiative as a diagnostic instrument. If it goes smoothly, the program had clear ownership. If it stalls, you have found something more important than a stalled traceability initiative.

---

Related: [Model governance for SysML programs that have to certify](sysml-model-governance.html) and [Interface control documents should be models](interface-control-documents-as-models.html).
