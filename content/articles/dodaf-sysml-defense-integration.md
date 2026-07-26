---
title: DoDAF and SysML on Defense Programs, Without the Viewpoint Theater, Matthew Collaro
h1: DoDAF and SysML on defense programs, without the viewpoint theater
description: DoDAF viewpoints get produced because they are deliverable, not because anyone reads them. Making them fall out of a coherent model is what turns compliance into engineering.
type: article
date: 2026-03-06
---

On defense programs, architecture products are contract deliverables. That fact shapes how they get made, and usually not for the better.

I developed SysML and DoDAF architecture models at a defense prime supporting integration planning and verification alignment across defense systems, and MBSE architecture representations for advanced naval concept systems at Deloitte using OOSEM. The dysfunction is consistent across both, and it is worth naming precisely because it is so easy to reproduce.

## Viewpoint theater

The failure mode is producing DoDAF views as artifacts rather than as views.

A program owes an OV-1, an SV-1, an SV-6, a set of others. Someone is assigned to produce them. They produce them: as drawings, in whatever tool is convenient, each one authored independently. They are delivered, accepted, filed.

Nobody reads them again. They contradict each other within a revision or two, because there is nothing forcing consistency between an SV-1 drawn in one tool and an SV-6 maintained as a spreadsheet. And when the system changes, they are updated only if a delivery is due.

This is compliance. It is not architecture, and the engineers producing it generally know that, which is corrosive in its own way.

## Views should be projections

The word "view" is doing real work in the DoDAF framework and it gets ignored. A view is a projection of an underlying architecture description. If you author views directly, you have no underlying description, you have a stack of drawings that resemble one.

The alternative is to build one coherent model and generate the views from it. Then:

- The SV-1 and the SV-6 cannot disagree about which systems exchange which data, because they are rendered from the same elements.
- A change to a resource flow appears in every view that shows it, automatically.
- A missing element is visible as a gap in the model rather than as an inconsistency someone notices across two documents.
- Producing a new view for a new stakeholder is a rendering task, not an authoring project.

This is the actual argument for MBSE on defense programs, and it is much stronger than the argument usually made, which is about rigor in the abstract. Rigor in the abstract does not survive a schedule review. "We can regenerate the whole architecture product set in an afternoon instead of six weeks" does.

## Where SysML and DoDAF meet

SysML gives you the language. DoDAF gives you the required viewpoints. Mapping between them is where programs burn time, and where a couple of decisions determine whether the rest goes smoothly.

The mapping that has worked for me:

- **Operational activities** map to SysML activities, with operational nodes as blocks in an operational-level structure. Keep this layer genuinely operational: it is about mission, not implementation, and the discipline to keep implementation out of it is what makes it useful later.
- **Systems** map to blocks in a separate system-level structure, with an explicit allocation relationship to the operational elements they support. Allocation is the load-bearing relationship in the whole scheme; treat it as a first-class modeled thing rather than a naming convention.
- **Resource flows and data exchanges** map to item flows on connectors, typed by shared definitions. If SV-6 content is not derived from typed item flows, it will drift.
- **Capability elements** map to a capability taxonomy that requirements trace to, which is what lets you answer capability coverage questions without a manual roll-up.

The mistake I made early was modeling the views. Building a package per DoDAF product and populating each with the elements that product needs feels organized. It reproduces exactly the problem you were trying to solve, one layer down, and it is harder to unwind than starting over.

Model the system. Tag elements with the viewpoints they participate in. Generate.

## OOSEM is a sequencing discipline

The OOSEM work at Deloitte on naval concept systems clarified something for me about method versus notation.

SysML tells you how to write things down. It does not tell you what to do first. Teams that know SysML and have no method produce models that are syntactically fine and structurally arbitrary, the decomposition reflects whoever modeled which part in what order.

OOSEM's contribution is sequencing: analyze the operational need, define the system boundary and its external interfaces, elaborate behavior before structure, allocate to a logical architecture, then commit to physical. That order matters because each step constrains the next. Decisions made out of order get made without their constraints, and get revisited expensively.

For concept-stage work this is especially valuable, because the temptation to jump to a physical architecture is strongest exactly when you know the least. A concept model that commits to boxes in week two has foreclosed the trade space it existed to explore.

## Integration planning is the payoff

The most concrete return I have seen from doing this properly is integration planning.

When interfaces are modeled with types, when allocation is explicit, and when verification methods are attached to requirements, the integration sequence is largely derivable. You know which subsystems must be available before which tests, because you know which interfaces those tests exercise. You know what a slip in one subsystem does to the test schedule.

Producing that by hand, from documents, across software, electrical, and test teams, was a substantial part of what I did at a defense prime in technical data packages and subsystem integration instructions. Most of the effort was reconciling sources that disagreed. From a coherent model, it is a query.

That is the difference between architecture products as a deliverable and architecture as engineering.

---

Related: [Interface control documents should be models](interface-control-documents-as-models.html) and [Why requirements traceability breaks](requirements-traceability-breaks.html).
