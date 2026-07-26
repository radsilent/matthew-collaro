---
title: Modeling Automotive HMI and Infotainment Integration, Matthew Collaro
h1: Modeling automotive HMI and infotainment integration
description: Notification timing, media routing, and vehicle state synchronization defects are integration problems disguised as feature bugs. Behavioral modeling is how you find out which is which.
type: article
date: 2026-02-13
---

A driver gets a navigation prompt while a phone call is connecting and music is ducking. Three subsystems own pieces of that moment and none owns the moment itself.

This is the category of problem I work on at Lucid: cross-domain integration of infotainment and driver feedback systems on autonomy-enabled builds. Notification timing, media routing, vehicle state synchronization. They arrive as feature bugs. They are almost never feature bugs.

## Why these defects are structurally hard

Coming from aircraft, the thing that struck me about vehicle infotainment is how much of the behavior is *emergent across domains that were specified independently*.

The audio path involves an infotainment controller, an amplifier, possibly a body module for chimes, and increasingly an autonomous compute domain that wants to produce driver feedback of its own. Each has a specification. Each specification is correct. The interaction between them is specified nowhere, because no single document has scope over it.

So the defect shows up as: under this specific combination of vehicle state, active media source, and pending notification, the wrong thing is audible, or the right thing is audible half a second late, or the chime plays and the navigation prompt is suppressed when it should be the reverse.

Every team looks at their own subsystem and finds it behaving to spec. They are all correct. The specifications are incomplete in a region none of them own.

## Behavioral models over structural ones

Structural modeling, which component connects to which, what signals cross the boundary, is necessary and does not catch these. The connections are all present. The signals all exist. The problem is *sequencing and arbitration*, which structure does not express.

What has been useful is behavioral modeling of the interaction itself: state machines for the arbitration logic, sequence diagrams for the cross-domain flows, and explicit modeling of priority relationships between audio sources and notification classes.

The exercise of building these is where most of the value is, before anyone runs anything. You sit down to model what happens when a navigation prompt arrives during an active call with media ducked and an autonomy alert pending, and you discover that nobody knows. Not that it is wrong, that it is undefined. Three teams have three reasonable assumptions and no forum has ever put them in the same room.

That discovery is the deliverable. The model is how you force the question into a form that cannot be deferred.

## Signal ownership and functional ownership are different

The clarifying distinction I keep returning to: knowing which module *emits* a signal is not knowing which function *owns* the behavior.

A chime is emitted by a body module. The decision that a chime is appropriate right now might belong to a driver-attention function that lives in a different domain entirely. If you model only emission, you will attribute the behavior to the body module, and you will route the defect to a team that can only change when the chime plays, not whether it should have.

Modeling functional ownership separately from signal emission, and making the allocation between them explicit, changes where defects get routed and what the fix looks like. It also tends to reveal that some functions have no owner, which is uncomfortable and worth knowing during platform bring-up rather than during a launch readiness review.

## Timing has to be in the model

Notification timing defects are the ones most resistant to structural analysis, because the structure is right and the timing is wrong.

If the model does not express latency budgets, message periodicity, and ordering constraints, then a model review cannot catch a timing defect and you are relying entirely on the bench. Putting timing in the model is more work and it converts a class of bench findings into a class of review findings.

Practically this means annotating flows with expected latency, marking which sequences have ordering requirements versus which are genuinely concurrent, and being explicit about what happens when a budget is exceeded: because the degraded behavior is a design decision, and if it is not modeled it will be an accident.

## Autonomy raises the stakes

The autonomy compute domain changes the character of this work. It produces driver feedback that is not entertainment and not convenience, it is safety-relevant communication about vehicle state and intent.

That feedback has to arbitrate against media and notifications that were designed under the assumption that the worst case of getting it wrong was an annoyed driver. Once one of the contenders is telling the driver something about the vehicle's behavior, the arbitration policy is a safety-relevant design decision.

Which means it needs to be specified, modeled, traced to requirements, and verified, rather than being emergent from three independently reasonable subsystem specifications. This is where the aerospace habits transfer cleanly. The question "what is the worst thing that happens if this is late, suppressed, or wrong" is a normal question in aircraft systems, and it is the right question here.

## What transfers from aerospace, and what does not

**Transfers:** interface discipline, the instinct to model failure and degraded behavior rather than only nominal, the assumption that anything unspecified will eventually be resolved unfavorably, and the practice of tracing behavior to a requirement someone owns.

**Does not transfer:** the pace, and the tolerance for process. Vehicle programs iterate faster than aircraft programs by a wide margin, and a modeling approach that requires a change board to update a state machine will be routed around within a week. The modeling has to be light enough to keep up with the build cadence.

The version that works is narrow and deep: model the cross-domain interactions that are genuinely emergent, at the fidelity needed to answer arbitration and timing questions, and do not attempt to model the entire vehicle. Breadth is what kills these efforts.

---

Related: [Interface control documents should be models](interface-control-documents-as-models.html).
