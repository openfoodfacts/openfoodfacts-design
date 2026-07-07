# 🥗 Open Food Facts Design Onboarding Guide

Welcome to the Open Food Facts Design repository! This guide is here to help you—whether you’re a **Designer**, **Developer**, or **UX Researcher**—get started contributing to the look, feel, and usability of Open Food Facts products.

---

## 📦 What is Open Food Facts Design?

This repo contains the assets, documentation, and design system that power the visual and interactive experiences across Open Food Facts products. We collaborate on everything from UI components to user flows, accessibility, and user research.

---

## 👥 Who Is This For?

- **Designers:** UI, UX, Visual, Interaction, and Product Designers.
- **Developers:** Frontend, UI, and those implementing design system components.
- **UX Researchers:** Those running user studies, analyzing feedback, and improving usability.

---

## 🚩 Quick Start

### 1. **Get Access**
- Make sure you have a [GitHub account](https://github.com/).
- Request access to this repository if needed.
- **Figma Access:** Follow our [Figma Access & Contribution Guide](#figma) below to get started.

### 2. **Clone the Repo**
```bash
git clone https://github.com/openfoodfacts/openfoodfacts-design.git
cd openfoodfacts-design
```

### 3. **Explore the Directory**
NOT CREATED YET, STRUCTURE TO DEBATE
- `/assets`: Design files (Figma exports, SVGs, etc.)
- `/components`: UI components and guidelines
- `/docs`: Documentation (including this guide!)
- `/ux-research`: Research plans, reports, and insights

---

## 🛠️ For Designers

- **Design System:** Find the [Figma file](https://www.figma.com/) link in `/assets` or ask in Slack.
- **Additions:** Propose changes via issues or PRs. Attach Figma/Sketch/other files as needed.
- **Naming:** Use clear, descriptive names for assets and components.
- **Accessibility:** Follow [WCAG guidelines](https://www.w3.org/WAI/standards-guidelines/wcag/) in your designs.

---

## 💻 For Developers

- **Design Tokens:** Sync with `/components/tokens` for colors, spacing, typography, etc.
- **Implementation:** Check `/components` for specs and code snippets.
- **Feedback Loop:** Collaborate with designers early; raise issues if specs are unclear or incomplete.
- **Storybook (if available):** Run Storybook locally to view UI components in isolation.

---

## 🔬 For UX Researchers

- **Research Directory:** Use `/ux-research` for plans, surveys, and reports.
- **Issue Tracking:** Log findings as GitHub issues and tag relevant teams.
- **Collaboration:** Work with designers/devs to turn research into actionable design changes.

---

## 📣 Communication

- **Slack:** Join our [#design channel](https://openfoodfacts.slack.com/) for quick questions and discussions.
- **GitHub Issues:** Use issues for bugs, feature requests, or research tasks.
- **Meetings:** Participate in regular syncs (calendar invites sent via Slack).

## Weekly meetings (Design team only)

- We e-meet on Fridays at 09:00 Paris Time (08:00 London Time, 11:30 IST, 12:00 AM PT)
- ![Google Meet](https://img.shields.io/badge/Google%20Meet-00897B?logo=google-meet&logoColor=white) Video call link: <https://meet.google.com/xxxxxxxx>
- Join by phone: <https://tel.meet/xxxxxx>
- Add the Event to your Calendar by [adding the Open Food Facts community calendar to your calendar](https://wiki.openfoodfacts.org/Events)
- [Weekly Agenda](https://docs.google.com/xxxxx/edit): please add the Agenda items as early as you can. Make sure to check the Agenda items in advance of the meeting, so that we have the most informed discussions possible, leading to reasoned decisions.
- The meeting will handle Agenda items first, and if time permits, collaborative bug triage.
- We strive to timebox the core of the meeting (decision making) to 30 minutes, with an optional free discussion/live debugging afterwards.
- We take comprehensive notes in the Weekly Agenda of agenda item discussions and of decisions taken.

## Weekly office hours (Design team, Developers and Community welcome)
- We e-meet on Fridays at 09:00 Paris Time (08:00 London Time, 11:30 IST, 12:00 AM PT)
- ![Google Meet](https://img.shields.io/badge/Google%20Meet-00897B?logo=google-meet&logoColor=white) Video call link: see the current event details in the community calendar: <https://wiki.openfoodfacts.org/Events>
- Join by phone: <https://tel.meet/xxxxxx>
- Add the Event to your Calendar by [adding the Open Food Facts community calendar to your calendar](https://wiki.openfoodfacts.org/Events)
- [Weekly Agenda](https://docs.google.com/document/d/REPLACE_WITH_ACTUAL_WEEKLY_AGENDA_ID/edit): please add the Agenda items as early as you can. Make sure to check the Agenda items in advance of the meeting, so that we have the most informed discussions possible, leading to reasoned decisions.
- The meeting will handle Agenda items first, and if time permits, collaborative bug triage.
- We strive to timebox the core of the meeting (decision making) to 30 minutes, with an optional free discussion/live debugging afterwards.
- We take comprehensive notes in the Weekly Agenda of agenda item discussions and of decisions taken.

---

## 🚀 Contributing

1. **Fork and Branch:** Create a new branch for your work.
2. **Make Changes:** Update files, add designs, or write docs.
3. **Pull Request:** Open a PR, clearly describing your changes.
4. **Review:** Request feedback from relevant team members.
5. **Merge:** After approvals, merge your branch.

See the [Contributing section](#-contributing) for details.

---

## 📝 Useful Resources

- [Open Food Facts main site](https://openfoodfacts.org/)
- [Open Food Facts GitHub](https://github.com/openfoodfacts/)
- [Figma Design System](https://www.figma.com/) (ask for access)
- [Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/standards-guidelines/wcag/)

---

# Figma

This guide helps you understand how to work with our design files, how to request access, and how to contribute even if you don't have full edit permissions.

## 💺 1. What is a "Figma Seat"?
In Figma, a **Seat** refers to a paid editor license. 
* **Viewer (Default):** Everyone can access this. You can see all designs, measurements, and export assets.
* **Editor (With Seat):** Allows you to modify the master design files directly.

> **Note:** Because Open Food Facts is a non-profit, we have a limited number of editor seats. We prioritize these for core designers and active contributors.

## 🚀 2. How to Contribute Without a Seat
You do **not** need a seat to be a successful contributor! Most tasks can be completed using these methods:
- **Inspect Mode:** Click any element in Figma to see its CSS, font sizes, colors, and spacing.
- **Exporting Assets:** You can export icons, illustrations, and images directly from the "Export" tab in the sidebar.
- **Duplicate to Drafts:** Go to `File > Duplicate to your drafts` to get a personal copy where you can experiment and edit freely.
- **Comment Tool:** Press `C` to leave suggestions or ask questions directly on the design for the team to see.

## 📝 3. Conditions to Request Edit Access
If your task requires moving elements in the main project file, you may request access if:
1. You have already made **1-2 consistent contributions** (code, documentation, or research).
2. You are assigned to a specific UI/UX task that requires **frequent design updates**.
3. You have introduced yourself in the **#design** Slack channel.

## 🛠️ 4. How to Request Access
If you meet the conditions above:
1. Comment on your assigned GitHub issue requesting access.
2. Provide your **Figma account email**.
3. **Alternative:** If a seat is not available, we may grant access to a **collective account**, or you can share your duplicated file link for review.

---

## 🙋 Need Help?

Open an issue or reach out in Slack. We’re happy to help!

---

Welcome aboard, and thank you for making food transparency more beautiful and usable for everyone!

---
