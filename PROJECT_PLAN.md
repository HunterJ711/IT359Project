# APTriage - IT 359 Final Project Plan

**Course:** IT 359 - Penetration Testing  
**Project Team:** Hunter Jackson and Tyler Werner  
**Project Start Date:** August 27, 2026  
**Final Completion Date:** December 3, 2026  
**Primary Repository Platform:** GitHub  

---

## 1. Overview

### Project Name

**APTriage - AI-Assisted Penetration Testing Analysis and Reporting Tool**

### Project Description

APTriage will be a Python-based penetration testing support tool that turns raw Nmap scan results into organized, understandable, and actionable security findings.

The tool will run or import an authorized Nmap scan, extract information such as hosts, open ports, services, protocols, and service versions, and organize those results into structured findings. Basic rule-based logic will identify findings that may deserve additional attention and assign a simple severity level such as Low, Medium, or High.

Artificial intelligence will then assist with analysis by explaining what selected findings mean, why they may matter from a security perspective, and what remediation steps could reduce the associated risk. APTriage will combine the original scan evidence, severity classification, AI-generated analysis, and remediation guidance into a readable penetration testing report.

The project is intended only for educational use and authorized testing environments. APTriage will focus on reconnaissance analysis and reporting rather than automated exploitation.

### Core Workflow

```text
Authorized Target
       |
       v
     Nmap
       |
       v
Nmap XML Results
       |
       v
 Python Parser
       |
       v
Finding Classification
       |
       v
  AI Analysis
       |
       v
Report Generator
       |
       v
Final Pentest Report
```

### Objectives

The primary objectives of APTriage are to:

- Build a functional Python-based penetration testing support tool.
- Run or import authorized Nmap scans.
- Parse Nmap XML output.
- Extract discovered hosts, open ports, protocols, services, and available version information.
- Organize scan results into a clear and consistent format.
- Identify findings that may require additional attention.
- Assign simple Low, Medium, or High severity ratings.
- Integrate artificial intelligence into the analysis process.
- Use AI to explain the security significance of selected findings.
- Use AI to provide remediation recommendations.
- Clearly separate raw scan evidence from AI-generated interpretation.
- Generate a readable penetration testing report.
- Test the application in an authorized lab environment.
- Maintain a professional, well-organized public GitHub repository.
- Provide enough documentation for another user to install and operate the tool.

### Success Criteria

The project will be considered successful when:

1. APTriage runs successfully in the intended environment.
2. The program can execute or accept an authorized Nmap scan.
3. Nmap XML results are parsed correctly.
4. Hosts, ports, protocols, services, and available version information are extracted correctly.
5. Findings are organized into a consistent structure.
6. The application assigns a basic severity level to relevant findings.
7. AI successfully analyzes selected findings.
8. AI output includes understandable explanations and remediation recommendations.
9. Raw Nmap evidence remains visible and distinguishable from AI-generated analysis.
10. The application generates a readable final penetration testing report.
11. The tool is tested against authorized lab systems or intentionally vulnerable virtual machines.
12. The GitHub repository contains all required source code, documentation, dependencies, final report, and `docs/Presentation_Slides.pdf`.
13. Hunter Jackson and Tyler Werner can successfully demonstrate the complete workflow during the 10-15 minute in-person presentation, with each member speaking meaningfully.

---

## 2. Stakeholders

### Sponsor Designation

**Project Sponsor / Evaluator:** IT 359 Course Instructor

The course instructor serves as the project sponsor and evaluator by defining academic requirements, providing guidance when necessary, and evaluating the completed project and deliverables.

### Stakeholder List

| Stakeholder | Role | Responsibilities |
|---|---|---|
| Hunter Jackson | Co-Project Lead / Developer | Nmap integration, XML parsing, application structure, testing, GitHub organization, documentation, and project coordination |
| Tyler Werner | Co-Project Lead / Developer | Finding classification, AI integration, prompt development, reporting functionality, testing, documentation, and project coordination |
| IT 359 Instructor | Sponsor / Evaluator | Define requirements, provide academic guidance, and evaluate final deliverables |
| Authorized Lab Users / Test Environment | Test Stakeholder | Provide safe and authorized systems for testing and demonstration |

