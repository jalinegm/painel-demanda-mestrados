# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Claude Artifact of the "Dashboard" type (https://claude.ai/artifact/3NdqmECK7GAG62GeJwvfhg). The page is one HTML file stored in the dashboard's own store, running inside the dashboard shell with d3 v7 and the type's `dash` API. No external fonts, scripts or network: assets must be embedded.

## Users

Professors on the team writing the IFFar professional master's proposals (APCN), plus IFFar management (campus directors, pró-reitoria). They open a shared link to see whether the demand study shows real interest in the programs.

## Product Purpose

Show the results of the "Estudo de Demanda — Mestrados Profissionais IFFar" form so the faculty and management see that there is real demand for the two proposed programs, and stay motivated to move the proposal forward. Success: a reader leaves convinced the demand exists and knows where it comes from (campus, municipality, profile, timing).

## Positioning

The only place that shows the live counts of the IFFar demand study for the two proposed programs: Mestrado Profissional em Ensino e Tecnologias (Campus Alegrete) and Mestrado Profissional em Ciências Ambientais e Sistemas Produtivos (Campi Alegrete, Júlio de Castilhos, Panambi).

## Operating Context

Data comes from the Google Forms response sheet, cleaned by `limpar_respostas.py` (email columns dropped; emails and phone numbers in free text removed) and refreshed daily by a scheduled task. Readers open it on desktop or phone from a shared link.

## Capabilities and Constraints

- Charts only; no full response table.
- Filter by course of interest (Ensino e Tecnologias / Ciências Ambientais e Sistemas Produtivos / both).
- Open comments shown as speech bubbles at the end of the page, attributed only by vínculo and município.
- Never show email or any contact data.
- Language: Brazilian Portuguese.

## Brand Commitments

Visual identity of the demand-study campaign pieces (Figma file "Estudo de Demanda — Mestrados Profissionais IFFar"): deep green #0E3B22, lime #C6E86B, white; Poppins (Black for highlighted headlines in lime bars, Bold/SemiBold/Medium for text); "ESTUDO DE DEMANDA" white tag; double chevron "»" markers; round "Ensino público GRATUITO e de qualidade" seal; campaign link bit.ly/mestradoIFFar. No portrait photos on the dashboard (user decision).

## Evidence on Hand

Real form responses only (285 on 2026-10-23, growing). No invented figures, testimonials or targets.

## Product Principles

1. Demand first: lead with the numbers that prove interest.
2. Every number comes from the responses; nothing typed by hand.
3. Respondents' voices are shown, but never who they are.
4. Same campaign look as the outreach pieces, so the study reads as one effort.
