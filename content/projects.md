---
title: Projects — Matthew Collaro
h1: Projects
description: Engineering projects by Matthew Collaro, including VectorMBE, the Model Context Protocol server for MBSE toolchains, and an Isaac ROS perception kit for edge hardware.
type: page
date: 2026-07-24
---

Things I have built, in and out of working hours.

## VectorMBE

A governed engineering intelligence platform for synchronizing requirements, model context, semantic relationships, and system constraints across MBSE workflows. It is the product side of [Vector Stream Systems LLC](https://vectorstreamsystems.com/), and the subject of a pending U.S. provisional patent application.

The core problem it addresses is one I hit repeatedly on aircraft and missile programs: requirements, architecture models, and verification evidence live in separate tools with no enforced relationship between them, so they drift. By the time a review board notices, months of design work are committed.

VectorMBE connects those tools into a single graph with formal traceability, hybrid retrieval over that graph, and change propagation. When an interface definition changes, the system identifies every downstream requirement that needs review before the change lands rather than after.

Technically it is a hybrid: an ontology layer for the parts of the domain that benefit from formal semantics, and a plain directed graph for the parts that benefit from being fast and inspectable. It runs on Rust and Python in Docker, with CLI and API surfaces, and exposes context to AI tooling through the Model Context Protocol so that agents read structured, versioned system state through a controlled interface instead of scraping documents.

## vectormbe-mcp

A Model Context Protocol server that gives AI assistants governed access to an MBSE model. Rather than pointing a language model at a pile of exported documents, it exposes typed operations — query requirements, traverse traceability relationships, check constraint satisfaction, retrieve related design context — so that what the model sees is scoped, current, and attributable.

The design principle is that an agent should not be able to assert something about the system that the model cannot back up. Retrieval is grounded in the graph, and validation runs against rules the agent does not control.

## Isaac ROS Perception Kit

A reproducible perception pipeline built on NVIDIA Isaac ROS, pairing the Synthetica DETR detection model with Isaac Sim for synthetic data generation, targeted at modest edge hardware rather than a datacenter GPU.

The interesting constraint was fitting a real-time detection and tracking stack onto a small-form-factor workstation with an 8 GB card, which forces honest decisions about model selection, batch sizing, and where to spend memory. Source is on [GitHub](https://github.com/radsilent).

## Model-based safety and hazard assessment tooling

At Boeing I developed tooling that generated safety and hazard assessment artifacts directly from system models for certification-oriented analysis. The value was not the automation itself but the coupling: when the architecture model changed, the hazard analysis was no longer silently stale.

That idea — that safety artifacts should be derived from the model rather than maintained alongside it — carried directly into the safety assessment work in VectorMBE.

## Aircraft network architecture studies

Also at Boeing: conceptual work on distributed network architecture enhancements across the 777 and 787 platforms, aimed at safety, redundancy, and cyber resilience, alongside model-based Interface Control Diagrams used to identify networked system vulnerabilities during threat analysis.

Modeling interfaces formally turns out to be one of the more effective ways to find security problems, because an interface you cannot draw precisely is usually one nobody fully owns.
