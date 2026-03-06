# GRC Intelligence Tracker

A lightweight automation tool that monitors cybersecurity intelligence, regulatory updates, and vulnerability disclosures across major security frameworks.

This project aggregates threat intelligence and compliance updates into a single dashboard for security and GRC teams.

## Features

* Aggregates cybersecurity intelligence feeds
* Tracks regulatory framework updates
* Monitors newly disclosed vulnerabilities
* Generates a live HTML dashboard
* Automatically updates using GitHub Actions

## Data Sources

Threat Intelligence

* CISA News
* Krebs on Security

Framework and Regulatory Updates

* IASME Cyber Essentials
* NCSC UK
* TISAX
* Spain ENS

Vulnerability Feeds

* CISA Known Exploited Vulnerabilities (KEV)
* NVD CVE Feed

## Architecture

RSS Feeds → Python Tracker → Structured CSV Data → HTML Dashboard → GitHub Pages

## Automation

The project uses GitHub Actions to automatically run the tracker and update the dashboard every 12 hours.

## Example Use Cases

* GRC monitoring of regulatory updates
* Security intelligence tracking
* Vulnerability awareness
* Compliance program support

## Dashboard

The dashboard aggregates intelligence updates into a single view that can be used by security teams to monitor emerging risks.

## Future Improvements

* Vulnerability severity classification
* Search and filtering capabilities
* Framework change detection alerts
* AI generated summaries of security updates
