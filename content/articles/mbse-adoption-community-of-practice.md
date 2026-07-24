---
title: What I Learned Leading an MBSE Community of Practice — Matthew Collaro
h1: What I learned leading an MBSE community of practice
description: Running a 100-engineer MBSE community of practice at Boeing taught me that modeling adoption fails for organizational reasons, and that the tool is almost never the problem.
type: article
date: 2026-03-27
---

I led a community of practice of more than a hundred engineers advancing MBSE adoption within Cabin and Network Systems at Boeing. Some of it worked. The parts that did not taught me more.

The summary, which I would have disbelieved beforehand: adoption is not a training problem, and it is not a tooling problem. It is a question of whether modeling is on the path to getting work done or beside it.

## The parallel-work problem

The single largest obstacle is that in early adoption, modeling is additive. An engineer's actual deliverable is a specification, a review package, an interface agreement. If modeling produces those, it is work. If modeling happens and then they also produce those by hand, it is homework.

Every failed adoption I have seen had engineers maintaining a model and separately maintaining the artifacts the program actually consumed. They did this conscientiously for a while. Then a schedule crunch arrived, they dropped the one that was not on the critical path, and it never came back.

The fix is unglamorous: make the model produce something the program requires, as early as possible, even if it is small. One generated interface table that goes into the real review package beats a beautiful complete model that nothing depends on. Once a deliverable comes out of the model, the model gets maintained, because now it is on the path.

I would now sequence an adoption around this exclusively. What artifact can we generate from the model within a month that someone currently makes by hand? Build that first. Model breadth second.

## Community of practice as a real mechanism

The community of practice worked better than training did, for a reason I did not anticipate.

Training teaches SysML. Almost nobody's problem was SysML. Their problem was "how do I represent this specific weird thing in my subsystem," and the answer was usually a convention decision rather than a language question. There is no course for that. There is only someone who has done it before.

What made the community valuable was that it was where those conventions got made and recorded. Someone would bring a modeling question, three people would have opinions, we would decide, and it would go in the modeling guide. Over time that guide became the actual asset — not because the decisions were profound, but because consistency across a hundred engineers is worth more than any individual decision being optimal.

The failure mode to watch is the community becoming a status meeting. If people are reporting progress rather than bringing problems, it has stopped working. I found it useful to open with an unresolved modeling question rather than a round-robin.

## Who to recruit first

I initially recruited enthusiasts. This was a mistake, though a pleasant one.

Enthusiasts adopt regardless. They will model whether you support them or not, and they will produce sophisticated models that other engineers find intimidating and unrepresentative. Their success proves nothing to skeptics, who correctly observe that the enthusiast would have done it anyway.

The people worth recruiting are the respected pragmatists — engineers with credibility who are not especially interested in modeling but have a problem modeling solves. When that person says the model saved them a week on change impact, it moves the organization. When the enthusiast says it, it confirms a prior.

They are also harder to recruit and require you to actually deliver value quickly, which is a useful discipline.

## Governance has to arrive before the model gets big

I have written elsewhere about [model governance](sysml-model-governance.html). The adoption-specific point is about timing.

There is a window early on where establishing conventions costs almost nothing, because the model is small and few people are working in it. Programs skip this because it feels premature and there is pressure to show model content.

Then the model is large, twenty engineers have developed incompatible local conventions, and harmonizing them is a project nobody has budget for. I have restored degraded architecture models — that was a substantial part of my work at Northrop Grumman — and the cost of retrofitting structure is many times the cost of establishing it early.

If I had one lever, I would spend it here. Set naming, decomposition, and traceability conventions in the first month, enforce them automatically, and accept looking slow for a few weeks.

## What skeptics are usually right about

Engineers who resist modeling are often objecting to something real, and treating the objection as resistance-to-change wastes the information.

"This does not represent how the system actually works." Often true, especially in early models built by people learning the domain and the notation simultaneously. The response is to fix the model, and to be glad someone read it closely enough to notice.

"I can draw this in PowerPoint in ten minutes." Also often true, for a single diagram. The counter is not that PowerPoint is unprofessional. It is change impact — the slide cannot tell you what breaks when the interface moves. If you cannot demonstrate that benefit concretely on their subsystem, they are right and you should improve your case rather than theirs.

"The tool is painful." Almost always true. Nothing is gained by pretending otherwise, and credibility is lost. Acknowledge it, and be honest that the tradeoff is tool friction now against integration archaeology later.

## The thing I would tell myself

Adoption is measured in artifacts that depend on the model, not in model content. A program with a small model that three real deliverables are generated from has adopted MBSE. A program with an enormous model that nothing depends on has adopted a hobby, and it will be cancelled the first time the schedule tightens.

---

Related: [Model governance for SysML programs that have to certify](sysml-model-governance.html) and [From mechanical engineering to MBSE](mechanical-engineer-to-mbse.html).