Both team members will contribute to development, code review, debugging, testing, documentation, the final report, and the in-person presentation.

---

## 3. Scope Management

### In-Scope Items

The required project scope includes:

- Python-based application development.
- Nmap scan execution or Nmap result importing.
- Nmap XML parsing.
- Extraction of:
  - IP addresses
  - Host status
  - Open ports
  - Protocols
  - Running services
  - Available service version information
- Organization of scan findings.
- Basic rule-based finding classification.
- Low, Medium, and High severity ratings.
- Identification of potentially important exposed services or configurations.
- AI integration.
- AI-generated explanations of findings.
- AI-generated security significance summaries.
- AI-generated remediation recommendations.
- Clear labeling of AI-generated content.
- Final report generation in a readable format such as Markdown or HTML.
- Command-line interface.
- Input validation and basic error handling.
- Testing against authorized systems or intentionally vulnerable virtual machines.
- GitHub source control and repository management.
- README documentation.
- Dependency documentation.
- Final 5-7 page PDF report.
- Final 10-15 minute project presentation and live demonstration.

### Out-of-Scope Items

The following features are not required for successful completion:

- Automated vulnerability exploitation.
- Automated privilege escalation.
- Credential attacks or password cracking.
- Malware development.
- Persistence mechanisms.
- Antivirus or security-evasion functionality.
- Testing unauthorized public systems.
- Building a replacement for Nmap.
- Creating a vulnerability scanner completely from scratch.
- Fully autonomous AI penetration testing.
- Large-scale enterprise vulnerability management.
- Complex graphical interfaces.
- Multiple scanner integrations.
- Full CVE database integration.
- Automated CVSS calculation.

These items may be considered only as future enhancements and will not take priority over the required core features.

### Project Assumptions

The project assumes that:

- Python 3 will be available on the development systems.
- Nmap can be installed and executed.
- An authorized lab or virtual-machine environment will be available.
- Internet access will be available if a cloud-based AI service is selected.
- GitHub will be available for version control and project submission.
- AI-generated content will be treated as supplemental analysis rather than unquestioned fact.
- Important AI-generated conclusions will be reviewed by the project team.
- Testing will only be performed against authorized targets.

### Project Constraints

Major constraints include:

- The project is being completed by two students while balancing other coursework.
- The final repository and deliverables must be completed by December 3, 2026.
- AI output may occasionally be inaccurate or overly general.
- AI APIs may have usage limits or costs.
- Nmap results vary depending on the target system and scan permissions.
- Security testing must remain within explicitly authorized environments.
- The project must remain small enough to be fully tested, documented, and demonstrated by the deadline.

---

## 4. GitHub Repository Management

GitHub will serve as the central location for source control, project documentation, task tracking, collaboration, and final submission.

### Planned Repository Structure

```text
aptriage/
|
|-- .gitignore
|-- README.md
|-- PROJECT_PLAN.md
|-- requirements.txt
|
|-- src/
|   |-- main.py
|   |-- scanner.py
|   |-- parser.py
|   |-- classifier.py
|   |-- ai_analyzer.py
|   `-- reporter.py
|
|-- tests/
|   |-- test_parser.py
|   |-- test_classifier.py
|   `-- sample_scans/
|
|-- docs/
|   `-- Final_Writeup_Jackson_Werner.pdf
|
`-- output/
    `-- example_report.md
