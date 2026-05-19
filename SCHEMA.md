# Data Schema Documentation

This document defines the structured schema for the processed call logs optimized for LLM (Claude) context injection.

## Core Schema Fields

| Field Name | Type | Description | Format / Example |
| :--- | :--- | :--- | :--- |
| `call_id` | String | Unique identifier of the call log | `"RKL-001"` |
| `phone` | String | Customer phone number formatted to E.164 standard | `"+34123456789"` |
| `created_at` | String | Explicit ISO 8601 timestamp localized to Madrid timezone | `"2026-05-20T14:30:00+02:00"` |
| `recording_url`| String | Direct secure URL path to the Rinkel audio recording file | `"https://rinkel.link/audio1.mp3"` |
| `notes` | String | System or operator clean text notes (UTF-8 encoded) | `"Client from Madrid.\nNeeds follow up."` or `null` |
| `resolved` | Boolean| Strictly enforced status flag | `true` or `false` |
| `transcript` | String | Full text transcript generated via OpenAI Whisper | `"Hola, buenas tardes..."` |

