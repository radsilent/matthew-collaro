---
title: From the Factory Floor to Systems Architecture — Matthew Collaro
h1: From the factory floor to systems architecture
description: How writing overhaul instructions for flight control actuators turned out to be useful preparation for architecture modeling, and what I would tell someone making the same move.
type: article
date: 2026-01-24
---

My first engineering job was writing repair and overhaul work instructions for electro-mechanical flight control actuation systems at Parker Hannifin. Military aircraft sustainment. A mechanical engineering degree and a stack of drawings.

It is not the obvious path into model-based systems engineering, and for a while I treated it as something to get past. I have come around to thinking it was the most useful two years I could have had.

## What manufacturing teaches that architecture does not

**A specification is only as good as the person who has to follow it.** Overhaul instructions are read by a technician with a part in front of them. Any ambiguity gets resolved by them, on the spot, in a way you will not learn about. If step 14 says "torque to specification" and the specification is in a different document, step 14 is wrong regardless of how defensible it looked in review.

That is the same failure as a requirement that says "the system shall respond promptly." Somebody downstream will resolve it, and they will not resolve it the way you meant. I have never been able to un-see this, and it makes me much less patient with prose requirements than I would otherwise be.

**Physical constraints do not negotiate.** You cannot schedule around a fixture that does not exist or a tolerance that cannot be held. Software and architecture work has more give in it, and that flexibility makes it easy to defer hard questions. Manufacturing does not offer the option, which is good training.

**Interfaces are real objects.** When I replaced legacy analog hydraulic test units with digital data acquisition systems, the interface was not a line on a diagram. It was a connector, a signal conditioning path, a sample rate, and a calibration procedure. It is harder to hand-wave an interface after you have physically wired one and watched it produce nonsense because of an assumption you did not know you had made.

Most interface defects I have seen since are the same defect at a different scale: two sides holding incompatible assumptions that neither wrote down.

## The transition

I moved into systems engineering at Raytheon, modeling embedded system interfaces and building SysML and DoDAF architecture models. The gap I had to close was notation, and I over-estimated how large that gap was.

SysML is not difficult. It is a notation with a specification, and a few weeks of deliberate practice gets you to competence. Georgia Tech's SysML 101/201 sequence was useful for structure, but the language itself was never the obstacle.

The real gap was *method* — knowing what to model, in what order, at what fidelity, and when to stop. Nobody teaches that well, because it is mostly judgment accumulated by doing it and getting it wrong. My first models were meticulous and useless: correct syntax, arbitrary decomposition, far more detail in the parts I understood than the parts that mattered.

The other gap was scope of concern. As a manufacturing engineer my question was "can this be built and maintained." As a systems engineer the question became "is this the right thing, does it satisfy what it must, and can we prove it." Verification thinking in particular took a while, because it requires designing backwards from evidence rather than forwards from function.

## What I would tell someone making the move

**Learn the method, not just the notation.** Being fluent in SysML and having no method produces syntactically valid models with arbitrary structure. Read about OOSEM or a comparable method and use it deliberately, even when it feels like overhead. The sequencing is the value.

**Model something you already understand deeply.** Your first model should be of a system you know cold, so that when the model looks wrong you can tell it is wrong. Modeling an unfamiliar system in an unfamiliar notation means you cannot distinguish your errors from your ignorance.

**Find out what the model is for before building it.** The most common waste is modeling breadth nobody needs. Ask what question the model will answer and what artifact it will produce. If there is no answer, the model will be abandoned, and you should know that going in.

**Keep the physical instinct.** Systems engineering has a tendency to drift into abstraction, and models can become internally consistent descriptions of nothing. Coming from manufacturing is a defense against that. The question "how would you actually test this" is one of the most useful things you can ask in an architecture review, and people with hands-on backgrounds ask it more.

## Where it led

The thread from overhaul instructions to what I do now is more continuous than it looks. Instructions were about making a procedure unambiguous enough to be executed correctly by someone who was not in the room when it was written. Interface modeling is the same problem between subsystems. Requirements traceability is the same problem across time. The [governed tooling I build now](../projects.html) is the same problem again, where the party who was not in the room is an automated one.

The specific technologies changed. The question did not: how do you write something down precisely enough that it survives being handed to someone else.

---

Related: [What I learned leading an MBSE community of practice](mbse-adoption-community-of-practice.html).