```

The exact filenames may change during development, but the repository will remain organized around source code, tests, documentation, and sample output.

### GitHub Workflow

The team will use the following practices:

- The `main` branch will contain stable code.
- Larger features may be developed in separate feature branches before being merged.
- GitHub Issues will be used to track bugs, features, and action items.
- GitHub Projects may be used as a simple Kanban board with categories such as **Backlog**, **In Progress**, **Testing**, and **Done**.
- Commits will be made regularly with descriptive commit messages.
- Pull requests may be used for larger changes to allow the other team member to review code before merging.
- The repository README will contain installation instructions, dependencies, and usage examples.
- Secrets such as API keys will never be committed to the repository.
- A `.gitignore` file will exclude virtual environments, API key files, temporary output, and other unnecessary files.

---

## 5. Timeline and Milestones

The project will be developed incrementally from August 27 through December 3, 2026. Core functionality will be completed before the final weeks so that the end of the project can focus on testing, documentation, presentation preparation, and polish.

| Target Date | Milestone | Key Deliverables |
|---|---|---|
| Aug. 27 | Project kickoff | Project plan finalized; team responsibilities established |
| Sept. 3 | GitHub setup | Public repository created; `.gitignore`, `README.md`, `PROJECT_PLAN.md`, and initial folder structure added |
| Sept. 10 | Development environment | Python environment configured; Nmap installed/tested; sample XML scan files collected |
| Sept. 17 | Nmap input | APTriage can run an authorized Nmap scan or accept an existing Nmap XML file |
| Sept. 24 | XML parser | Hosts, ports, protocols, services, and service versions are extracted from scan results |
| Oct. 1 | Structured findings | Parsed results are converted into consistent internal finding objects/data structures |
| Oct. 8 | Severity classification | Basic Low/Medium/High classification logic is implemented and tested |
| Oct. 15 | AI design | AI provider selected; prompt format and AI input/output structure finalized |
| Oct. 22 | AI integration | Application can send selected findings to AI and receive explanations and remediation recommendations |
| Oct. 29 | Report generator | Scan evidence, severity, AI explanations, and remediation are combined into a readable report |
| Nov. 5 | Core application integration | Complete Nmap -> parser -> classification -> AI -> report workflow functions end-to-end |
| Nov. 12 | Functional testing | Multiple authorized scan files and targets tested; bugs documented in GitHub Issues |
| Nov. 19 | Stabilization | Major bugs fixed; error handling improved; code cleaned and commented |
| Nov. 23 | Feature freeze | Required features complete; no new major features added after this point |
| Nov. 26 | Documentation | README setup/usage sections, dependencies, examples, and repository documentation substantially complete |
| Nov. 30 | Final writeup | 5-7 page PDF report completed and added to `docs/` |
| Dec. 1 | Demo preparation | Reliable demo target/sample scan prepared; presentation outline completed |
| Dec. 2 | Presentation and repository review | Live demonstration rehearsed; 8-12 slide deck exported to `docs/Presentation_Slides.pdf`; backup screenshots prepared; repository checked for missing files/secrets |
| **Dec. 3** | **Final project completion** | **Public GitHub repository finalized and ready for submission** |

### Minimum Viable Product Deadline

The team will aim to have the complete core workflow functional by **November 5, 2026**. The remaining time will be used for testing, debugging, documentation, the written report, and presentation preparation.

---

## 6. Risk Management

| Risk | Probability | Impact | Mitigation / Response |
|---|---|---|---|
| AI produces incorrect security information | Medium | High | Preserve original scan evidence, clearly label AI output, and manually review important conclusions |
| Nmap XML parsing fails on certain scans | Medium | High | Test multiple XML files and handle missing fields safely |
| Project scope becomes too large | Medium | High | Prioritize the minimum viable product and treat additional features as optional |
| AI API becomes unavailable | Low-Medium | Medium | Keep scanning/parsing/classification functional without AI and save known-good test outputs |
| API usage creates unexpected cost | Low | Medium | Limit requests to relevant findings and monitor usage |
| One team member becomes temporarily unavailable | Low-Medium | Medium | Keep all source code and documentation synchronized through GitHub so either member can continue work |
| Merge conflicts or integration bugs occur | Medium | Medium | Use frequent pulls, small commits, feature branches when appropriate, and code review before large merges |
| Testing environment becomes unavailable | Low | Medium | Maintain saved Nmap XML files for development and demonstration backup |
| Live demonstration scan fails | Medium | Medium | Prepare a reliable authorized test environment and saved sample scan as a fallback |
| Sensitive API key is accidentally committed | Low | High | Use environment variables, `.env` files excluded through `.gitignore`, and review commit history before publication |
| Project falls behind schedule | Medium | High | Complete core functionality by early November and reserve the final weeks for polish rather than new features |
| Unauthorized target is accidentally scanned | Low | High | Only use clearly identified course labs, local VMs, or explicitly authorized targets |

---

## 7. Resources

### Budget Allocation

The project is expected to require little or no direct cost.

| Resource | Estimated Cost |
|---|---:|
| Python | $0 |
| Nmap | $0 |
| Git / GitHub | $0 |
| Visual Studio Code or similar IDE | $0 |
| Authorized lab / virtual machines | $0 |
| AI service | $0-$20 |
| **Estimated Total** | **$0-$20** |

The team will prioritize free and open-source tools whenever possible.

### Required Tools and Technology

Expected technologies include:

- Python 3
- Nmap
- Git
- GitHub
- GitHub Issues / Projects
- Visual Studio Code or equivalent IDE
- Nmap XML output
- Python XML parsing
- JSON where appropriate
- AI API or other approved AI model
- Markdown and/or HTML for reporting
- Authorized lab systems or virtual machines

Potential Python modules/libraries include:

- `xml.etree.ElementTree`
- `subprocess`
- `requests`
- Selected AI client library
- `rich` for improved terminal output if desired

The final dependency list will be documented in `requirements.txt`.

### Project Dependencies

APTriage depends on:

1. Python installation.
2. Nmap installation.
3. Access to authorized testing targets.
4. Successful Nmap result generation.
5. Successful parsing of Nmap XML output.
6. Access to the selected AI model.
7. GitHub availability for collaboration and final submission.
8. Successful integration of parsing, classification, AI analysis, and reporting components.

The major technical dependency chain is:

```text
Nmap Integration
      |
      v
Result Parsing
      |
      v
Finding Classification
      |
      v
AI Analysis
      |
      v
Report Generation
```

---

## 8. Communication

### Meeting Cadence

Hunter Jackson and Tyler Werner will conduct a project sync **at least once per week**, with additional communication as needed during active development or integration periods.

Weekly discussions will cover:

- Recently completed tasks.
- Current work in progress.
- Technical blockers.
- Open GitHub Issues.
- Upcoming milestones.
- Testing results.
- Division of upcoming work.
- Whether the project remains on schedule.

### Reporting Frequency

Progress will be reviewed weekly against the milestone schedule. Major completed features will be reflected through GitHub commits, Issues, and repository history.

### Communication Channels

- **GitHub:** Source control, Issues, Project board, documentation, and final deliverables.
- **GSD:** Action-item tracking when required by the course project-plan format.
- **Text / Discord or agreed messaging platform:** Quick team communication.
- **Email:** Instructor communication when necessary.
- **In-person / class discussion:** Questions, instructor feedback, and project coordination.

---

## 9. Action Items

The following items can be entered as GitHub Issues and, where required, pushed to the main GSD inbox for tracking.

| Action Item | Owner | Due Date | GitHub Issue | GSD Sync |
|---|---|---|---|---|
| Finalize and submit project plan | Hunter / Tyler | Aug. 27 | Yes | Yes |
| Create public GitHub repository | Hunter | Sept. 3 | Yes | Yes |
| Add repository structure and `.gitignore` | Hunter | Sept. 3 | Yes | Yes |
| Add initial README and project plan | Hunter / Tyler | Sept. 3 | Yes | Yes |
| Configure Python development environments | Hunter / Tyler | Sept. 10 | Yes | Yes |
| Install and test Nmap | Hunter | Sept. 10 | Yes | Yes |
| Collect safe sample Nmap XML files | Hunter | Sept. 10 | Yes | Yes |
| Implement Nmap execution/import functionality | Hunter | Sept. 17 | Yes | Yes |
| Develop Nmap XML parser | Hunter | Sept. 24 | Yes | Yes |
| Create structured finding format | Hunter / Tyler | Oct. 1 | Yes | Yes |
| Develop finding classification logic | Tyler | Oct. 8 | Yes | Yes |
| Select AI integration method | Tyler | Oct. 15 | Yes | Yes |
| Develop AI prompt structure | Tyler | Oct. 15 | Yes | Yes |
| Implement AI analysis module | Tyler | Oct. 22 | Yes | Yes |
| Integrate AI analysis with parsed findings | Hunter / Tyler | Oct. 22 | Yes | Yes |
| Develop report generator | Tyler | Oct. 29 | Yes | Yes |
| Complete end-to-end application integration | Hunter / Tyler | Nov. 5 | Yes | Yes |
| Perform functional testing | Hunter / Tyler | Nov. 12 | Yes | Yes |
| Log and resolve major bugs | Hunter / Tyler | Nov. 19 | Yes | Yes |
| Reach feature freeze | Hunter / Tyler | Nov. 23 | Yes | Yes |
| Complete README setup and usage guide | Hunter | Nov. 26 | Yes | Yes |
| Complete final 5-7 page report | Hunter / Tyler | Nov. 30 | Yes | Yes |
| Prepare demonstration environment | Hunter / Tyler | Dec. 1 | Yes | Yes |
| Create 8-12 presentation slides and export `docs/Presentation_Slides.pdf` | Hunter / Tyler | Dec. 2 | Yes | Yes |
| Rehearse the 10-15 minute in-person presentation and live demonstration | Hunter / Tyler | Dec. 2 | Yes | Yes |
| Add backup demonstration screenshots to the slide deck | Hunter / Tyler | Dec. 2 | Yes | Yes |
| Review public repository for completeness and exposed secrets | Hunter / Tyler | Dec. 2 | Yes | Yes |
| Finalize repository for submission | Hunter / Tyler | **Dec. 3** | Yes | Yes |

---

## 10. Division of Responsibilities

### Hunter Jackson - Primary Focus

- Project organization and GitHub repository setup.
- Nmap installation and integration.
- Nmap XML parsing.
- Command-line application structure.
- Test environment and sample scan management.
- Application integration.
- README setup and usage documentation.

### Tyler Werner - Primary Focus

- Finding classification logic.
- AI model integration.
- AI prompt design.
- AI-generated security explanations.
- Remediation recommendation generation.
- Report-generation functionality.
- Testing and documentation.

### Shared Responsibilities

Both team members will participate in:

- Architecture decisions.
- GitHub Issue management.
- Code review.
- Debugging.
- Integration testing.
- Security and authorization checks.
- Final report writing.
- Presentation preparation.
- Live demonstration.
- Final repository review and submission preparation.

The division of responsibilities establishes clear ownership without preventing either team member from contributing to other parts of the application.

---

## 11. Minimum Viable Product (MVP)

The minimum required version of APTriage will complete the following workflow:

1. Accept or generate an authorized Nmap scan.
2. Read the Nmap XML results.
3. Extract hosts, ports, protocols, services, and versions.
4. Convert scan results into organized findings.
5. Assign basic severity ratings.
6. Send relevant findings to an AI model.
7. Receive understandable explanations and remediation recommendations.
8. Clearly distinguish AI analysis from original scan evidence.
9. Generate an organized penetration testing report.

The MVP will be completed before optional features are considered.

---

## 12. Potential Future Enhancements

If the required project is completed early and adequate testing time remains, possible future enhancements include:

- Nikto scan result support.
- CVE lookup.
- CVSS scoring.
- Improved HTML reports.
- Comparison of scans from different dates.
- JSON or CSV export.
- Simple graphical interface.
- Additional severity rules.
- Support for additional reconnaissance or scanning tools.

These enhancements are not required for project success and will not take priority over stability, documentation, or testing.

---

## 13. Project Completion Definition

APTriage will be considered complete when Hunter Jackson and Tyler Werner can successfully demonstrate the following process:

**Nmap scan -> result parsing -> finding classification -> AI analysis -> generated penetration testing report**

By **December 3, 2026**, the public GitHub repository will contain:

- Complete source code.
- `.gitignore` file.
- `requirements.txt` or equivalent dependency documentation.
- Comprehensive README with project overview, setup, usage, testing, and limitations.
- Clear setup and execution instructions.
- Usage examples.
- Project plan.
- Test/sample data appropriate for public release.
- Final 5-7 page PDF report in the `docs/` folder.
- PDF copy of the 8-12 presentation slides at `docs/Presentation_Slides.pdf`.

The final project will demonstrate how artificial intelligence can assist penetration testers with one of the most time-consuming stages of the process: turning raw reconnaissance data into organized, understandable, and actionable security findings while keeping the final interpretation and decisions under human control.
